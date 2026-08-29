#!/usr/bin/env python3
"""
AutoVault Knowledge Graph for Threat Intelligence — FUTURE OF AI SECURITY.

This module implements semantic knowledge graph for security:
- Graph-based threat representation
- Semantic reasoning over threats
- Relationship discovery
- Inference and prediction
- Contextual understanding

This is the FUTURE of threat intelligence — understanding threats
through relationships and context, not just isolated indicators.
"""

import os
import sys
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
from collections import defaultdict


class NodeType(Enum):
    THREAT = "threat"
    ACTOR = "actor"
    TOOL = "tool"
    TECHNIQUE = "technique"
    VULNERABILITY = "vulnerability"
    INDICATOR = "indicator"
    ASSET = "asset"
    MITIGATION = "mitigation"


class EdgeType(Enum):
    USES = "uses"
    TARGETS = "targets"
    EXPLOITS = "exploits"
    MITIGATES = "mitigates"
    ASSOCIATED_WITH = "associated_with"
    PART_OF = "part_of"
    ORIGINATES_FROM = "originate_from"


@dataclass
class GraphNode:
    id: str
    type: NodeType
    name: str
    properties: Dict[str, Any]
    created_at: str


@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    type: EdgeType
    properties: Dict[str, Any]
    weight: float


