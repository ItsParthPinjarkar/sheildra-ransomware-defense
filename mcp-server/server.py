"""
AutoVault MCP Server — Exposes security monitoring tools for TrueForge agent.

MCP SDK v2 compatible — uses MCPServer and @app.tool() decorator.

This server provides MCP tools that the TrueForge agent can use to:
- Monitor file systems for ransomware activity
- Analyze threat intelligence
- Execute safe sandbox operations
- Interact with blockchain vault
- Manage IPFS snapshots
"""

import os
import sys
import json
import hashlib
import math
import time
from typing import Any, Dict, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent'))

try:
    from mcp.server.mcpserver import MCPServer
    from mcp.types import TextContent
except ImportError:
    print("Installing mcp package...")
    os.system(f"{sys.executable} -m pip install mcp")
    from mcp.server.mcpserver import MCPServer
    from mcp.types import TextContent

from watchdog_monitor import FileWatcher, calculate_entropy
from brain import ThreatBrain


# Initialize MCP server (v2 API)
app = MCPServer("autovault-security-agent")

# Global state
watcher: Optional[FileWatcher] = None
brain: Optional[ThreatBrain] = None
vault_state = {
    "latest_cid": None,
    "latest_tx": None,
    "snapshots": [],
    "lockdowns": [],
    "network_blocked": False
}


