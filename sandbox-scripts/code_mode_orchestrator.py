#!/usr/bin/env python3
"""
AutoVault Code Mode Orchestrator — Chains multiple MCP calls in single execution.

This script demonstrates TrueForge's Code Mode capability:
- Chain multiple tool calls together
- Aggregate results from different sources
- Generate comprehensive analysis in one execution
- Offload complex orchestration to sandbox
"""

import os
import sys
import json
import hashlib
import math
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp-server'))


class CodeModeOrchestrator:
    """
    Code Mode Orchestrator — Chains multiple MCP tool calls.
    
    This demonstrates TrueForge's Code Mode where a single sandbox script
    can orchestrate multiple tool calls, aggregate results, and produce
    a comprehensive analysis.
    """
    
    def __init__(self):
        self.execution_log = []
        self.tool_results = {}
        self.execution_id = f"CM-{int(time.time())}"
        
    def log_execution(self, tool: str, status: str, duration: float = 0):
        """Log tool execution."""
        self.execution_log.append({
            "tool": tool,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
    
    def execute_parallel(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple tools in parallel."""
        results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for tool in tools:
                future = executor.submit(self._execute_tool, tool)
                futures[future] = tool["name"]
            
            for future in as_completed(futures):
                tool_name = futures[future]
                try:
                    result = future.result(timeout=30)
                    results[tool_name] = result
                except Exception as e:
                    results[tool_name] = {"error": str(e)}
        
        return results
    
    def _execute_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single tool (simulated for sandbox)."""
        start_time = time.time()
        tool_name = tool["name"]
        
        try:
            # Simulate tool execution based on name
            if tool_name == "scan_directory":
                result = self._scan_directory(tool.get("args", {}).get("directory", "./test_vault"))
            elif tool_name == "analyze_threat":
                result = self._analyze_threat(tool.get("args", {}))
            elif tool_name == "get_network_connections":
                result = self._get_network_connections()
            elif tool_name == "analyze_file_deep":
                result = self._analyze_file(tool.get("args", {}).get("filepath", ""))
            elif tool_name == "build_timeline":
                result = self._build_timeline(tool.get("args", {}).get("directory", "./test_vault"))
            elif tool_name == "detect_ransomware":
                result = self._detect_ransomware(tool.get("args", {}).get("directory", "./test_vault"))
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            duration = time.time() - start_time
            self.log_execution(tool_name, "success", duration)
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_execution(tool_name, "error", duration)
            return {"error": str(e)}
    
    def _scan_directory(self, directory: str) -> Dict[str, Any]:
        """Scan directory for ransomware indicators."""
        results = {
            "directory": directory,
            "total_files": 0,
            "high_entropy_files": [],
            "suspicious_extensions": [],
            "recently_modified": []
        }
        
        suspicious_exts = {'.locked', '.encrypted', '.enc', '.crypto'}
        now = time.time()
        
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    results["total_files"] += 1
                    stat = entry.stat()
                    
                    # Check entropy
                    entropy = self._calculate_entropy(entry.path)
                    if entropy > 7.5:
                        results["high_entropy_files"].append({
                            "name": entry.name,
                            "entropy": round(entropy, 2)
                        })
                    
                    # Check extensions
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() in suspicious_exts:
                        results["suspicious_extensions"].append(entry.name)
                    
                    # Check recent modifications
                    if now - stat.st_mtime < 300:
                        results["recently_modified"].append(entry.name)
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def _analyze_threat(self, args: Dict) -> Dict[str, Any]:
        """Analyze threat using ML model."""
        # Simulate ML analysis
        return {
            "anomaly_score": -0.15,
            "is_threat": True,
            "threat_level": "HIGH",
            "confidence": 85.5,
            "features": {
                "entropy": args.get("entropy", 7.8),
                "io_velocity": args.get("io_velocity", 150),
                "extension_churn": args.get("extension_churn", 5)
            }
        }
    
    def _get_network_connections(self) -> Dict[str, Any]:
        """Get network connections (simulated)."""
        return {
            "total_connections": 47,
            "established": 12,
            "listening": 8,
            "suspicious": [
                {"remote_ip": "185.220.101.45", "port": 4444, "process": "unknown"},
                {"remote_ip": "91.215.85.142", "port": 6666, "process": "python"}
            ],
            "risk_score": 65
        }
    
    def _analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a file deeply."""
        if not filepath or not os.path.exists(filepath):
            return {"error": "File not found"}
        
        entropy = self._calculate_entropy(filepath)
        stat = os.stat(filepath)
        
        return {
            "filepath": filepath,
            "size": stat.st_size,
            "entropy": round(entropy, 4),
            "classification": "ENCRYPTED" if entropy > 7.5 else "NORMAL",
            "hashes": {
                "md5": hashlib.md5(f"simulated-{filepath}".encode()).hexdigest(),
                "sha256": hashlib.sha256(f"simulated-{filepath}".encode()).hexdigest()
            }
        }
    
    def _build_timeline(self, directory: str) -> Dict[str, Any]:
        """Build file modification timeline."""
        timeline = []
        
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    stat = entry.stat()
                    timeline.append({
                        "filename": entry.name,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "size": stat.st_size,
                        "entropy": round(self._calculate_entropy(entry.path), 2)
                    })
            
            timeline.sort(key=lambda x: x["modified"])
        except Exception as e:
            timeline.append({"error": str(e)})
        
        return {"timeline": timeline, "total_events": len(timeline)}
    
    def _detect_ransomware(self, directory: str) -> Dict[str, Any]:
        """Detect ransomware indicators."""
        scan = self._scan_directory(directory)
        
        indicators = {
            "encrypted_files": len(scan.get("high_entropy_files", [])),
            "suspicious_extensions": len(scan.get("suspicious_extensions", [])),
            "mass_modifications": len(scan.get("recently_modified", [])) > 5,
            "risk_score": 0,
            "risk_level": "LOW"
        }
        
        # Calculate risk score
        indicators["risk_score"] = (
            indicators["encrypted_files"] * 20 +
            indicators["suspicious_extensions"] * 25 +
            (30 if indicators["mass_modifications"] else 0)
        )
        
        if indicators["risk_score"] >= 75:
            indicators["risk_level"] = "CRITICAL"
        elif indicators["risk_score"] >= 50:
            indicators["risk_level"] = "HIGH"
        elif indicators["risk_score"] >= 25:
            indicators["risk_level"] = "MEDIUM"
        
        return indicators
    
    def _calculate_entropy(self, filepath: str) -> float:
        """Calculate file entropy."""
        try:
            with open(filepath, 'rb') as f:
                data = f.read(8192)  # Read first 8KB
                if not data:
                    return 0.0
                byte_freq = {}
                for byte in data:
                    byte_freq[byte] = byte_freq.get(byte, 0) + 1
                length = len(data)
                return -sum((count / length) * math.log2(count / length) 
                           for count in byte_freq.values())
        except Exception:
            return 0.0
    
    def orchestrate_full_analysis(self, directory: str = "./test_vault") -> Dict[str, Any]:
        """
        Code Mode: Chain multiple tool calls in single execution.
        
        This demonstrates TrueForge's Code Mode where a single sandbox
        script orchestrates multiple tool calls, aggregates results,
        and produces comprehensive analysis.
        """
        start_time = time.time()
        
        print(f"🔍 Code Mode Orchestrator — Execution {self.execution_id}")
        print(f"   Directory: {directory}")
        print()
        
        # Step 1: Parallel execution of independent tools
        print("  Step 1: Parallel Tool Execution")
        parallel_tools = [
            {"name": "scan_directory", "args": {"directory": directory}},
            {"name": "get_network_connections", "args": {}},
            {"name": "build_timeline", "args": {"directory": directory}},
            {"name": "detect_ransomware", "args": {"directory": directory}}
        ]
        
        parallel_results = self.execute_parallel(parallel_tools)
        
        for tool_name, result in parallel_results.items():
            status = "✓" if "error" not in result else "✗"
            print(f"    {status} {tool_name}")
        
        print()
        
        # Step 2: Analyze threat based on scan results
        print("  Step 2: Threat Analysis")
        scan_result = parallel_results.get("scan_directory", {})
        high_entropy = len(scan_result.get("high_entropy_files", []))
        suspicious_exts = len(scan_result.get("suspicious_extensions", []))
        
        threat_result = self._execute_tool({
            "name": "analyze_threat",
            "args": {
                "entropy": 7.8 if high_entropy > 0 else 3.5,
                "io_velocity": 150 if len(scan_result.get("recently_modified", [])) > 5 else 10,
                "extension_churn": suspicious_exts
            }
        })
        print(f"    ✓ Threat analysis complete: {threat_result.get('threat_level', 'UNKNOWN')}")
        
        # Step 3: Deep file analysis if threats found
        print("  Step 3: Deep File Analysis")
        deep_results = []
        if high_entropy > 0:
            for file_info in scan_result.get("high_entropy_files", [])[:3]:
                filepath = os.path.join(directory, file_info["name"])
                deep_result = self._execute_tool({
                    "name": "analyze_file_deep",
                    "args": {"filepath": filepath}
                })
                deep_results.append(deep_result)
                print(f"    ✓ Analyzed: {file_info['name']}")
        
        print()
        
        # Step 4: Aggregate all results
        print("  Step 4: Result Aggregation")
        
        total_duration = time.time() - start_time
        
        aggregated_result = {
            "execution_id": self.execution_id,
            "timestamp": datetime.now().isoformat(),
            "directory": directory,
            "duration_seconds": round(total_duration, 2),
            
            "parallel_results": parallel_results,
            "threat_analysis": threat_result,
            "deep_file_analysis": deep_results,
            
            "summary": {
                "total_files_scanned": scan_result.get("total_files", 0),
                "high_entropy_files": high_entropy,
                "suspicious_extensions": suspicious_exts,
                "recent_modifications": len(scan_result.get("recently_modified", [])),
                "network_suspicious": len(parallel_results.get("get_network_connections", {}).get("suspicious", [])),
                "threat_level": threat_result.get("threat_level", "UNKNOWN"),
                "anomaly_score": threat_result.get("anomaly_score", 0),
                "ransomware_risk": parallel_results.get("detect_ransomware", {}).get("risk_level", "UNKNOWN")
            },
            
            "execution_log": self.execution_log,
            "tools_executed": len(self.execution_log),
            "parallel_executions": len(parallel_tools)
        }
        
        print(f"    ✓ {len(self.execution_log)} tools executed")
        print(f"    ✓ {len(parallel_tools)} parallel executions")
        print(f"    ✓ Total duration: {total_duration:.2f}s")
        print()
        
        return aggregated_result


def main():
    """Main entry point for Code Mode execution."""
    if len(sys.argv) < 2:
        directory = "./test_vault"
    else:
        directory = sys.argv[1]
    
    orchestrator = CodeModeOrchestrator()
    result = orchestrator.orchestrate_full_analysis(directory)
    
    # Output as JSON
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
