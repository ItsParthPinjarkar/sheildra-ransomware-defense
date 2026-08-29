#!/usr/bin/env python3
"""
AutoVault Generative UI — Interactive components for TrueForge.

This script generates interactive UI components:
- Threat cards with severity indicators
- Forensics dashboards with charts
- Approval forms with risk assessment
- Real-time status displays
- Interactive investigation panels
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional


class GenerativeUI:
    """Generate interactive UI components for TrueForge."""
    
    def __init__(self):
        self.component_count = 0
    
    def create_threat_card(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive threat card component."""
        self.component_count += 1
        
        severity = threat_data.get("severity", "LOW")
        severity_colors = {
            "CRITICAL": {"bg": "#ff3366", "text": "#ffffff", "border": "#ff0040"},
            "HIGH": {"bg": "#ff6600", "text": "#ffffff", "border": "#ff4400"},
            "MEDIUM": {"bg": "#ffcc00", "text": "#000000", "border": "#ffaa00"},
            "LOW": {"bg": "#00ffaa", "text": "#000000", "border": "#00cc88"}
        }
        
        colors = severity_colors.get(severity, severity_colors["LOW"])
        
        component = {
            "type": "threat_card",
            "id": f"threat-card-{self.component_count}",
            "title": f"🚨 Threat Detected — {severity}",
            "severity": severity,
            "colors": colors,
            "data": {
                "threat_level": threat_data.get("threat_level", "UNKNOWN"),
                "risk_score": threat_data.get("risk_score", 0),
                "affected_files": threat_data.get("affected_files", 0),
                "detected_at": threat_data.get("detected_at", datetime.now().isoformat()),
                "indicators": threat_data.get("indicators", []),
                "mitre_techniques": threat_data.get("mitre", [])
            },
            "actions": [
                {"label": "Investigate", "action": "investigate", "style": "primary"},
                {"label": "Isolate", "action": "isolate", "style": "danger"},
                {"label": "Dismiss", "action": "dismiss", "style": "secondary"}
            ],
            "interactive": True,
            "refresh_interval": 5000
        }
        
        return component
    
    def create_forensics_dashboard(self, forensics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive forensics dashboard."""
        self.component_count += 1
        
        component = {
            "type": "forensics_dashboard",
            "id": f"forensics-dash-{self.component_count}",
            "title": "🔬 Forensic Analysis Dashboard",
            "layout": "grid",
            "panels": [
                {
                    "type": "timeline",
                    "title": "Attack Timeline",
                    "data": forensics_data.get("timeline", []),
                    "interactive": True
                },
                {
                    "type": "entropy_chart",
                    "title": "Entropy Distribution",
                    "data": forensics_data.get("entropy_distribution", {}),
                    "chart_type": "bar"
                },
                {
                    "type": "file_list",
                    "title": "Affected Files",
                    "data": forensics_data.get("affected_files", []),
                    "sortable": True,
                    "filterable": True
                },
                {
                    "type": "network_map",
                    "title": "Network Connections",
                    "data": forensics_data.get("network_connections", []),
                    "visualization": "graph"
                }
            ],
            "summary": {
                "total_files": forensics_data.get("total_files", 0),
                "encrypted_files": forensics_data.get("encrypted_files", 0),
                "attack_duration": forensics_data.get("attack_duration", "Unknown"),
                "indicators_found": forensics_data.get("indicators_count", 0)
            }
        }
        
        return component
    
    def create_approval_form(self, approval_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive approval form."""
        self.component_count += 1
        
        severity = approval_data.get("severity", "P3")
        severity_styles = {
            "P1": {"bg": "#ff3366", "pulse": True, "urgent": True},
            "P2": {"bg": "#ff6600", "pulse": True, "urgent": True},
            "P3": {"bg": "#ffcc00", "pulse": False, "urgent": False},
            "P4": {"bg": "#00ffaa", "pulse": False, "urgent": False}
        }
        
        component = {
            "type": "approval_form",
            "id": f"approval-{self.component_count}",
            "title": f"🔐 Approval Required — {severity}",
            "severity": severity,
            "style": severity_styles.get(severity, severity_styles["P3"]),
            "data": {
                "action": approval_data.get("action", "Unknown Action"),
                "description": approval_data.get("description", ""),
                "justification": approval_data.get("justification", ""),
                "risk_assessment": approval_data.get("risk_assessment", {}),
                "timeout": approval_data.get("timeout", 300),
                "auto_deny": approval_data.get("auto_deny", False)
            },
            "form": {
                "fields": [
                    {
                        "name": "decision",
                        "type": "select",
                        "options": ["Approve", "Deny", "Defer"],
                        "required": True
                    },
                    {
                        "name": "reason",
                        "type": "textarea",
                        "placeholder": "Provide reason for your decision...",
                        "required": False
                    }
                ],
                "submit_label": "Submit Decision"
            },
            "risk_meter": {
                "value": approval_data.get("risk_score", 50),
                "max": 100,
                "thresholds": [
                    {"value": 25, "label": "Low Risk", "color": "#00ffaa"},
                    {"value": 50, "label": "Medium Risk", "color": "#ffcc00"},
                    {"value": 75, "label": "High Risk", "color": "#ff6600"},
                    {"value": 100, "label": "Critical Risk", "color": "#ff3366"}
                ]
            }
        }
        
        return component
    
    def create_status_display(self, status_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a real-time status display."""
        self.component_count += 1
        
        component = {
            "type": "status_display",
            "id": f"status-{self.component_count}",
            "title": "📊 System Status",
            "layout": "cards",
            "cards": [
                {
                    "label": "Threat Level",
                    "value": status_data.get("threat_level", "NORMAL"),
                    "icon": "🛡️",
                    "color": self._get_threat_color(status_data.get("threat_level", "NORMAL"))
                },
                {
                    "label": "Active Alerts",
                    "value": status_data.get("active_alerts", 0),
                    "icon": "⚠️",
                    "color": "#ffcc00"
                },
                {
                    "label": "Files Monitored",
                    "value": status_data.get("files_monitored", 0),
                    "icon": "📁",
                    "color": "#00e5ff"
                },
                {
                    "label": "Network Connections",
                    "value": status_data.get("network_connections", 0),
                    "icon": "🌐",
                    "color": "#00ffaa"
                },
                {
                    "label": "Uptime",
                    "value": status_data.get("uptime", "0h 0m"),
                    "icon": "⏱️",
                    "color": "#7a889b"
                },
                {
                    "label": "Last Scan",
                    "value": status_data.get("last_scan", "Never"),
                    "icon": "🔍",
                    "color": "#00e5ff"
                }
            ],
            "refresh_interval": 2000
        }
        
        return component
    
    def create_investigation_panel(self, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive investigation panel."""
        self.component_count += 1
        
        component = {
            "type": "investigation_panel",
            "id": f"investigation-{self.component_count}",
            "title": "🔍 Investigation Panel",
            "tabs": [
                {
                    "name": "Overview",
                    "content": {
                        "type": "summary",
                        "data": investigation_data.get("summary", {})
                    }
                },
                {
                    "name": "Timeline",
                    "content": {
                        "type": "timeline",
                        "data": investigation_data.get("timeline", [])
                    }
                },
                {
                    "name": "IOCs",
                    "content": {
                        "type": "ioc_list",
                        "data": investigation_data.get("iocs", [])
                    }
                },
                {
                    "name": "Network",
                    "content": {
                        "type": "network_graph",
                        "data": investigation_data.get("network", {})
                    }
                },
                {
                    "name": "Files",
                    "content": {
                        "type": "file_tree",
                        "data": investigation_data.get("files", [])
                    }
                }
            ],
            "actions": [
                {"label": "Export Report", "action": "export", "style": "primary"},
                {"label": "Share Findings", "action": "share", "style": "secondary"},
                {"label": "Create Ticket", "action": "ticket", "style": "secondary"}
            ]
        }
        
        return component
    
    def create_playbook_executor(self, playbook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a playbook execution interface."""
        self.component_count += 1
        
        steps = playbook_data.get("steps", [])
        completed_steps = playbook_data.get("completed_steps", [])
        
        component = {
            "type": "playbook_executor",
            "id": f"playbook-{self.component_count}",
            "title": f"📋 Playbook: {playbook_data.get('name', 'Incident Response')}",
            "status": playbook_data.get("status", "running"),
            "progress": {
                "total": len(steps),
                "completed": len(completed_steps),
                "percent": int((len(completed_steps) / max(len(steps), 1)) * 100)
            },
            "steps": [
                {
                    "name": step.get("name", f"Step {i+1}"),
                    "status": "completed" if i in completed_steps else "pending",
                    "description": step.get("description", ""),
                    "tools_used": step.get("tools", []),
                    "duration": step.get("duration", None)
                }
                for i, step in enumerate(steps)
            ],
            "controls": {
                "pause": playbook_data.get("status") == "running",
                "resume": playbook_data.get("status") == "paused",
                "abort": True
            }
        }
        
        return component
    
    def create_threat_heatmap(self, heatmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a threat heatmap visualization."""
        self.component_count += 1
        
        component = {
            "type": "threat_heatmap",
            "id": f"heatmap-{self.component_count}",
            "title": "🗺️ Threat Heatmap",
            "data": heatmap_data.get("data", []),
            "color_scale": [
                {"min": 0, "max": 25, "color": "#00ffaa", "label": "Safe"},
                {"min": 25, "max": 50, "color": "#ffcc00", "label": "Warning"},
                {"min": 50, "max": 75, "color": "#ff6600", "label": "Danger"},
                {"min": 75, "max": 100, "color": "#ff3366", "label": "Critical"}
            ],
            "interactive": True,
            "zoom": True
        }
        
        return component
    
    def create_agent_communication(self, comm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create agent-to-agent communication visualization."""
        self.component_count += 1
        
        component = {
            "type": "agent_communication",
            "id": f"comm-{self.component_count}",
            "title": "🤖 Agent Communication",
            "agents": comm_data.get("agents", []),
            "messages": comm_data.get("messages", []),
            "visualization": "flow",
            "interactive": True
        }
        
        return component
    
    def _get_threat_color(self, threat_level: str) -> str:
        """Get color for threat level."""
        colors = {
            "CRITICAL": "#ff3366",
            "HIGH": "#ff6600",
            "MEDIUM": "#ffcc00",
            "LOW": "#00ffaa",
            "NORMAL": "#00e5ff"
        }
        return colors.get(threat_level, "#7a889b")


def main():
    """Generate all UI components."""
    ui = GenerativeUI()
    
    # Generate example components
    components = []
    
    # Threat card
    components.append(ui.create_threat_card({
        "severity": "CRITICAL",
        "threat_level": "RANSOMWARE",
        "risk_score": 85,
        "affected_files": 15,
        "indicators": ["High entropy files", "Suspicious extensions", "Ransom note"],
        "mitre": ["T1486", "T1489"]
    }))
    
    # Forensics dashboard
    components.append(ui.create_forensics_dashboard({
        "total_files": 47,
        "encrypted_files": 15,
        "attack_duration": "2m 34s",
        "indicators_count": 8,
        "timeline": [
            {"time": "14:32:15", "event": "Attack started"},
            {"time": "14:32:45", "event": "Encryption detected"},
            {"time": "14:33:00", "event": "Lockdown triggered"}
        ]
    }))
    
    # Approval form
    components.append(ui.create_approval_form({
        "severity": "P1",
        "action": "Execute Lockdown",
        "description": "Suspend processes and block network",
        "risk_score": 85,
        "timeout": 30,
        "auto_deny": False
    }))
    
    # Status display
    components.append(ui.create_status_display({
        "threat_level": "HIGH",
        "active_alerts": 3,
        "files_monitored": 1247,
        "network_connections": 47,
        "uptime": "2h 15m",
        "last_scan": "30s ago"
    }))
    
    # Investigation panel
    components.append(ui.create_investigation_panel({
        "summary": {"findings": 8, "risk": "HIGH"},
        "timeline": [{"time": "14:32", "event": "Attack detected"}],
        "iocs": [{"type": "file", "hash": "abc123"}],
        "network": {"nodes": 5, "edges": 8}
    }))
    
    # Playbook executor
    components.append(ui.create_playbook_executor({
        "name": "Ransomware Response",
        "status": "running",
        "steps": [
            {"name": "Detect", "description": "Identify threat"},
            {"name": "Contain", "description": "Isolate systems"},
            {"name": "Eradicate", "description": "Remove threat"},
            {"name": "Recover", "description": "Restore systems"}
        ],
        "completed_steps": [0, 1]
    }))
    
    # Threat heatmap
    components.append(ui.create_threat_heatmap({
        "data": [
            {"x": 0, "y": 0, "value": 25},
            {"x": 1, "y": 0, "value": 50},
            {"x": 2, "y": 0, "value": 85},
            {"x": 0, "y": 1, "value": 30},
            {"x": 1, "y": 1, "value": 60},
            {"x": 2, "y": 1, "value": 90}
        ]
    }))
    
    # Agent communication
    components.append(ui.create_agent_communication({
        "agents": [
            {"name": "process-investigator", "status": "active"},
            {"name": "network-analyzer", "status": "active"},
            {"name": "forensics-analyst", "status": "idle"}
        ],
        "messages": [
            {"from": "process-investigator", "to": "network-analyzer", "message": "Found suspicious PID"},
            {"from": "network-analyzer", "to": "forensics-analyst", "message": "C2 connection detected"}
        ]
    }))
    
    # Output all components
    result = {
        "total_components": len(components),
        "components": components,
        "generated_at": datetime.now().isoformat()
    }
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