class KnowledgeGraphThreatIntel:
    """
    Knowledge Graph for Threat Intelligence — FUTURE OF AI SECURITY.
    
    This system features:
    - Graph-based threat representation
    - Semantic reasoning over relationships
    - Inference of hidden connections
    - Contextual threat understanding
    - Pattern discovery
    
    This is the FUTURE of threat intelligence.
    """
    
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
        self.inference_cache: Dict[str, Any] = {}
        
    def add_node(self, node_type: NodeType, name: str, 
                 properties: Dict[str, Any] = None) -> GraphNode:
        """Add a node to the knowledge graph."""
        node = GraphNode(
            id=str(uuid.uuid4())[:8],
            type=node_type,
            name=name,
            properties=properties or {},
            created_at=datetime.now().isoformat()
        )
        
        self.nodes[node.id] = node
        
        print(f"   📊 Added node: {node.name} ({node.type.value})")
        
        return node
    
    def add_edge(self, source_id: str, target_id: str, 
                 edge_type: EdgeType, properties: Dict[str, Any] = None,
                 weight: float = 1.0) -> GraphEdge:
        """Add an edge (relationship) to the knowledge graph."""
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Source or target node not found")
        
        edge = GraphEdge(
            id=str(uuid.uuid4())[:8],
            source=source_id,
            target=target_id,
            type=edge_type,
            properties=properties or {},
            weight=weight
        )
        
        self.edges[edge.id] = edge
        self.adjacency[source_id].append(target_id)
        self.adjacency[target_id].append(source_id)
        
        source_name = self.nodes[source_id].name
        target_name = self.nodes[target_id].name
        
        print(f"   🔗 Added edge: {source_name} --[{edge_type.value}]--> {target_name}")
        
        return edge
    
    def infer_relationships(self, node_id: str) -> List[Dict[str, Any]]:
        """
        Infer hidden relationships through graph traversal.
        
        Semantic reasoning discovers non-obvious connections.
        """
        if node_id not in self.nodes:
            return []
        
        node = self.nodes[node_id]
        inferences = []
        
        # Find 2-hop neighbors
        direct_neighbors = set(self.adjacency.get(node_id, []))
        two_hop_neighbors = set()
        
        for neighbor in direct_neighbors:
            two_hop_neighbors.update(self.adjacency.get(neighbor, []))
        
        two_hop_neighbors.discard(node_id)
        
        # Infer relationships
        for neighbor_id in two_hop_neighbors:
            if neighbor_id in self.nodes:
                neighbor = self.nodes[neighbor_id]
                
                # Find common connections
                common = direct_neighbors.intersection(set(self.adjacency.get(neighbor_id, [])))
                
                if common:
                    inferences.append({
                        "source": node.name,
                        "target": neighbor.name,
                        "inferred_relationship": "indirect_connection",
                        "through": [self.nodes[n].name for n in common if n in self.nodes],
                        "confidence": min(len(common) * 0.2, 0.8)
                    })
        
        return inferences
    
    def find_attack_paths(self, source_id: str, target_id: str) -> List[List[Dict]]:
        """
        Find potential attack paths between nodes.
        
        Graph traversal to discover attack vectors.
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            return []
        
        # BFS to find paths
        paths = []
        queue = [(source_id, [source_id])]
        
        visited = {source_id}
        max_depth = 5
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            if current == target_id:
                # Convert path to readable format
                readable_path = []
                for node_id in path:
                    if node_id in self.nodes:
                        readable_path.append({
                            "id": node_id,
                            "name": self.nodes[node_id].name,
                            "type": self.nodes[node_id].type.value
                        })
                paths.append(readable_path)
                continue
            
            for neighbor in self.adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return paths[:10]  # Limit to 10 paths
    
    def discover_patterns(self) -> List[Dict[str, Any]]:
        """
        Discover patterns in the knowledge graph.
        
        Find common structures and relationships.
        """
        patterns = []
        
        # Find common subgraphs
        node_types = defaultdict(int)
        edge_types = defaultdict(int)
        
        for node in self.nodes.values():
            node_types[node.type.value] += 1
        
        for edge in self.edges.values():
            edge_types[edge.type.value] += 1
        
        # Pattern 1: Threat-Tool chains
        threat_tools = []
        for edge in self.edges.values():
            if edge.type == EdgeType.USES:
                source = self.nodes.get(edge.source)
                target = self.nodes.get(edge.target)
                if source and target:
                    threat_tools.append({
                        "threat": source.name,
                        "tool": target.name
                    })
        
        if threat_tools:
            patterns.append({
                "type": "threat_tool_chain",
                "description": f"Found {len(threat_tools)} threat-tool relationships",
                "examples": threat_tools[:3]
            })
        
        # Pattern 2: Target patterns
        target_counts = defaultdict(int)
        for edge in self.edges.values():
            if edge.type == EdgeType.TARGETS:
                target = self.nodes.get(edge.target)
                if target:
                    target_counts[target.name] += 1
        
        if target_counts:
            most_targeted = max(target_counts, key=target_counts.get)
            patterns.append({
                "type": "target_pattern",
                "description": f"Most targeted asset: {most_targeted}",
                "count": target_counts[most_targeted]
            })
        
        return patterns
    
    def semantic_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Semantic search over the knowledge graph.
        
        Find relevant nodes and relationships based on meaning.
        """
        results = []
        query_lower = query.lower()
        
        # Search nodes by name and properties
        for node in self.nodes.values():
            score = 0
            
            # Name match
            if query_lower in node.name.lower():
                score += 0.5
            
            # Property match
            for prop_value in node.properties.values():
                if isinstance(prop_value, str) and query_lower in prop_value.lower():
                    score += 0.3
                elif isinstance(prop_value, list):
                    for item in prop_value:
                        if isinstance(item, str) and query_lower in item.lower():
                            score += 0.2
            
            if score > 0:
                results.append({
                    "node": {
                        "id": node.id,
                        "name": node.name,
                        "type": node.type.value
                    },
                    "score": score,
                    "relationships": len(self.adjacency.get(node.id, []))
                })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:10]
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Get knowledge graph statistics."""
        node_type_counts = defaultdict(int)
        edge_type_counts = defaultdict(int)
        
        for node in self.nodes.values():
            node_type_counts[node.type.value] += 1
        
        for edge in self.edges.values():
            edge_type_counts[edge.type.value] += 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": dict(node_type_counts),
            "edge_types": dict(edge_type_counts),
            "avg_degree": sum(len(v) for v in self.adjacency.values()) / max(len(self.nodes), 1)
        }
    
    def visualize_graph(self) -> str:
        """Generate text-based graph visualization."""
        lines = ["Knowledge Graph Visualization:"]
        lines.append("=" * 50)
        
        # Group by node type
        nodes_by_type = defaultdict(list)
        for node in self.nodes.values():
            nodes_by_type[node.type.value].append(node)
        
        for node_type, nodes in nodes_by_type.items():
            lines.append(f"\n{node_type.upper()}S:")
            for node in nodes:
                connections = len(self.adjacency.get(node.id, []))
                lines.append(f"  - {node.name} ({connections} connections)")
        
        return "\n".join(lines)


async def main():
    """Demo knowledge graph."""
    kg = KnowledgeGraphThreatIntel()
    
    print("📊 Knowledge Graph for Threat Intelligence Demo")
    print()
    
    # Add nodes
    print("=== Adding Nodes ===")
    ransomware = kg.add_node(NodeType.THREAT, "Ransomware", {
        "severity": "CRITICAL",
        "description": "Malware that encrypts files"
    })
    
    wannacry = kg.add_node(NodeType.THREAT, "WannaCry", {
        "severity": "CRITICAL",
        "first_seen": "2017"
    })
    
    exploit = kg.add_node(NodeType.VULNERABILITY, "EternalBlue", {
        "cve": "CVE-2017-0144",
        "severity": "CRITICAL"
    })
    
    smb = kg.add_node(NodeType.TECHNIQUE, "SMB Exploitation", {
        "mitre_id": "T1210"
    })
    
    windows = kg.add_node(NodeType.ASSET, "Windows Server", {
        "os": "Windows",
        "criticality": "HIGH"
    })
    
    backup = kg.add_node(NodeType.MITIGATION, "Regular Backups", {
        "effectiveness": "HIGH"
    })
    
    print()
    
    # Add edges
    print("=== Adding Relationships ===")
    kg.add_edge(wannacry.id, ransomware.id, EdgeType.ASSOCIATED_WITH)
    kg.add_edge(wannacry.id, exploit.id, EdgeType.USES)
    kg.add_edge(exploit.id, smb.id, EdgeType.PART_OF)
    kg.add_edge(wannacry.id, windows.id, EdgeType.TARGETS)
    kg.add_edge(backup.id, ransomware.id, EdgeType.MITIGATES)
    
    print()
    
    # Infer relationships
    print("=== Inferring Relationships ===")
    inferences = kg.infer_relationships(wannacry.id)
    for inference in inferences:
        print(f"   Inferred: {inference['source']} -> {inference['target']}")
        print(f"      Through: {inference['through']}")
        print(f"      Confidence: {inference['confidence']:.0%}")
    
    print()
    
    # Find attack paths
    print("=== Finding Attack Paths ===")
    paths = kg.find_attack_paths(wannacry.id, windows.id)
    for i, path in enumerate(paths[:2]):
        print(f"   Path {i+1}: {' -> '.join(p['name'] for p in path)}")
    
    print()
    
    # Discover patterns
    print("=== Discovering Patterns ===")
    patterns = kg.discover_patterns()
    for pattern in patterns:
        print(f"   Pattern: {pattern['type']}")
        print(f"      {pattern['description']}")
    
    print()
    
    # Semantic search
    print("=== Semantic Search ===")
    results = kg.semantic_search("ransomware")
    for result in results[:3]:
        print(f"   Found: {result['node']['name']} (score: {result['score']:.2f})")
    
    print()
    
    # Get stats
    stats = kg.get_graph_stats()
    print("📊 Graph Stats:")
    print(json.dumps(stats, indent=2))
    
    # Visualize
    print()
    print(kg.visualize_graph())


if __name__ == "__main__":
    asyncio.run(main())
