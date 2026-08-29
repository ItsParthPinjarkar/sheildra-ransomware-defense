"""
AutoVault Forensics MCP Server — Deep forensic analysis tools.

MCP SDK v2 compatible — uses MCPServer and @app.tool() decorator.

Provides TrueForge agent with:
- File content analysis
- Binary entropy mapping
- Metadata extraction
- Timeline reconstruction
- Evidence collection
"""

import os
import sys
import json
import hashlib
import math
import time
from typing import Any, Dict, List
from datetime import datetime

from mcp.server.mcpserver import MCPServer
from mcp.types import TextContent

app = MCPServer("autovault-forensics")


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


def calculate_entropy_map(filepath: str, chunk_size: int = 1024) -> List[Dict[str, Any]]:
    """Calculate entropy map of a file (entropy per chunk)."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            if not data:
                return []

            entropy_map = []
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                if not chunk:
                    continue

                byte_freq = {}
                for byte in chunk:
                    byte_freq[byte] = byte_freq.get(byte, 0) + 1
                length = len(chunk)
                entropy = -sum((count / length) * math.log2(count / length) for count in byte_freq.values())

                entropy_map.append({
                    "offset": i,
                    "size": len(chunk),
                    "entropy": round(entropy, 4),
                    "is_encrypted": entropy > 7.5
                })

            return entropy_map
    except Exception:
        return []


def extract_file_metadata(filepath: str) -> Dict[str, Any]:
    """Extract comprehensive file metadata."""
    try:
        stat = os.stat(filepath)

        md5_hash = hashlib.md5()
        sha1_hash = hashlib.sha1()
        sha256_hash = hashlib.sha256()

        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)

        return {
            "path": filepath,
            "name": os.path.basename(filepath),
            "extension": os.path.splitext(filepath)[1],
            "size": stat.st_size,
            "size_human": format_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:],
            "md5": md5_hash.hexdigest(),
            "sha1": sha1_hash.hexdigest(),
            "sha256": sha256_hash.hexdigest(),
            "entropy": round(calculate_file_entropy(filepath), 4),
            "is_suspicious": calculate_file_entropy(filepath) > 7.5
        }
    except Exception as e:
        return {"error": str(e)}


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def build_timeline(directory: str) -> List[Dict[str, Any]]:
    """Build file modification timeline."""
    timeline = []

    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                stat = entry.stat()
                timeline.append({
                    "filename": entry.name,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                    "size": stat.st_size,
                    "entropy": round(calculate_file_entropy(entry.path), 4)
                })

        timeline.sort(key=lambda x: x["modified"])
    except Exception as e:
        timeline.append({"error": str(e)})

    return timeline


def detect_ransomware_indicators(directory: str) -> Dict[str, Any]:
    """Detect ransomware indicators in a directory."""
    indicators = {
        "encrypted_files": [],
        "suspicious_extensions": [],
        "high_entropy_files": [],
        "recent_mass_modifications": [],
        "ransom_notes": [],
        "risk_score": 0,
        "risk_level": "LOW"
    }

    suspicious_exts = {'.locked', '.encrypted', '.enc', '.crypto', '.crypted', '.vault', '.cry'}
    ransom_keywords = ['readme', 'decrypt', 'recover', 'restore', 'help', 'how_to']

    now = time.time()
    recent_mods = []

    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                stat = entry.stat()
                _, ext = os.path.splitext(entry.name)
                name_lower = entry.name.lower()

                if ext.lower() in suspicious_exts:
                    indicators["suspicious_extensions"].append(entry.name)
                    indicators["risk_score"] += 30

                entropy = calculate_file_entropy(entry.path)
                if entropy > 7.5:
                    indicators["high_entropy_files"].append({
                        "name": entry.name,
                        "entropy": round(entropy, 2),
                        "size": stat.st_size
                    })
                    indicators["risk_score"] += 20

                if now - stat.st_mtime < 300:
                    recent_mods.append({
                        "name": entry.name,
                        "modified_ago": round(now - stat.st_mtime, 1)
                    })

                if any(kw in name_lower for kw in ransom_keywords):
                    indicators["ransom_notes"].append(entry.name)
                    indicators["risk_score"] += 50

        if len(recent_mods) > 5:
            indicators["recent_mass_modifications"] = recent_mods
            indicators["risk_score"] += 40

        if indicators["risk_score"] >= 100:
            indicators["risk_level"] = "CRITICAL"
        elif indicators["risk_score"] >= 60:
            indicators["risk_level"] = "HIGH"
        elif indicators["risk_score"] >= 30:
            indicators["risk_level"] = "MEDIUM"

    except Exception as e:
        indicators["error"] = str(e)

    return indicators


# ── MCP Tools (v2 API) ──────────────────────────────────────────────

@app.tool(
    name="analyze_file_deep",
    description="Deep forensic analysis of a file: hashes, entropy map, metadata"
)
async def tool_analyze_file_deep(filepath: str) -> str:
    metadata = extract_file_metadata(filepath)
    entropy_map = calculate_entropy_map(filepath)

    result = {
        "metadata": metadata,
        "entropy_map": entropy_map[:50],
        "total_chunks": len(entropy_map),
        "encrypted_chunks": sum(1 for e in entropy_map if e["is_encrypted"])
    }

    return json.dumps(result, indent=2)


@app.tool(
    name="build_timeline",
    description="Build file modification timeline for forensic reconstruction"
)
async def tool_build_timeline(directory: str) -> str:
    timeline = build_timeline(directory)
    return json.dumps(timeline, indent=2)


@app.tool(
    name="detect_ransomware",
    description="Comprehensive ransomware indicator detection"
)
async def tool_detect_ransomware(directory: str) -> str:
    indicators = detect_ransomware_indicators(directory)
    indicators["timestamp"] = datetime.now().isoformat()
    return json.dumps(indicators, indent=2)


@app.tool(
    name="compare_snapshots",
    description="Compare two file snapshots to detect changes"
)
async def tool_compare_snapshots(snapshot_before: str, snapshot_after: str) -> str:
    before = json.loads(snapshot_before)
    after = json.loads(snapshot_after)

    before_files = {f["name"]: f for f in before.get("files", [])}
    after_files = {f["name"]: f for f in after.get("files", [])}

    added = set(after_files.keys()) - set(before_files.keys())
    removed = set(before_files.keys()) - set(after_files.keys())
    modified = set()

    for fname in set(before_files.keys()) & set(after_files.keys()):
        if before_files[fname].get("hash") != after_files[fname].get("hash"):
            modified.add(fname)

    diff = {
        "files_added": list(added),
        "files_removed": list(removed),
        "files_modified": list(modified),
        "total_changes": len(added) + len(removed) + len(modified)
    }

    return json.dumps(diff, indent=2)


@app.tool(
    name="generate_forensic_report",
    description="Generate comprehensive forensic report for a directory"
)
async def tool_generate_forensic_report(directory: str) -> str:
    timeline = build_timeline(directory)
    indicators = detect_ransomware_indicators(directory)

    total_files = len([t for t in timeline if "error" not in t])
    total_size = sum(t.get("size", 0) for t in timeline if "error" not in t)
    avg_entropy = sum(t.get("entropy", 0) for t in timeline if "error" not in t) / max(total_files, 1)

    report = {
        "report_id": f"FR-{int(time.time())}",
        "timestamp": datetime.now().isoformat(),
        "directory": directory,
        "summary": {
            "total_files": total_files,
            "total_size": format_size(total_size),
            "average_entropy": round(avg_entropy, 4),
            "risk_level": indicators["risk_level"],
            "risk_score": indicators["risk_score"]
        },
        "indicators": indicators,
        "timeline": timeline,
        "recommendations": []
    }

    if indicators["risk_level"] == "CRITICAL":
        report["recommendations"].extend([
            "IMMEDIATE: Initiate full system lockdown",
            "Suspend all suspicious processes",
            "Block all network connections",
            "Preserve forensic evidence",
            "Contact incident response team"
        ])
    elif indicators["risk_level"] == "HIGH":
        report["recommendations"].extend([
            "Increase monitoring frequency",
            "Investigate high-entropy files",
            "Review recent file modifications",
            "Prepare for potential lockdown"
        ])
    else:
        report["recommendations"].append("Continue normal monitoring")

    return json.dumps(report, indent=2)


# ── Server Entry Point ───────────────────────────────────────────────

async def main():
    """Run the MCP server."""
    print("AutoVault Forensics MCP Server starting...", file=sys.stderr)
    await app.run_stdio_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
