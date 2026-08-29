#!/usr/bin/env python3
"""
AutoVault Entropy Analyzer — Sandbox-executable script for entropy analysis.

This script performs deep entropy analysis on files and directories,
generating visual entropy maps and detecting encrypted content.
"""

import os
import sys
import json
import math
from typing import Dict, List, Any, Tuple
from datetime import datetime


class EntropyAnalyzer:
    """Analyze entropy patterns in files and directories."""
    
    # Entropy thresholds
    THRESHOLDS = {
        "encrypted": 7.5,
        "compressed": 7.0,
        "compressed_high": 7.3,
        "normal_max": 6.5,
        "normal_min": 3.0,
        "text_max": 5.5
    }
    
    def __init__(self, chunk_size: int = 1024):
        self.chunk_size = chunk_size
        self.results = []
    
    def calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of data."""
        if not data:
            return 0.0
        
        byte_freq = {}
        for byte in data:
            byte_freq[byte] = byte_freq.get(byte, 0) + 1
        
        length = len(data)
        entropy = -sum((count / length) * math.log2(count / length) 
                      for count in byte_freq.values())
        
        return entropy
    
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Perform deep entropy analysis on a file."""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            if not data:
                return {"error": "Empty file", "file": filepath}
            
            # Overall entropy
            overall_entropy = self.calculate_entropy(data)
            
            # Chunk-by-chunk entropy map
            entropy_map = []
            encrypted_chunks = 0
            compressed_chunks = 0
            
            for i in range(0, len(data), self.chunk_size):
                chunk = data[i:i+self.chunk_size]
                chunk_entropy = self.calculate_entropy(chunk)
                
                chunk_info = {
                    "offset": i,
                    "size": len(chunk),
                    "entropy": round(chunk_entropy, 4),
                    "classification": self._classify_entropy(chunk_entropy)
                }
                
                entropy_map.append(chunk_info)
                
                if chunk_entropy > self.THRESHOLDS["encrypted"]:
                    encrypted_chunks += 1
                elif chunk_entropy > self.THRESHOLDS["compressed"]:
                    compressed_chunks += 1
            
            # Detect encryption patterns
            encryption_detected = encrypted_chunks > len(entropy_map) * 0.5
            compression_detected = compressed_chunks > len(entropy_map) * 0.3
            
            # Find entropy transitions
            transitions = self._find_transitions(entropy_map)
            
            result = {
                "file": filepath,
                "size": len(data),
                "overall_entropy": round(overall_entropy, 4),
                "classification": self._classify_entropy(overall_entropy),
                "chunk_size": self.chunk_size,
                "total_chunks": len(entropy_map),
                "encrypted_chunks": encrypted_chunks,
                "compressed_chunks": compressed_chunks,
                "encryption_detected": encryption_detected,
                "compression_detected": compression_detected,
                "entropy_map": entropy_map[:100],  # Limit for large files
                "transitions": transitions,
                "entropy_distribution": self._calculate_distribution(entropy_map),
                "risk_assessment": self._assess_risk(overall_entropy, encrypted_chunks, 
                                                     len(entropy_map), transitions)
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            return {"error": str(e), "file": filepath}
    
    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze entropy of all files in a directory."""
        analysis = {
            "directory": directory,
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "total_files": 0,
            "high_entropy_files": [],
            "encrypted_files": [],
            "compressed_files": [],
            "entropy_statistics": {
                "min": float('inf'),
                "max": float('-inf'),
                "avg": 0,
                "std_dev": 0
            },
            "risk_summary": {
                "encrypted_count": 0,
                "high_entropy_count": 0,
                "total_risk_score": 0
            }
        }
        
        entropies = []
        
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    analysis["total_files"] += 1
                    
                    # Quick entropy check
                    file_analysis = self.analyze_file(entry.path)
                    
                    if "error" not in file_analysis:
                        analysis["files_analyzed"] += 1
                        entropy = file_analysis["overall_entropy"]
                        entropies.append(entropy)
                        
                        # Track high entropy files
                        if entropy > self.THRESHOLDS["normal_max"]:
                            analysis["high_entropy_files"].append({
                                "name": entry.name,
                                "entropy": round(entropy, 4),
                                "classification": file_analysis["classification"]
                            })
                        
                        # Track encrypted files
                        if file_analysis["encryption_detected"]:
                            analysis["encrypted_files"].append({
                                "name": entry.name,
                                "entropy": round(entropy, 4),
                                "encrypted_chunks": file_analysis["encrypted_chunks"]
                            })
                            analysis["risk_summary"]["encrypted_count"] += 1
                        
                        # Track compressed files
                        if file_analysis["compression_detected"]:
                            analysis["compressed_files"].append({
                                "name": entry.name,
                                "entropy": round(entropy, 4)
                            })
        except Exception as e:
            analysis["error"] = str(e)
        
        # Calculate statistics
        if entropies:
            analysis["entropy_statistics"]["min"] = round(min(entropies), 4)
            analysis["entropy_statistics"]["max"] = round(max(entropies), 4)
            analysis["entropy_statistics"]["avg"] = round(sum(entropies) / len(entropies), 4)
            analysis["entropy_statistics"]["std_dev"] = round(
                math.sqrt(sum((e - analysis["entropy_statistics"]["avg"]) ** 2 
                             for e in entropies) / len(entropies)), 4
            )
        
        analysis["risk_summary"]["high_entropy_count"] = len(analysis["high_entropy_files"])
        analysis["risk_summary"]["total_risk_score"] = self._calculate_directory_risk(analysis)
        
        return analysis
    
    def generate_visual_report(self, file_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a visual entropy report (text-based heatmap)."""
        if "entropy_map" not in file_analysis:
            return {"error": "No entropy map available"}
        
        entropy_map = file_analysis["entropy_map"]
        
        # Create text-based heatmap
        heatmap_chars = " ░▒▓█"
        heatmap = ""
        
        for chunk in entropy_map:
            entropy = chunk["entropy"]
            # Map entropy (0-8) to character index (0-4)
            char_index = min(int(entropy / 2), 4)
            heatmap += heatmap_chars[char_index]
        
        # Create summary visualization
        visualization = {
            "heatmap": heatmap[:200],  # Limit length
            "entropy_curve": [c["entropy"] for c in entropy_map[:50]],
            "classification_summary": {
                "encrypted_regions": file_analysis.get("encrypted_chunks", 0),
                "compressed_regions": file_analysis.get("compressed_chunks", 0),
                "total_regions": file_analysis.get("total_chunks", 0)
            }
        }
        
        return visualization
    
    def _classify_entropy(self, entropy: float) -> str:
        """Classify entropy value."""
        if entropy > self.THRESHOLDS["encrypted"]:
            return "ENCRYPTED"
        elif entropy > self.THRESHOLDS["compressed_high"]:
            return "HIGHLY_COMPRESSED"
        elif entropy > self.THRESHOLDS["compressed"]:
            return "COMPRESSED"
        elif entropy > self.THRESHOLDS["normal_max"]:
            return "HIGH_ENTROPY"
        elif entropy > self.THRESHOLDS["text_max"]:
            return "BINARY"
        elif entropy > self.THRESHOLDS["normal_min"]:
            return "TEXT"
        else:
            return "LOW_ENTROPY"
    
    def _find_transitions(self, entropy_map: List[Dict]) -> List[Dict]:
        """Find significant entropy transitions."""
        transitions = []
        
        for i in range(1, len(entropy_map)):
            prev_entropy = entropy_map[i-1]["entropy"]
            curr_entropy = entropy_map[i]["entropy"]
            
            # Significant transition (entropy change > 1.5)
            if abs(curr_entropy - prev_entropy) > 1.5:
                transitions.append({
                    "position": i,
                    "from_entropy": round(prev_entropy, 4),
                    "to_entropy": round(curr_entropy, 4),
                    "change": round(curr_entropy - prev_entropy, 4),
                    "type": "encryption_start" if curr_entropy > prev_entropy else "encryption_end"
                })
        
        return transitions[:20]  # Limit to 20 transitions
    
    def _calculate_distribution(self, entropy_map: List[Dict]) -> Dict[str, int]:
        """Calculate entropy distribution."""
        distribution = {
            "0-2": 0,
            "2-4": 0,
            "4-6": 0,
            "6-7": 0,
            "7-8": 0
        }
        
        for chunk in entropy_map:
            entropy = chunk["entropy"]
            if entropy < 2:
                distribution["0-2"] += 1
            elif entropy < 4:
                distribution["2-4"] += 1
            elif entropy < 6:
                distribution["4-6"] += 1
            elif entropy < 7:
                distribution["6-7"] += 1
            else:
                distribution["7-8"] += 1
        
        return distribution
    
    def _assess_risk(self, overall_entropy: float, encrypted_chunks: int, 
                    total_chunks: int, transitions: List) -> Dict[str, Any]:
        """Assess risk based on entropy analysis."""
        risk_score = 0
        risk_factors = []
        
        # High overall entropy
        if overall_entropy > self.THRESHOLDS["encrypted"]:
            risk_score += 40
            risk_factors.append("Overall entropy indicates encryption")
        elif overall_entropy > self.THRESHOLDS["compressed"]:
            risk_score += 20
            risk_factors.append("Overall entropy indicates compression")
        
        # Many encrypted chunks
        if total_chunks > 0:
            encrypted_ratio = encrypted_chunks / total_chunks
            if encrypted_ratio > 0.5:
                risk_score += 30
                risk_factors.append(f"{encrypted_ratio:.0%} of file appears encrypted")
            elif encrypted_ratio > 0.3:
                risk_score += 15
                risk_factors.append(f"{encrypted_ratio:.0%} of file has high entropy")
        
        # Many transitions
        if len(transitions) > 5:
            risk_score += 20
            risk_factors.append("Multiple entropy transitions detected")
        
        # Calculate risk level
        if risk_score >= 70:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "score": min(risk_score, 100),
            "level": risk_level,
            "factors": risk_factors
        }
    
    def _calculate_directory_risk(self, analysis: Dict) -> int:
        """Calculate overall risk score for directory."""
        risk_score = 0
        
        # Encrypted files
        risk_score += analysis["risk_summary"]["encrypted_count"] * 25
        
        # High entropy files
        risk_score += analysis["risk_summary"]["high_entropy_count"] * 10
        
        # Average entropy
        avg_entropy = analysis["entropy_statistics"]["avg"]
        if avg_entropy > self.THRESHOLDS["encrypted"]:
            risk_score += 30
        elif avg_entropy > self.THRESHOLDS["compressed"]:
            risk_score += 15
        
        return min(risk_score, 100)


def main():
    """Main entry point for sandbox execution."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: entropy_analyzer.py <file_or_directory>"}))
        sys.exit(1)
    
    target = sys.argv[1]
    analyzer = EntropyAnalyzer()
    
    if os.path.isfile(target):
        result = analyzer.analyze_file(target)
        # Add visual report
        result["visualization"] = analyzer.generate_visual_report(result)
    elif os.path.isdir(target):
        result = analyzer.analyze_directory(target)
    else:
        result = {"error": f"Target not found: {target}"}
    
    # Output as JSON
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
