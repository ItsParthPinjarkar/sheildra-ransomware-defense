#!/usr/bin/env python3
"""
AutoVault Log Analyzer — Sandbox-executable script for log analysis.

This script analyzes system logs for security indicators and can be
executed safely in the TrueForge sandbox.
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict


class LogAnalyzer:
    """Analyze logs for security indicators."""
    
    # Suspicious patterns
    PATTERNS = {
        "failed_login": r"(?i)failed login|authentication failure|invalid password",
        "brute_force": r"(?i)multiple failed|too many attempts|account locked",
        "privilege_escalation": r"(?i)privilege|escalat|sudo|admin",
        "process_injection": r"(?i)inject|loadlib|createremotethread",
        "persistence": r"(?i)scheduled task|startup|run key|service install",
        "lateral_movement": r"(?i)remoteservice|psexec|wmic|smb",
        "data_exfiltration": r"(?i)upload|transfer|exfiltrat|dump",
        "ransomware": r"(?i)encrypt|decrypt|locked|ransom|bitcoin",
        "suspicious_network": r"(?i)connection.*external|unknown.*ip|suspicious.*dest",
        "file_modification": r"(?i)modified|changed|renamed|deleted"
    }
    
    # Severity levels
    SEVERITY = {
        "CRITICAL": ["ransomware", "data_exfiltration", "privilege_escalation"],
        "HIGH": ["brute_force", "lateral_movement", "process_injection"],
        "MEDIUM": ["failed_login", "suspicious_network", "persistence"],
        "LOW": ["file_modification"]
    }
    
    def __init__(self):
        self.findings = []
        self.timeline = []
        self.statistics = defaultdict(int)
    
    def analyze_line(self, line: str, source: str) -> List[Dict[str, Any]]:
        """Analyze a single log line."""
        findings = []
        
        for pattern_name, pattern in self.PATTERNS.items():
            if re.search(pattern, line):
                severity = self._get_severity(pattern_name)
                finding = {
                    "pattern": pattern_name,
                    "severity": severity,
                    "source": source,
                    "line": line[:200],
                    "timestamp": self._extract_timestamp(line)
                }
                findings.append(finding)
                self.statistics[pattern_name] += 1
        
        return findings
    
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a log file."""
        findings = []
        
        try:
            with open(filepath, 'r', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line_findings = self.analyze_line(line, filepath)
                    for finding in line_findings:
                        finding["line_number"] = line_num
                    findings.extend(line_findings)
        except Exception as e:
            return {"error": str(e), "file": filepath}
        
        self.findings.extend(findings)
        
        return {
            "file": filepath,
            "lines_analyzed": line_num if 'line_num' in dir() else 0,
            "findings": findings,
            "finding_count": len(findings)
        }
    
    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze all log files in a directory."""
        results = {
            "directory": directory,
            "files_analyzed": 0,
            "total_findings": 0,
            "findings_by_severity": defaultdict(list),
            "findings_by_pattern": defaultdict(int),
            "timeline": []
        }
        
        try:
            for entry in os.scandir(directory):
                if entry.is_file() and entry.name.endswith(('.log', '.txt', '.csv')):
                    file_result = self.analyze_file(entry.path)
                    if "error" not in file_result:
                        results["files_analyzed"] += 1
                        results["total_findings"] += file_result["finding_count"]
                        
                        for finding in file_result["findings"]:
                            results["findings_by_severity"][finding["severity"]].append(finding)
                            results["findings_by_pattern"][finding["pattern"]] += 1
                            results["timeline"].append(finding)
        except Exception as e:
            results["error"] = str(e)
        
        # Sort timeline
        results["timeline"].sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Convert defaultdicts to regular dicts for JSON
        results["findings_by_severity"] = dict(results["findings_by_severity"])
        results["findings_by_pattern"] = dict(results["findings_by_pattern"])
        
        # Calculate risk score
        risk_score = 0
        for severity, findings in results["findings_by_severity"].items():
            if severity == "CRITICAL":
                risk_score += len(findings) * 25
            elif severity == "HIGH":
                risk_score += len(findings) * 15
            elif severity == "MEDIUM":
                risk_score += len(findings) * 10
            else:
                risk_score += len(findings) * 5
        
        results["risk_score"] = min(risk_score, 100)
        results["risk_level"] = self._calculate_risk_level(risk_score)
        
        return results
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive analysis report."""
        report = {
            "report_id": f"LA-{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "files_analyzed": analysis_results.get("files_analyzed", 0),
                "total_findings": analysis_results.get("total_findings", 0),
                "risk_score": analysis_results.get("risk_score", 0),
                "risk_level": analysis_results.get("risk_level", "UNKNOWN")
            },
            "critical_findings": [],
            "high_findings": [],
            "recommendations": []
        }
        
        # Extract critical and high findings
        for severity, findings in analysis_results.get("findings_by_severity", {}).items():
            if severity == "CRITICAL":
                report["critical_findings"] = findings[:10]
            elif severity == "HIGH":
                report["high_findings"] = findings[:10]
        
        # Generate recommendations
        if report["summary"]["risk_level"] == "CRITICAL":
            report["recommendations"] = [
                "IMMEDIATE ACTION REQUIRED",
                "Critical security findings detected",
                "Initiate incident response procedures",
                "Preserve all evidence",
                "Isolate affected systems"
            ]
        elif report["summary"]["risk_level"] == "HIGH":
            report["recommendations"] = [
                "High-risk findings detected",
                "Investigate immediately",
                "Increase monitoring",
                "Review access controls"
            ]
        elif report["summary"]["risk_level"] == "MEDIUM":
            report["recommendations"] = [
                "Medium-risk findings detected",
                "Review flagged events",
                "Update detection rules"
            ]
        else:
            report["recommendations"] = [
                "Low-risk findings only",
                "Continue normal monitoring",
                "Review logs periodically"
            ]
        
        return report
    
    def _get_severity(self, pattern_name: str) -> str:
        """Get severity level for a pattern."""
        for severity, patterns in self.SEVERITY.items():
            if pattern_name in patterns:
                return severity
        return "INFO"
    
    def _extract_timestamp(self, line: str) -> str:
        """Extract timestamp from log line."""
        # Common timestamp patterns
        patterns = [
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
            r"\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}",
            r"\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}",
            r"\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(0)
        
        return ""
    
    def _calculate_risk_level(self, score: int) -> str:
        """Calculate risk level from score."""
        if score >= 75:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"


def main():
    """Main entry point for sandbox execution."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: log_analyzer.py <directory_or_file>"}))
        sys.exit(1)
    
    target = sys.argv[1]
    analyzer = LogAnalyzer()
    
    if os.path.isfile(target):
        result = analyzer.analyze_file(target)
    elif os.path.isdir(target):
        result = analyzer.analyze_directory(target)
    else:
        result = {"error": f"Target not found: {target}"}
    
    # Generate report
    if "error" not in result:
        report = analyzer.generate_report(result)
        result["report"] = report
    
    # Output as JSON
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
