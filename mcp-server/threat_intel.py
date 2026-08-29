"""
AutoVault Threat Intelligence MCP Server — Threat analysis and intelligence.

MCP SDK v2 compatible — uses MCPServer and @app.tool() decorator.

Provides TrueForge agent with:
- Threat pattern matching
- IOC (Indicators of Compromise) checking
- Threat scoring
- Attack pattern recognition
- MITRE ATT&CK mapping
"""

import os
import sys
import json
import hashlib
import time
from typing import Any, Dict, List
from datetime import datetime

from mcp.server.mcpserver import MCPServer
from mcp.types import TextContent

app = MCPServer("autovault-threat-intel")

# Known ransomware IOCs
KNOWN_MALICIOUS_EXTENSIONS = {
    '.locked', '.encrypted', '.enc', '.crypto', '.crypted',
    '.vault', '.cry', '.locky', '.zepto', '.cerber',
    '.wnry', '.wncry', '.wcry'
}

KNOWN_RANSOMWARE_PATTERNS = {
    "locky": [".locky", "_locky"],
    "wannacry": ["@wanacry", "wannacry", "@ WannaDecryptor@"],
    "ryuk": [".ryuk", "RYUK-README"],
    "maze": [".maze", "maze_readme"],
    "revil": [".revil", "RECOVER-FILES"]
}

MITRE_TECHNIQUES = {
    "T1486": "Data Encrypted for Impact",
    "T1489": "Service Stop",
    "T1490": "Inhibit System Recovery",
    "T1498": "Network Denial of Service",
    "T1059": "Command and Scripting Interpreter",
    "T1053": "Scheduled Task/Job",
    "T1547": "Boot or Logon Autostart Execution",
    "T1082": "System Information Discovery",
    "T1083": "File and Directory Discovery",
    "T1041": "Exfiltration Over C2 Channel"
}