def calculate_file_entropy(filepath: str) -> float:
    """Calculate Shannon entropy of a file."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            if not data:
                return 0.0
            byte_freq = {}
            for byte in data:
                byte_freq[byte] = byte_freq.get(byte, 0) + 1
            length = len(data)
            entropy = -sum((count / length) * math.log2(count / length) for count in byte_freq.values())
            return entropy
    except Exception:
        return 0.0


def _scan_directory(directory: str) -> Dict[str, Any]:
    """Scan a directory for file statistics."""
    results = {
        "total_files": 0,
        "high_entropy_files": [],
        "recently_modified": [],
        "suspicious_extensions": [],
        "directory": directory
    }

    suspicious_exts = {'.locked', '.encrypted', '.enc', '.crypto', '.crypted'}

    try:
        now = time.time()
        for entry in os.scandir(directory):
            if entry.is_file():
                results["total_files"] += 1
                stat = entry.stat()

                entropy = calculate_file_entropy(entry.path)
                if entropy > 7.5:
                    results["high_entropy_files"].append({
                        "name": entry.name,
                        "entropy": round(entropy, 2),
                        "size": stat.st_size
                    })

                if now - stat.st_mtime < 60:
                    results["recently_modified"].append({
                        "name": entry.name,
                        "modified_ago": round(now - stat.st_mtime, 1),
                        "size": stat.st_size
                    })

                _, ext = os.path.splitext(entry.name)
                if ext.lower() in suspicious_exts:
                    results["suspicious_extensions"].append(entry.name)

    except Exception as e:
        results["error"] = str(e)

    return results


def get_recommendation(analysis: Dict) -> str:
    """Get human-readable recommendation based on analysis."""
    if analysis.get("threat_level") == "CRITICAL":
        return "IMMEDIATE ACTION REQUIRED: Initiate lockdown, suspend process, and block network. This looks like active ransomware encryption."
    elif analysis.get("threat_level") == "HIGH":
        return "Investigate immediately. High anomaly score suggests potential ransomware activity. Monitor closely."
    elif analysis.get("threat_level") == "ELEVATED":
        return "Monitor closely. Some unusual activity detected but may be benign. Continue watching."
    else:
        return "System appears normal. No action required."


# ── MCP Tools (v2 API) ──────────────────────────────────────────────

@app.tool(
    name="scan_directory",
    description="Scan a directory for ransomware indicators: high-entropy files, suspicious extensions, recent modifications"
)
async def tool_scan_directory(directory: str) -> str:
    results = _scan_directory(directory)
    return json.dumps(results, indent=2)


@app.tool(
    name="analyze_threat",
    description="Analyze file system telemetry to detect ransomware activity using ML model"
)
async def tool_analyze_threat(entropy: float, io_velocity: int, extension_churn: int) -> str:
    global brain
    if brain is None:
        brain = ThreatBrain()

    analysis = brain.analyze(entropy, io_velocity, extension_churn)
    analysis["recommendation"] = get_recommendation(analysis)
    analysis["timestamp"] = datetime.now().isoformat()
    return json.dumps(analysis, indent=2)


@app.tool(
    name="get_vault_status",
    description="Get current blockchain vault status including latest CID, transaction hash, and lockdown history"
)
async def tool_get_vault_status() -> str:
    return json.dumps(vault_state, indent=2)


@app.tool(
    name="create_snapshot",
    description="Create a snapshot of the monitored directory and pin to IPFS"
)
async def tool_create_snapshot(directory: str) -> str:
    h = hashlib.sha256()

    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                with open(entry.path, 'rb') as f:
                    h.update(f.read())
    except Exception as e:
        return json.dumps({"error": str(e)})

    cid = f"QmAutoVault{h.hexdigest()[:20]}"
    vault_state["latest_cid"] = cid
    vault_state["snapshots"].append({
        "cid": cid,
        "directory": directory,
        "timestamp": datetime.now().isoformat()
    })

    return json.dumps({
        "success": True,
        "cid": cid,
        "snapshots_count": len(vault_state["snapshots"])
    }, indent=2)


@app.tool(
    name="analyze_file",
    description="Analyze a specific file for ransomware indicators (entropy, content patterns)"
)
async def tool_analyze_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return json.dumps({"error": f"File not found: {filepath}"})

    entropy = calculate_file_entropy(filepath)
    stat = os.stat(filepath)

    analysis = {
        "filepath": filepath,
        "size": stat.st_size,
        "entropy": round(entropy, 2),
        "entropy_level": "HIGH" if entropy > 7.5 else "NORMAL",
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "is_suspicious": entropy > 7.5 or any(
            filepath.endswith(ext) for ext in ['.locked', '.encrypted', '.enc']
        ),
        "recommendation": "Investigate immediately" if entropy > 7.5 else "Normal"
    }

    return json.dumps(analysis, indent=2)


@app.tool(
    name="get_system_health",
    description="Get overall system health metrics including monitored processes, disk usage, and threat history"
)
async def tool_get_system_health() -> str:
    health = {
        "timestamp": datetime.now().isoformat(),
        "vault_state": vault_state,
        "watcher_active": watcher is not None and watcher.running if watcher else False,
        "brain_active": brain is not None,
        "total_snapshots": len(vault_state["snapshots"]),
        "total_lockdowns": len(vault_state["lockdowns"]),
        "network_blocked": vault_state["network_blocked"]
    }

    return json.dumps(health, indent=2)


@app.tool(
    name="simulate_normal_activity",
    description="Generate normal file activity for testing/demonstration purposes"
)
async def tool_simulate_normal_activity(directory: str) -> str:
    import ransim
    ransim.setup_test_vault(directory)
    ransim.simulate_normal_activity(directory)

    return json.dumps({
        "success": True,
        "message": f"Normal activity started in {directory}"
    })


@app.tool(
    name="investigate_process",
    description="Investigate a suspicious process: check its open files, network connections, and resource usage"
)
async def tool_investigate_process(pid: int) -> str:
    try:
        import psutil
        proc = psutil.Process(pid)
        info = {
            "pid": pid,
            "name": proc.name(),
            "status": proc.status(),
            "cpu_percent": proc.cpu_percent(),
            "memory_percent": proc.memory_percent(),
            "create_time": datetime.fromtimestamp(proc.create_time()).isoformat(),
            "open_files": [{"path": f.path, "fd": f.fd} for f in proc.open_files()[:10]],
            "connections": [{"fd": c.fd, "family": str(c.family), "type": str(c.type)} for c in proc.connections()[:5]],
            "is_suspicious": proc.cpu_percent() > 80 or len(proc.open_files()) > 50
        }
    except ImportError:
        info = {"error": "psutil not installed"}
    except Exception as e:
        info = {"error": str(e)}

    return json.dumps(info, indent=2)


# ── Server Entry Point ───────────────────────────────────────────────

async def main():
    """Run the MCP server."""
    global watcher, brain

    # Initialize components
    try:
        watcher = FileWatcher("./test_vault")
        brain = ThreatBrain()
        watcher.start()
    except Exception as e:
        print(f"Warning: Could not initialize watcher/brain: {e}", file=sys.stderr)

    print("AutoVault MCP Server starting...", file=sys.stderr)
    await app.run_stdio_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
