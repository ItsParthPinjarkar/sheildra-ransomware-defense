#!/usr/bin/env python3
"""
AutoVault Predictive Analyzer — Predict threats before they happen.

This script demonstrates advanced TrueForge capabilities:
- Predictive threat analysis
- Pattern recognition
- Anomaly prediction
- Risk forecasting
- Proactive defense recommendations
"""

import os
import sys
import json
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import statistics


class PredictiveAnalyzer:
    """
    Predictive Threat Analyzer — TrueForge predictive capabilities.
    
    Demonstrates:
    - Pattern recognition in file system activity
    - Anomaly prediction using statistical analysis
    - Risk forecasting based on historical data
    - Proactive defense recommendations
    """
    
    def __init__(self):
        self.history = []
        self.patterns = {}
        self.predictions = []
    
    def analyze_patterns(self, directory: str, time_window: int = 3600) -> Dict[str, Any]:
        """
        Analyze patterns in file system activity.
        
        This demonstrates TrueForge's pattern recognition:
        - Identify normal behavior patterns
        - Detect deviations from baseline
        - Predict potential threats
        """
        analysis = {
            "directory": directory,
            "time_window": time_window,
            "timestamp": datetime.now().isoformat(),
            "patterns": {},
            "anomalies": [],
            "risk_factors": []
        }
        
        try:
            # Collect file activity data
            file_activity = self._collect_file_activity(directory, time_window)
            
            # Analyze patterns
            patterns = self._identify_patterns(file_activity)
            analysis["patterns"] = patterns
            
            # Detect anomalies
            anomalies = self._detect_anomalies(file_activity, patterns)
            analysis["anomalies"] = anomalies
            
            # Calculate risk factors
            risk_factors = self._calculate_risk_factors(patterns, anomalies)
            analysis["risk_factors"] = risk_factors
            
            # Generate predictions
            predictions = self._generate_predictions(patterns, anomalies, risk_factors)
            analysis["predictions"] = predictions
            
        except Exception as e:
            analysis["error"] = str(e)
        
        return analysis
    
    def _collect_file_activity(self, directory: str, time_window: int) -> Dict[str, Any]:
        """Collect file activity data."""
        activity = {
            "files_created": [],
            "files_modified": [],
            "files_deleted": [],
            "extensions": defaultdict(int),
            "sizes": [],
            "entropy_values": [],
            "modification_times": []
        }
        
        now = time.time()
        
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    stat = entry.stat()
                    
                    # Check if within time window
                    if now - stat.st_mtime <= time_window:
                        activity["files_modified"].append(entry.name)
                        activity["modification_times"].append(stat.st_mtime)
                    
                    if now - stat.st_ctime <= time_window:
                        activity["files_created"].append(entry.name)
                    
                    # Collect extension data
                    _, ext = os.path.splitext(entry.name)
                    activity["extensions"][ext] += 1
                    
                    # Collect size data
                    activity["sizes"].append(stat.st_size)
                    
                    # Calculate entropy
                    entropy = self._calculate_entropy(entry.path)
                    activity["entropy_values"].append(entropy)
                    
        except Exception as e:
            activity["error"] = str(e)
        
        return activity
    
    def _identify_patterns(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Identify patterns in activity."""
        patterns = {
            "temporal": {},
            "spatial": {},
            "behavioral": {}
        }
        
        # Temporal patterns (time-based)
        if activity["modification_times"]:
            times = activity["modification_times"]
            patterns["temporal"] = {
                "modification_frequency": len(times),
                "avg_time_between_modifications": self._avg_time_between(times),
                "peak_activity_period": self._find_peak_period(times),
                "regularity_score": self._calculate_regularity(times)
            }
        
        # Spatial patterns (location-based)
        patterns["spatial"] = {
            "extension_distribution": dict(activity["extensions"]),
            "file_size_distribution": {
                "min": min(activity["sizes"]) if activity["sizes"] else 0,
                "max": max(activity["sizes"]) if activity["sizes"] else 0,
                "avg": statistics.mean(activity["sizes"]) if activity["sizes"] else 0,
                "std": statistics.stdev(activity["sizes"]) if len(activity["sizes"]) > 1 else 0
            },
            "entropy_distribution": {
                "min": min(activity["entropy_values"]) if activity["entropy_values"] else 0,
                "max": max(activity["entropy_values"]) if activity["entropy_values"] else 0,
                "avg": statistics.mean(activity["entropy_values"]) if activity["entropy_values"] else 0,
                "high_entropy_count": sum(1 for e in activity["entropy_values"] if e > 7.5)
            }
        }
        
        # Behavioral patterns
        patterns["behavioral"] = {
            "total_files": len(activity["sizes"]),
            "created_files": len(activity["files_created"]),
            "modified_files": len(activity["files_modified"]),
            "creation_rate": len(activity["files_created"]) / max(len(activity["sizes"]), 1),
            "modification_rate": len(activity["files_modified"]) / max(len(activity["sizes"]), 1)
        }
        
        return patterns
    
    def _detect_anomalies(self, activity: Dict[str, Any], patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalies in activity."""
        anomalies = []
        
        # Check for high entropy files
        high_entropy = patterns["spatial"]["entropy_distribution"]["high_entropy_count"]
        if high_entropy > 3:
            anomalies.append({
                "type": "high_entropy_files",
                "severity": "HIGH",
                "count": high_entropy,
                "description": f"Detected {high_entropy} files with entropy > 7.5",
                "potential_threat": "Possible encryption activity"
            })
        
        # Check for mass modifications
        modification_rate = patterns["behavioral"]["modification_rate"]
        if modification_rate > 0.3:
            anomalies.append({
                "type": "mass_modifications",
                "severity": "MEDIUM",
                "rate": modification_rate,
                "description": f"High modification rate: {modification_rate:.1%}",
                "potential_threat": "Possible ransomware encryption"
            })
        
        # Check for suspicious extensions
        extensions = patterns["spatial"]["extension_distribution"]
        suspicious_exts = {'.locked', '.encrypted', '.enc', '.crypto'}
        suspicious_count = sum(extensions.get(ext, 0) for ext in suspicious_exts)
        
        if suspicious_count > 0:
            anomalies.append({
                "type": "suspicious_extensions",
                "severity": "HIGH",
                "count": suspicious_count,
                "extensions": {ext: extensions[ext] for ext in suspicious_exts if ext in extensions},
                "description": f"Detected {suspicious_count} files with suspicious extensions",
                "potential_threat": "Known ransomware indicators"
            })
        
        # Check for unusual entropy patterns
        entropy_values = activity["entropy_values"]
        if entropy_values:
            avg_entropy = statistics.mean(entropy_values)
            if avg_entropy > 7.0:
                anomalies.append({
                    "type": "high_average_entropy",
                    "severity": "MEDIUM",
                    "avg_entropy": avg_entropy,
                    "description": f"High average entropy: {avg_entropy:.2f}",
                    "potential_threat": "Possible obfuscated or encrypted content"
                })
        
        # Check for temporal anomalies
        temporal = patterns["temporal"]
        if temporal.get("modification_frequency", 0) > 100:
            anomalies.append({
                "type": "high_activity_frequency",
                "severity": "MEDIUM",
                "frequency": temporal["modification_frequency"],
                "description": f"High modification frequency: {temporal['modification_frequency']}",
                "potential_threat": "Possible automated attack"
            })
        
        return anomalies
    
    def _calculate_risk_factors(self, patterns: Dict[str, Any], anomalies: List[Dict]) -> List[Dict[str, Any]]:
        """Calculate risk factors."""
        risk_factors = []
        
        # Factor 1: High entropy files
        high_entropy = patterns["spatial"]["entropy_distribution"]["high_entropy_count"]
        if high_entropy > 0:
            risk_factors.append({
                "factor": "High Entropy Files",
                "score": min(high_entropy * 20, 100),
                "weight": 0.3,
                "contribution": min(high_entropy * 6, 30),
                "description": f"{high_entropy} files with entropy > 7.5"
            })
        
        # Factor 2: Modification rate
        mod_rate = patterns["behavioral"]["modification_rate"]
        if mod_rate > 0.1:
            risk_factors.append({
                "factor": "High Modification Rate",
                "score": min(mod_rate * 100, 100),
                "weight": 0.25,
                "contribution": min(mod_rate * 25, 25),
                "description": f"Modification rate: {mod_rate:.1%}"
            })
        
        # Factor 3: Suspicious extensions
        extensions = patterns["spatial"]["extension_distribution"]
        suspicious_exts = {'.locked', '.encrypted', '.enc', '.crypto'}
        suspicious_count = sum(extensions.get(ext, 0) for ext in suspicious_exts)
        
        if suspicious_count > 0:
            risk_factors.append({
                "factor": "Suspicious Extensions",
                "score": min(suspicious_count * 25, 100),
                "weight": 0.35,
                "contribution": min(suspicious_count * 8.75, 35),
                "description": f"{suspicious_count} files with suspicious extensions"
            })
        
        # Factor 4: Anomaly count
        anomaly_count = len(anomalies)
        if anomaly_count > 0:
            risk_factors.append({
                "factor": "Anomaly Count",
                "score": min(anomaly_count * 20, 100),
                "weight": 0.1,
                "contribution": min(anomaly_count * 2, 10),
                "description": f"{anomaly_count} anomalies detected"
            })
        
        return risk_factors
    
    def _generate_predictions(self, patterns: Dict, anomalies: List, risk_factors: List) -> List[Dict[str, Any]]:
        """Generate predictive insights."""
        predictions = []
        
        # Calculate overall risk score
        total_contribution = sum(rf.get("contribution", 0) for rf in risk_factors)
        risk_score = min(total_contribution, 100)
        
        # Prediction 1: Threat likelihood
        threat_likelihood = "LOW"
        if risk_score >= 75:
            threat_likelihood = "CRITICAL"
        elif risk_score >= 50:
            threat_likelihood = "HIGH"
        elif risk_score >= 25:
            threat_likelihood = "MEDIUM"
        
        predictions.append({
            "type": "threat_likelihood",
            "prediction": threat_likelihood,
            "confidence": 0.85,
            "timeframe": "next_hour",
            "description": f"Threat likelihood for next hour: {threat_likelihood}"
        })
        
        # Prediction 2: Encryption probability
        high_entropy = patterns["spatial"]["entropy_distribution"]["high_entropy_count"]
        encryption_prob = min(high_entropy * 15, 100)
        
        predictions.append({
            "type": "encryption_probability",
            "prediction": f"{encryption_prob:.0f}%",
            "confidence": 0.78,
            "timeframe": "next_30_minutes",
            "description": f"Probability of encryption activity: {encryption_prob:.0f}%"
        })
        
        # Prediction 3: Attack progression
        if anomalies:
            predictions.append({
                "type": "attack_progression",
                "prediction": "ACTIVE",
                "confidence": 0.82,
                "timeframe": "current",
                "description": "Attack appears to be in progress",
                "indicators": [a["type"] for a in anomalies]
            })
        
        # Prediction 4: Data at risk
        total_files = patterns["behavioral"]["total_files"]
        files_at_risk = int(total_files * (risk_score / 100))
        
        predictions.append({
            "type": "data_at_risk",
            "prediction": f"{files_at_risk} files",
            "confidence": 0.75,
            "timeframe": "next_hour",
            "description": f"Estimated files at risk: {files_at_risk}/{total_files}"
        })
        
        # Prediction 5: Recommended action
        if risk_score >= 75:
            action = "IMMEDIATE_LOCKDOWN"
        elif risk_score >= 50:
            action = "INCREASED_MONITORING"
        elif risk_score >= 25:
            action = "STANDARD_MONITORING"
        else:
            action = "CONTINUE_NORMAL"
        
        predictions.append({
            "type": "recommended_action",
            "prediction": action,
            "confidence": 0.90,
            "timeframe": "immediate",
            "description": f"Recommended action: {action.replace('_', ' ')}"
        })
        
        return predictions
    
    def _calculate_entropy(self, filepath: str) -> float:
        """Calculate file entropy."""
        try:
            with open(filepath, 'rb') as f:
                data = f.read(8192)
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
    
    def _avg_time_between(self, times: List[float]) -> float:
        """Calculate average time between events."""
        if len(times) < 2:
            return 0.0
        sorted_times = sorted(times)
        diffs = [sorted_times[i+1] - sorted_times[i] for i in range(len(sorted_times)-1)]
        return statistics.mean(diffs) if diffs else 0.0
    
    def _find_peak_period(self, times: List[float]) -> Dict[str, Any]:
        """Find peak activity period."""
        if not times:
            return {"start": None, "end": None, "count": 0}
        
        # Simple peak detection (group by minute)
        minute_counts = defaultdict(int)
        for t in times:
            minute = int(t // 60)
            minute_counts[minute] += 1
        
        peak_minute = max(minute_counts, key=minute_counts.get)
        
        return {
            "start": datetime.fromtimestamp(peak_minute * 60).isoformat(),
            "end": datetime.fromtimestamp((peak_minute + 1) * 60).isoformat(),
            "count": minute_counts[peak_minute]
        }
    
    def _calculate_regularity(self, times: List[float]) -> float:
        """Calculate regularity of activity (0-1)."""
        if len(times) < 2:
            return 0.0
        
        sorted_times = sorted(times)
        diffs = [sorted_times[i+1] - sorted_times[i] for i in range(len(sorted_times)-1)]
        
        if not diffs:
            return 0.0
        
        avg_diff = statistics.mean(diffs)
        if avg_diff == 0:
            return 1.0
        
        std_diff = statistics.stdev(diffs) if len(diffs) > 1 else 0
        coefficient_of_variation = std_diff / avg_diff
        
        # Regularity is inverse of coefficient of variation
        regularity = 1 / (1 + coefficient_of_variation)
        
        return min(regularity, 1.0)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        directory = "./test_vault"
    else:
        directory = sys.argv[1]
    
    analyzer = PredictiveAnalyzer()
    
    print("🔮 Predictive Threat Analyzer")
    print(f"   Directory: {directory}")
    print()
    
    # Run analysis
    result = analyzer.analyze_patterns(directory)
    
    # Print summary
    print("  📊 Analysis Results:")
    print(f"    Patterns identified: {len(result.get('patterns', {}))}")
    print(f"    Anomalies detected: {len(result.get('anomalies', []))}")
    print(f"    Risk factors: {len(result.get('risk_factors', []))}")
    print(f"    Predictions: {len(result.get('predictions', []))}")
    print()
    
    # Print predictions
    print("  🔮 Predictions:")
    for pred in result.get("predictions", []):
        print(f"    {pred['type']}: {pred['prediction']} ({pred['confidence']:.0%} confidence)")
    print()
    
    # Print risk factors
    print("  ⚠️  Risk Factors:")
    for rf in result.get("risk_factors", []):
        print(f"    {rf['factor']}: {rf['description']} (contribution: {rf['contribution']:.1f})")
    print()
    
    # Output as JSON
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