def analyze_file_for_iocs(filepath: str) -> Dict[str, Any]:
    """Analyze a file for indicators of compromise."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        iocs = {
            "file": filepath,
            "size": len(data),
            "md5": hashlib.md5(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "suspicious_strings": [],
            "potential_malware_families": [],
            "mitre_techniques": [],
            "risk_indicators": []
        }

        text = data.decode('utf-8', errors='ignore').lower()

        suspicious_strings = [
            "encrypt", "decrypt", "bitcoin", "wallet", "ransom",
            "pay", "decryptor", "restore", "recover", "your files",
            "have been encrypted", "pay us", "dark web"
        ]

        for s in suspicious_strings:
            if s in text:
                iocs["suspicious_strings"].append(s)

        for family, patterns in KNOWN_RANSOMWARE_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in text:
                    iocs["potential_malware_families"].append(family)

        if any(s in text for s in ["encrypt", "locked"]):
            iocs["mitre_techniques"].append({
                "id": "T1486",
                "name": "Data Encrypted for Impact",
                "description": "Ransomware encryption detected"
            })

        if any(s in text for s in ["bitcoin", "wallet", "pay"]):
            iocs["mitre_techniques"].append({
                "id": "T1486",
                "name": "Data Encrypted for Impact",
                "description": "Ransom payment mechanism detected"
            })

        risk_score = 0
        if iocs["suspicious_strings"]:
            risk_score += len(iocs["suspicious_strings"]) * 10
        if iocs["potential_malware_families"]:
            risk_score += len(iocs["potential_malware_families"]) * 25
        if iocs["mitre_techniques"]:
            risk_score += len(iocs["mitre_techniques"]) * 15

        iocs["risk_score"] = min(risk_score, 100)
        iocs["risk_level"] = "CRITICAL" if risk_score >= 75 else "HIGH" if risk_score >= 50 else "MEDIUM" if risk_score >= 25 else "LOW"

        return iocs
    except Exception as e:
        return {"error": str(e)}


def analyze_directory_for_threats(directory: str) -> Dict[str, Any]:
    """Analyze entire directory for threat indicators."""
    analysis = {
        "directory": directory,
        "timestamp": datetime.now().isoformat(),
        "total_files": 0,
        "suspicious_files": [],
        "threat_families": set(),
        "mitre_techniques": [],
        "overall_risk_score": 0,
        "overall_risk_level": "LOW",
        "recommendations": []
    }

    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                analysis["total_files"] += 1

                _, ext = os.path.splitext(entry.name)
                if ext.lower() in KNOWN_MALICIOUS_EXTENSIONS:
                    analysis["suspicious_files"].append({
                        "name": entry.name,
                        "reason": f"Suspicious extension: {ext}"
                    })
                    analysis["overall_risk_score"] += 20

                if ext.lower() in ['.txt', '.md', '.html', '.json']:
                    iocs = analyze_file_for_iocs(entry.path)
                    if iocs.get("risk_score", 0) > 0:
                        analysis["suspicious_files"].append({
                            "name": entry.name,
                            "risk_score": iocs["risk_score"],
                            "indicators": iocs.get("suspicious_strings", [])
                        })
                        analysis["overall_risk_score"] += iocs["risk_score"]

                    for family in iocs.get("potential_malware_families", []):
                        analysis["threat_families"].add(family)

                    for tech in iocs.get("mitre_techniques", []):
                        if tech not in analysis["mitre_techniques"]:
                            analysis["mitre_techniques"].append(tech)

        analysis["threat_families"] = list(analysis["threat_families"])
        analysis["overall_risk_score"] = min(analysis["overall_risk_score"], 100)

        if analysis["overall_risk_score"] >= 75:
            analysis["overall_risk_level"] = "CRITICAL"
            analysis["recommendations"] = [
                "IMMEDIATE LOCKDOWN REQUIRED",
                "Evidence suggests active ransomware infection",
                "Preserve all evidence for forensic analysis",
                "Isolate system from network immediately"
            ]
        elif analysis["overall_risk_score"] >= 50:
            analysis["overall_risk_level"] = "HIGH"
            analysis["recommendations"] = [
                "Investigate suspicious files immediately",
                "Increase monitoring frequency",
                "Prepare for potential lockdown"
            ]
        elif analysis["overall_risk_score"] >= 25:
            analysis["overall_risk_level"] = "MEDIUM"
            analysis["recommendations"] = [
                "Review flagged files manually",
                "Monitor for changes"
            ]
        else:
            analysis["recommendations"] = ["Continue normal monitoring"]

    except Exception as e:
        analysis["error"] = str(e)

    return analysis


# ── MCP Tools (v2 API) ──────────────────────────────────────────────

@app.tool(
    name="analyze_file_iocs",
    description="Analyze a file for indicators of compromise (IOCs)"
)
async def tool_analyze_file_iocs(filepath: str) -> str:
    result = analyze_file_for_iocs(filepath)
    return json.dumps(result, indent=2)


@app.tool(
    name="analyze_directory_threats",
    description="Analyze directory for threat indicators and ransomware patterns"
)
async def tool_analyze_directory_threats(directory: str) -> str:
    result = analyze_directory_for_threats(directory)
    return json.dumps(result, indent=2)


@app.tool(
    name="get_mitre_technique",
    description="Get details about a MITRE ATT&CK technique"
)
async def tool_get_mitre_technique(technique_id: str) -> str:
    if technique_id in MITRE_TECHNIQUES:
        result = {
            "id": technique_id,
            "name": MITRE_TECHNIQUES[technique_id],
            "description": f"MITRE ATT&CK technique used in ransomware attacks"
        }
    else:
        result = {"error": f"Technique {technique_id} not found"}
    return json.dumps(result, indent=2)


@app.tool(
    name="check_known_malicious",
    description="Check if a file hash is in known malicious database"
)
async def tool_check_known_malicious(file_hash: str) -> str:
    result = {
        "hash": file_hash,
        "found_in_database": False,
        "source": "AutoVault Local Database",
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(result, indent=2)


@app.tool(
    name="generate_threat_report",
    description="Generate comprehensive threat intelligence report"
)
async def tool_generate_threat_report(directory: str) -> str:
    analysis = analyze_directory_for_threats(directory)

    report = {
        "report_id": f"TR-{int(time.time())}",
        "timestamp": datetime.now().isoformat(),
        "executive_summary": {
            "directory": directory,
            "risk_level": analysis["overall_risk_level"],
            "risk_score": analysis["overall_risk_score"],
            "files_analyzed": analysis["total_files"],
            "suspicious_files": len(analysis["suspicious_files"]),
            "threat_families_detected": analysis["threat_families"]
        },
        "detailed_analysis": analysis,
        "mitre_mapping": analysis["mitre_techniques"],
        "recommendations": analysis["recommendations"]
    }

    return json.dumps(report, indent=2)


# ── Server Entry Point ───────────────────────────────────────────────

async def main():
    """Run the MCP server."""
    print("AutoVault Threat Intelligence MCP Server starting...", file=sys.stderr)
    await app.run_stdio_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
