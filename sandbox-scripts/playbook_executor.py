#!/usr/bin/env python3
"""
AutoVault Playbook Executor — Automated incident response playbooks.

This script demonstrates TrueForge's automated response capabilities:
- Predefined response playbooks
- Step-by-step execution
- Conditional branching
- Tool orchestration
- Approval checkpoints
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class PlaybookStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


@dataclass
class PlaybookStep:
    id: str
    name: str
    description: str
    action: str
    tools: List[str]
    requires_approval: bool
    approval_message: str
    conditions: Dict[str, Any]
    next_step_success: Optional[str]
    next_step_failure: Optional[str]


class PlaybookExecutor:
    """
    Playbook Executor — TrueForge automated response.
    
    Demonstrates:
    - Predefined response playbooks
    - Step-by-step execution
    - Conditional branching
    - Tool orchestration
    - Approval checkpoints
    """
    
    def __init__(self):
        self.playbooks = {}
        self.execution_history = []
        self.current_playbook = None
        self.current_step = None
        self.execution_id = f"PE-{int(time.time())}"
        
        # Register built-in playbooks
        self._register_playbooks()
    
    def _register_playbooks(self):
        """Register built-in incident response playbooks."""
        
        # Ransomware Response Playbook
        self.playbooks["ransomware_response"] = {
            "name": "Ransomware Response",
            "description": "Automated response to ransomware attacks",
            "severity_levels": ["CRITICAL", "HIGH"],
            "steps": [
                PlaybookStep(
                    id="detect",
                    name="Detection",
                    description="Confirm ransomware activity",
                    action="analyze_threat",
                    tools=["scan_directory", "analyze_threat"],
                    requires_approval=False,
                    approval_message="",
                    conditions={"threat_level": ["CRITICAL", "HIGH"]},
                    next_step_success="contain",
                    next_step_failure="monitor"
                ),
                PlaybookStep(
                    id="contain",
                    name="Containment",
                    description="Isolate affected systems",
                    action="isolate_system",
                    tools=["create_snapshot", "block_network"],
                    requires_approval=True,
                    approval_message="Approve system isolation?",
                    conditions={},
                    next_step_success="eradicate",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="eradicate",
                    name="Eradication",
                    description="Remove threat from systems",
                    action="remove_threat",
                    tools=["investigate_process", "terminate_process"],
                    requires_approval=True,
                    approval_message="Approve threat removal?",
                    conditions={},
                    next_step_success="recover",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="recover",
                    name="Recovery",
                    description="Restore systems from backup",
                    action="restore_systems",
                    tools=["restore_files", "verify_integrity"],
                    requires_approval=True,
                    approval_message="Approve system restoration?",
                    conditions={},
                    next_step_success="verify",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="verify",
                    name="Verification",
                    description="Verify system integrity",
                    action="verify_systems",
                    tools=["scan_directory", "analyze_network"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success="document",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="document",
                    name="Documentation",
                    description="Document incident and actions taken",
                    action="document_incident",
                    tools=["generate_forensic_report", "generate_threat_report"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success=None,
                    next_step_failure=None
                )
            ]
        }
        
        # Data Breach Response Playbook
        self.playbooks["data_breach_response"] = {
            "name": "Data Breach Response",
            "description": "Automated response to data breaches",
            "severity_levels": ["CRITICAL", "HIGH", "MEDIUM"],
            "steps": [
                PlaybookStep(
                    id="detect",
                    name="Detection",
                    description="Confirm data breach activity",
                    action="analyze_breach",
                    tools=["scan_directory", "analyze_network"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success="contain",
                    next_step_failure="monitor"
                ),
                PlaybookStep(
                    id="contain",
                    name="Containment",
                    description="Isolate compromised systems",
                    action="isolate_compromised",
                    tools=["block_network", "create_snapshot"],
                    requires_approval=True,
                    approval_message="Approve containment?",
                    conditions={},
                    next_step_success="investigate",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="investigate",
                    name="Investigation",
                    description="Investigate breach scope",
                    action="investigate_breach",
                    tools=["analyze_file_deep", "build_timeline"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success="notify",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="notify",
                    name="Notification",
                    description="Notify stakeholders",
                    action="send_notifications",
                    tools=["generate_forensic_report"],
                    requires_approval=True,
                    approval_message="Approve notifications?",
                    conditions={},
                    next_step_success="remediate",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="remediate",
                    name="Remediation",
                    description="Remediate affected systems",
                    action="remediate_systems",
                    tools=["restore_files", "verify_integrity"],
                    requires_approval=True,
                    approval_message="Approve remediation?",
                    conditions={},
                    next_step_success="document",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="document",
                    name="Documentation",
                    description="Document breach and response",
                    action="document_breach",
                    tools=["generate_forensic_report", "generate_threat_report"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success=None,
                    next_step_failure=None
                )
            ]
        }
        
        # Malware Response Playbook
        self.playbooks["malware_response"] = {
            "name": "Malware Response",
            "description": "Automated response to malware infections",
            "severity_levels": ["HIGH", "MEDIUM"],
            "steps": [
                PlaybookStep(
                    id="detect",
                    name="Detection",
                    description="Confirm malware presence",
                    action="analyze_malware",
                    tools=["analyze_file_iocs", "detect_ransomware"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success="quarantine",
                    next_step_failure="monitor"
                ),
                PlaybookStep(
                    id="quarantine",
                    name="Quarantine",
                    description="Isolate infected systems",
                    action="quarantine_system",
                    tools=["block_network", "create_snapshot"],
                    requires_approval=True,
                    approval_message="Approve quarantine?",
                    conditions={},
                    next_step_success="analyze",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="analyze",
                    name="Analysis",
                    description="Analyze malware behavior",
                    action="analyze_behavior",
                    tools=["analyze_file_deep", "build_timeline"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success="remove",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="remove",
                    name="Removal",
                    description="Remove malware from systems",
                    action="remove_malware",
                    tools=["investigate_process", "terminate_process"],
                    requires_approval=True,
                    approval_message="Approve malware removal?",
                    conditions={},
                    next_step_success="verify",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="verify",
                    name="Verification",
                    description="Verify system cleanliness",
                    action="verify_clean",
                    tools=["scan_directory", "analyze_network"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success="document",
                    next_step_failure="escalate"
                ),
                PlaybookStep(
                    id="document",
                    name="Documentation",
                    description="Document malware incident",
                    action="document_malware",
                    tools=["generate_forensic_report"],
                    requires_approval=False,
                    approval_message="",
                    conditions={},
                    next_step_success=None,
                    next_step_failure=None
                )
            ]
        }
    
    def get_available_playbooks(self) -> List[Dict[str, Any]]:
        """Get list of available playbooks."""
        return [
            {
                "id": playbook_id,
                "name": playbook["name"],
                "description": playbook["description"],
                "severity_levels": playbook["severity_levels"],
                "step_count": len(playbook["steps"])
            }
            for playbook_id, playbook in self.playbooks.items()
        ]
    
    def start_playbook(self, playbook_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Start executing a playbook."""
        if playbook_id not in self.playbooks:
            return {"error": f"Playbook not found: {playbook_id}"}
        
        playbook = self.playbooks[playbook_id]
        
        self.current_playbook = {
            "id": playbook_id,
            "name": playbook["name"],
            "status": PlaybookStatus.RUNNING,
            "context": context,
            "started_at": datetime.now().isoformat(),
            "current_step": playbook["steps"][0].id if playbook["steps"] else None,
            "completed_steps": [],
            "execution_log": []
        }
        
        print(f"📋 Starting Playbook: {playbook['name']}")
        print(f"   Context: {json.dumps(context, indent=2)}")
        print()
        
        return {
            "success": True,
            "playbook_id": playbook_id,
            "execution_id": self.execution_id,
            "status": "running",
            "first_step": playbook["steps"][0].id if playbook["steps"] else None
        }
    
    async def execute_step(self, step_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single playbook step."""
        if not self.current_playbook:
            return {"error": "No playbook running"}
        
        playbook = self.playbooks[self.current_playbook["id"]]
        
        # Find the step
        step = None
        for s in playbook["steps"]:
            if s.id == step_id:
                step = s
                break
        
        if not step:
            return {"error": f"Step not found: {step_id}"}
        
        print(f"  🔧 Executing Step: {step.name}")
        print(f"     Description: {step.description}")
        print(f"     Action: {step.action}")
        print(f"     Tools: {', '.join(step.tools)}")
        
        # Check if approval is required
        if step.requires_approval:
            print(f"     ⏳ Approval required: {step.approval_message}")
            self.current_playbook["status"] = PlaybookStatus.WAITING_APPROVAL
            self.current_step = step.id
            
            return {
                "success": True,
                "step_id": step.id,
                "status": "waiting_approval",
                "approval_message": step.approval_message,
                "tools": step.tools
            }
        
        # Execute the step
        result = await self._execute_step_action(step, context)
        
        # Log execution
        self.current_playbook["execution_log"].append({
            "step": step.id,
            "action": step.action,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update status
        self.current_playbook["completed_steps"].append(step.id)
        
        # Determine next step
        next_step = None
        if result.get("success", False):
            next_step = step.next_step_success
        else:
            next_step = step.next_step_failure
        
        if next_step:
            self.current_playbook["current_step"] = next_step
            print(f"     ✓ Step completed. Next: {next_step}")
        else:
            self.current_playbook["status"] = PlaybookStatus.COMPLETED
            print(f"     ✓ Playbook completed!")
        
        return {
            "success": True,
            "step_id": step.id,
            "status": "completed",
            "result": result,
            "next_step": next_step
        }
    
    async def _execute_step_action(self, step: PlaybookStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute step action (simulated)."""
        # Simulate execution based on action type
        await asyncio.sleep(0.3)  # Simulate work
        
        results = {
            "analyze_threat": {"threat_level": "HIGH", "anomaly_score": -0.25},
            "create_snapshot": {"cid": f"Qm{int(time.time())}", "success": True},
            "block_network": {"success": True, "connections_blocked": 12},
            "investigate_process": {"findings": ["Suspicious process detected"], "risk": "HIGH"},
            "terminate_process": {"success": True, "pid": 4920},
            "restore_files": {"success": True, "files_restored": 15},
            "verify_integrity": {"success": True, "integrity_check": "PASSED"},
            "generate_forensic_report": {"report_id": f"FR-{int(time.time())}", "success": True},
            "generate_threat_report": {"report_id": f"TR-{int(time.time())}", "success": True},
            "analyze_file_deep": {"classification": "MALICIOUS", "confidence": 0.95},
            "build_timeline": {"events": 8, "timeline_built": True},
            "analyze_network": {"suspicious_connections": 3, "analysis_complete": True},
            "detect_ransomware": {"detected": True, "risk_score": 85},
            "analyze_file_iocs": {"iocs_found": 5, "analysis_complete": True}
        }
        
        # Execute each tool in the step
        tool_results = {}
        for tool in step.tools:
            tool_results[tool] = results.get(tool, {"success": True})
        
        return {
            "success": True,
            "tool_results": tool_results,
            "duration": 0.3
        }
    
    def approve_step(self, step_id: str, approved: bool) -> Dict[str, Any]:
        """Approve or deny a step."""
        if not self.current_playbook:
            return {"error": "No playbook running"}
        
        if self.current_playbook["status"] != PlaybookStatus.WAITING_APPROVAL:
            return {"error": "No step waiting for approval"}
        
        if approved:
            print(f"     ✅ Step approved: {step_id}")
            self.current_playbook["status"] = PlaybookStatus.RUNNING
        else:
            print(f"     ❌ Step denied: {step_id}")
            self.current_playbook["status"] = PlaybookStatus.ABORTED
        
        return {
            "success": True,
            "step_id": step_id,
            "approved": approved,
            "status": self.current_playbook["status"].value
        }
    
    def get_playbook_status(self) -> Dict[str, Any]:
        """Get current playbook status."""
        if not self.current_playbook:
            return {"status": "no_playbook"}
        
        playbook = self.playbooks[self.current_playbook["id"]]
        total_steps = len(playbook["steps"])
        completed_steps = len(self.current_playbook["completed_steps"])
        
        return {
            "playbook_id": self.current_playbook["id"],
            "playbook_name": self.current_playbook["name"],
            "status": self.current_playbook["status"].value,
            "current_step": self.current_playbook["current_step"],
            "progress": {
                "total": total_steps,
                "completed": completed_steps,
                "percent": int((completed_steps / total_steps) * 100)
            },
            "started_at": self.current_playbook["started_at"],
            "execution_log": self.current_playbook["execution_log"]
        }


import asyncio

async def main():
    """Demo playbook execution."""
    executor = PlaybookExecutor()
    
    print("📋 Playbook Executor Demo")
    print()
    
    # List available playbooks
    print("Available Playbooks:")
    for playbook in executor.get_available_playbooks():
        print(f"  {playbook['id']}: {playbook['name']} ({playbook['step_count']} steps)")
    print()
    
    # Start ransomware response playbook
    result = executor.start_playbook("ransomware_response", {
        "threat_type": "ransomware",
        "severity": "CRITICAL",
        "affected_systems": ["server-01", "workstation-05"]
    })
    
    print(f"Started playbook: {result['playbook_id']}")
    print()
    
    # Execute steps
    status = executor.get_playbook_status()
    while status["status"] == "running":
        current_step = status["current_step"]
        if not current_step:
            break
        
        step_result = await executor.execute_step(current_step, {})
        
        if step_result.get("status") == "waiting_approval":
            # Auto-approve for demo
            executor.approve_step(current_step, True)
        
        status = executor.get_playbook_status()
        
        if status["status"] == "completed":
            break
    
    print()
    print("📊 Final Status:")
    final_status = executor.get_playbook_status()
    print(f"  Status: {final_status['status']}")
    print(f"  Completed: {final_status['progress']['completed']}/{final_status['progress']['total']}")
    print(f"  Progress: {final_status['progress']['percent']}%")
    print()
    
    # Output as JSON
    print(json.dumps(final_status, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
