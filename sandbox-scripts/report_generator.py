#!/usr/bin/env python3
"""
AutoVault Report Generator — Sandbox-executable script for generating reports.

This script generates comprehensive security reports in multiple formats
that can be executed safely in the TrueForge sandbox.
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any


class ReportGenerator:
    """Generate comprehensive security reports."""
    
    def __init__(self):
        self.report_id = f"RPT-{int(datetime.now().timestamp())}"
    
    def generate_incident_report(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive incident report."""
        report = {
            "report_id": self.report_id,
            "report_type": "INCIDENT",
            "generated_at": datetime.now().isoformat(),
            "classification": incident_data.get("severity", "UNKNOWN"),
            
            "executive_summary": {
                "incident_id": incident_data.get("incident_id", "UNKNOWN"),
                "severity": incident_data.get("severity", "UNKNOWN"),
                "status": incident_data.get("status", "ACTIVE"),
                "impact_summary": incident_data.get("impact", "Under investigation"),
                "response_actions": incident_data.get("actions_taken", [])
            },
            
            "timeline": incident_data.get("timeline", []),
            
            "affected_systems": incident_data.get("affected_systems", []),
            
            "indicators_of_compromise": incident_data.get("iocs", []),
            
            "technical_analysis": {
                "attack_vector": incident_data.get("attack_vector", "Unknown"),
                "techniques_used": incident_data.get("techniques", []),
                "tools_detected": incident_data.get("tools", []),
                "malware_families": incident_data.get("malware_families", [])
            },
            
            "response_actions": {
                "immediate": incident_data.get("immediate_actions", []),
                "containment": incident_data.get("containment_actions", []),
                "eradication": incident_data.get("eradication_actions", []),
                "recovery": incident_data.get("recovery_actions", [])
            },
            
            "evidence_inventory": incident_data.get("evidence", []),
            
            "recommendations": {
                "immediate": [],
                "short_term": [],
                "long_term": []
            },
            
            "lessons_learned": incident_data.get("lessons", []),
            
            "appendices": {
                "raw_logs": incident_data.get("logs", []),
                "tool_output": incident_data.get("tool_output", []),
                "additional_data": incident_data.get("additional_data", {})
            }
        }
        
        # Generate recommendations based on severity
        severity = incident_data.get("severity", "LOW")
        
        if severity == "CRITICAL":
            report["recommendations"]["immediate"] = [
                "Isolate affected systems from network",
                "Preserve all forensic evidence",
                "Engage incident response team",
                "Notify affected parties",
                "Contact law enforcement if required"
            ]
            report["recommendations"]["short_term"] = [
                "Conduct full system audit",
                "Implement emergency patches",
                "Review access controls",
                "Enhance monitoring"
            ]
            report["recommendations"]["long_term"] = [
                "Implement zero-trust architecture",
                "Enhance security training",
                "Improve detection capabilities",
                "Regular penetration testing"
            ]
        elif severity == "HIGH":
            report["recommendations"]["immediate"] = [
                "Investigate scope of incident",
                "Increase monitoring",
                "Review suspicious activity"
            ]
            report["recommendations"]["short_term"] = [
                "Update security policies",
                "Enhance logging",
                "Review user access"
            ]
            report["recommendations"]["long_term"] = [
                "Improve detection rules",
                "Regular security assessments"
            ]
        else:
            report["recommendations"]["immediate"] = [
                "Monitor for escalation",
                "Review flagged activity"
            ]
            report["recommendations"]["short_term"] = [
                "Update detection signatures",
                "Review procedures"
            ]
        
        return report
    
    def generate_forensic_report(self, forensic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive forensic analysis report."""
        report = {
            "report_id": self.report_id,
            "report_type": "FORENSIC",
            "generated_at": datetime.now().isoformat(),
            
            "case_information": {
                "case_id": forensic_data.get("case_id", self.report_id),
                "investigator": forensic_data.get("investigator", "AutoVault Agent"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "classification": forensic_data.get("classification", "CONFIDENTIAL")
            },
            
            "evidence_inventory": forensic_data.get("evidence", []),
            
            "methodology": {
                "tools_used": forensic_data.get("tools", ["AutoVault Forensics"]),
                "techniques_applied": forensic_data.get("techniques", []),
                "chain_of_custody": forensic_data.get("chain_of_custody", [])
            },
            
            "findings": forensic_data.get("findings", []),
            
            "timeline_reconstruction": forensic_data.get("timeline", []),
            
            "indicators_of_compromise": forensic_data.get("iocs", []),
            
            "analysis_results": {
                "file_analysis": forensic_data.get("file_analysis", {}),
                "network_analysis": forensic_data.get("network_analysis", {}),
                "memory_analysis": forensic_data.get("memory_analysis", {}),
                "log_analysis": forensic_data.get("log_analysis", {})
            },
            
            "conclusions": forensic_data.get("conclusions", []),
            
            "recommendations": forensic_data.get("recommendations", []),
            
            "digital_signatures": self._generate_signatures(forensic_data),
            
            "appendices": {
                "raw_data": forensic_data.get("raw_data", {}),
                "supplementary_information": forensic_data.get("supplementary", {})
            }
        }
        
        return report
    
    def generate_threat_report(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a threat intelligence report."""
        report = {
            "report_id": self.report_id,
            "report_type": "THREAT_INTELLIGENCE",
            "generated_at": datetime.now().isoformat(),
            
            "threat_summary": {
                "threat_level": threat_data.get("threat_level", "UNKNOWN"),
                "threat_type": threat_data.get("threat_type", "Unknown"),
                "confidence_level": threat_data.get("confidence", "Low"),
                "first_seen": threat_data.get("first_seen", datetime.now().isoformat()),
                "last_seen": threat_data.get("last_seen", datetime.now().isoformat())
            },
            
            "indicators": {
                "file_hashes": threat_data.get("file_hashes", []),
                "ip_addresses": threat_data.get("ip_addresses", []),
                "domains": threat_data.get("domains", []),
                "urls": threat_data.get("urls", []),
                "email_addresses": threat_data.get("emails", [])
            },
            
            "mitre_attack_mapping": threat_data.get("mitre", []),
            
            "malware_analysis": {
                "family": threat_data.get("malware_family", "Unknown"),
                "variants": threat_data.get("variants", []),
                "capabilities": threat_data.get("capabilities", []),
                "infrastructure": threat_data.get("infrastructure", [])
            },
            
            "targeting_information": {
                "targeted_sectors": threat_data.get("sectors", []),
                "targeted_geographies": threat_data.get("geographies", []),
                "targeted_systems": threat_data.get("systems", [])
            },
            
            "detection_signatures": threat_data.get("signatures", []),
            
            "mitigation_strategies": threat_data.get("mitigations", []),
            
            "references": threat_data.get("references", [])
        }
        
        return report
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an executive summary."""
        summary = {
            "report_id": self.report_id,
            "report_type": "EXECUTIVE_SUMMARY",
            "generated_at": datetime.now().isoformat(),
            
            "overview": {
                "period": data.get("period", "Last 24 hours"),
                "total_incidents": data.get("total_incidents", 0),
                "critical_incidents": data.get("critical_incidents", 0),
                "high_incidents": data.get("high_incidents", 0),
                "systems_affected": data.get("systems_affected", 0),
                "data_exposed": data.get("data_exposed", "None confirmed")
            },
            
            "key_metrics": {
                "mean_time_to_detect": data.get("mttd", "N/A"),
                "mean_time_to_respond": data.get("mttr", "N/A"),
                "false_positive_rate": data.get("fpr", "N/A"),
                "detection_coverage": data.get("coverage", "N/A")
            },
            
            "threat_landscape": {
                "top_threats": data.get("top_threats", []),
                "trending_attacks": data.get("trending", []),
                "emerging_risks": data.get("emerging", [])
            },
            
            "recommendations_highlights": data.get("top_recommendations", []),
            
            "next_steps": data.get("next_steps", [])
        }
        
        return summary
    
    def export_markdown(self, report: Dict[str, Any]) -> str:
        """Export report as Markdown."""
        md = f"# {report.get('report_type', 'SECURITY')} Report\n\n"
        md += f"**Report ID:** {report.get('report_id', 'N/A')}\n"
        md += f"**Generated:** {report.get('generated_at', 'N/A')}\n\n"
        
        # Executive Summary
        if "executive_summary" in report:
            md += "## Executive Summary\n\n"
            summary = report["executive_summary"]
            for key, value in summary.items():
                if isinstance(value, list):
                    md += f"### {key.replace('_', ' ').title()}\n"
                    for item in value:
                        md += f"- {item}\n"
                else:
                    md += f"**{key.replace('_', ' ').title()}:** {value}\n"
            md += "\n"
        
        # Findings
        if "findings" in report:
            md += "## Findings\n\n"
            for i, finding in enumerate(report["findings"], 1):
                md += f"### Finding {i}\n"
                if isinstance(finding, dict):
                    for key, value in finding.items():
                        md += f"**{key.replace('_', ' ').title()}:** {value}\n"
                else:
                    md += f"{finding}\n"
                md += "\n"
        
        # Recommendations
        if "recommendations" in report:
            md += "## Recommendations\n\n"
            recs = report["recommendations"]
            if isinstance(recs, dict):
                for category, items in recs.items():
                    md += f"### {category.replace('_', ' ').title()}\n"
                    if isinstance(items, list):
                        for item in items:
                            md += f"- {item}\n"
                    else:
                        md += f"{items}\n"
                    md += "\n"
            elif isinstance(recs, list):
                for item in recs:
                    md += f"- {item}\n"
                md += "\n"
        
        return md
    
    def _generate_signatures(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate digital signatures for report integrity."""
        data_str = json.dumps(data, sort_keys=True, default=str)
        
        return {
            "md5": hashlib.md5(data_str.encode()).hexdigest(),
            "sha256": hashlib.sha256(data_str.encode()).hexdigest(),
            "generated_at": datetime.now().isoformat()
        }


def main():
    """Main entry point for sandbox execution."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: report_generator.py <command> [data_file]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    data_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    generator = ReportGenerator()
    
    # Load data if provided
    data = {}
    if data_file and os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    
    # Generate report based on command
    if command == "incident":
        report = generator.generate_incident_report(data)
    elif command == "forensic":
        report = generator.generate_forensic_report(data)
    elif command == "threat":
        report = generator.generate_threat_report(data)
    elif command == "executive":
        report = generator.generate_executive_summary(data)
    else:
        report = {"error": f"Unknown command: {command}"}
    
    # Output as JSON
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
