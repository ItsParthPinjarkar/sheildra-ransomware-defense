"""
AutoVault Network Monitor MCP Server — Advanced network analysis tools.

MCP SDK v2 compatible — uses MCPServer and @app.tool() decorator.

Provides TrueForge agent with:
- Network connection monitoring
- Traffic analysis
- DNS monitoring
- Bandwidth analysis
- Connection anomaly detection
"""

import os
import sys
import json
import time
from typing import Any, Dict, List
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

from mcp.server.mcpserver import MCPServer
from mcp.types import TextContent

app = MCPServer("autovault-network-monitor")


def get_network_connections() -> List[Dict[str, Any]]:
    """Get all active network connections."""
    if psutil is None:
        return [{"error": "psutil not installed"}]

    connections = []
    for conn in psutil.net_connections():
        try:
            connections.append({
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type),
                "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                "status": conn.status,
                "pid": conn.pid
            })
        except Exception:
            continue
    return connections


def get_network_io() -> Dict[str, Any]:
    """Get network I/O statistics."""
    if psutil is None:
        return {"error": "psutil not installed"}

    io = psutil.net_io_counters()
    return {
        "bytes_sent": io.bytes_sent,
        "bytes_recv": io.bytes_recv,
        "packets_sent": io.packets_sent,
        "packets_recv": io.packets_recv,
        "errin": io.errin,
        "errout": io.errout,
        "dropin": io.dropin,
        "dropout": io.dropout
    }


def get_listening_ports() -> List[Dict[str, Any]]:
    """Get all listening ports."""
    if psutil is None:
        return [{"error": "psutil not installed"}]

    ports = []
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN':
            try:
                ports.append({
                    "port": conn.laddr.port,
                    "ip": conn.laddr.ip,
                    "pid": conn.pid,
                    "process": psutil.Process(conn.pid).name() if conn.pid else "unknown"
                })
            except Exception:
                continue
    return ports


def analyze_connection_patterns(connections: List[Dict]) -> Dict[str, Any]:
    """Analyze connection patterns for anomalies."""
    analysis = {
        "total_connections": len(connections),
        "established": 0,
        "listening": 0,
        "time_wait": 0,
        "close_wait": 0,
        "foreign_ips": set(),
        "high_port_count": 0,
        "suspicious_patterns": []
    }

    for conn in connections:
        status = conn.get("status", "")
        if status == "ESTABLISHED":
            analysis["established"] += 1
        elif status == "LISTEN":
            analysis["listening"] += 1
        elif status == "TIME_WAIT":
            analysis["time_wait"] += 1
        elif status == "CLOSE_WAIT":
            analysis["close_wait"] += 1

        raddr = conn.get("raddr", "")
        if raddr:
            ip = raddr.split(":")[0] if ":" in raddr else raddr
            analysis["foreign_ips"].add(ip)

        laddr = conn.get("laddr", "")
        if laddr and ":" in laddr:
            port = int(laddr.split(":")[1])
            if port > 49152:
                analysis["high_port_count"] += 1

    analysis["foreign_ips"] = list(analysis["foreign_ips"])
    analysis["unique_foreign_ips"] = len(analysis["foreign_ips"])

    if analysis["established"] > 100:
        analysis["suspicious_patterns"].append("High number of established connections")
    if analysis["high_port_count"] > 20:
        analysis["suspicious_patterns"].append("Many high-port connections (possible C2)")
    if analysis["close_wait"] > 10:
        analysis["suspicious_patterns"].append("Many CLOSE_WAIT connections (possible leak)")
    if analysis["unique_foreign_ips"] > 50:
        analysis["suspicious_patterns"].append("Connections to many foreign IPs (possible scan)")

    return analysis


# ── MCP Tools (v2 API) ──────────────────────────────────────────────

@app.tool(
    name="get_network_connections",
    description="Get all active network connections with details"
)
async def tool_get_network_connections() -> str:
    connections = get_network_connections()
    return json.dumps(connections, indent=2)


@app.tool(
    name="get_network_io",
    description="Get network I/O statistics (bytes sent/received, packets, errors)"
)
async def tool_get_network_io() -> str:
    io_stats = get_network_io()
    return json.dumps(io_stats, indent=2)


@app.tool(
    name="get_listening_ports",
    description="Get all listening ports and their associated processes"
)
async def tool_get_listening_ports() -> str:
    ports = get_listening_ports()
    return json.dumps(ports, indent=2)


@app.tool(
    name="analyze_network",
    description="Analyze network patterns for anomalies and suspicious activity"
)
async def tool_analyze_network() -> str:
    connections = get_network_connections()
    analysis = analyze_connection_patterns(connections)
    analysis["timestamp"] = datetime.now().isoformat()
    return json.dumps(analysis, indent=2)


@app.tool(
    name="check_suspicious_connections",
    description="Check for connections to known suspicious ports or patterns"
)
async def tool_check_suspicious_connections(suspicious_ports: list = None) -> str:
    if suspicious_ports is None:
        suspicious_ports = [4444, 5555, 6666, 7777, 8888, 9999, 1234, 31337]

    connections = get_network_connections()

    suspicious = []
    for conn in connections:
        raddr = conn.get("raddr", "")
        if raddr and ":" in raddr:
            port = int(raddr.split(":")[1])
            if port in suspicious_ports:
                suspicious.append({
                    "connection": conn,
                    "reason": f"Connected to suspicious port {port}"
                })

    result = {
        "suspicious_connections": suspicious,
        "total_checked": len(connections),
        "suspicious_count": len(suspicious),
        "suspicious_ports_checked": suspicious_ports
    }

    return json.dumps(result, indent=2)


# ── Server Entry Point ───────────────────────────────────────────────

async def main():
    """Run the MCP server."""
    print("AutoVault Network Monitor MCP Server starting...", file=sys.stderr)
    await app.run_stdio_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
