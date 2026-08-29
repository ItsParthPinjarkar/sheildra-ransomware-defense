#!/usr/bin/env python3
"""
AutoVault AI Agent Memory Architecture — FUTURE OF AI SECURITY.

This module implements human-like memory for security agents:
- Episodic Memory: Remember specific incidents and events
- Semantic Memory: General knowledge about threats and defenses
- Procedural Memory: How to perform security actions
- Working Memory: Current context and attention
- Memory Consolidation: Transfer short-term to long-term
- Memory Retrieval: Access relevant memories for decisions

This is the FUTURE of AI security agents — memory that makes them
truly intelligent and capable of learning from experience.
"""

import os
import sys
import json
import time
import math
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class MemoryType(Enum):
    EPISODIC = "episodic"      # Specific events and incidents
    SEMANTIC = "semantic"      # General knowledge
    PROCEDURAL = "procedural"  # How to do things
    WORKING = "working"        # Current context


class MemoryImportance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Memory:
    id: str
    type: MemoryType
    content: Dict[str, Any]
    importance: MemoryImportance
    created_at: str
    last_accessed: str
    access_count: int
    emotional_valence: float  # -1 to 1 (negative to positive)
    associations: List[str]  # IDs of associated memories
    tags: List[str]


class AgentMemoryArchitecture:
    """
    AI Agent Memory Architecture — FUTURE OF AI SECURITY.
    
    This system features:
    - Human-like memory types (episodic, semantic, procedural)
    - Memory consolidation and decay
    - Associative memory retrieval
    - Emotional valence for importance weighting
    - Working memory for current context
    
    This is the FUTURE of intelligent security agents.
    """
    
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.working_memory: List[str] = []  # Current context (limited capacity)
        self.working_memory_capacity = 7  # Miller's Law
        self.consolidation_threshold = 3  # Access count to consolidate
        self.decay_rate = 0.1  # Memory decay per day
        
    def store_episodic_memory(self, event: Dict[str, Any], 
                              importance: MemoryImportance = MemoryImportance.MEDIUM) -> str:
        """
        Store episodic memory (specific event).
        
        Episodic memory remembers WHAT happened, WHEN, and HOW it FELT.
        """
        memory = Memory(
            id=str(uuid.uuid4())[:8],
            type=MemoryType.EPISODIC,
            content={
                "event": event.get("type", "unknown"),
                "description": event.get("description", ""),
                "timestamp": event.get("timestamp", datetime.now().isoformat()),
                "location": event.get("location", "unknown"),
                "actors": event.get("actors", []),
                "outcome": event.get("outcome", "unknown"),
                "details": event
            },
            importance=importance,
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat(),
            access_count=0,
            emotional_valence=self._calculate_emotional_valence(event),
            associations=[],
            tags=event.get("tags", [])
        )
        
        self.memories[memory.id] = memory
        
        # Add to working memory
        self._addToWorkingMemory(memory.id)
        
        print(f"   🧠 Episodic memory stored: {memory.id}")
        print(f"      Event: {event.get('type', 'unknown')}")
        print(f"      Importance: {importance.name}")
        print(f"      Emotional valence: {memory.emotional_valence:.2f}")
        
        return memory.id
    
    def store_semantic_memory(self, knowledge: Dict[str, Any],
                              importance: MemoryImportance = MemoryImportance.MEDIUM) -> str:
        """
        Store semantic memory (general knowledge).
        
        Semantic memory remembers FACTS, CONCEPTS, and RELATIONSHIPS.
        """
        memory = Memory(
            id=str(uuid.uuid4())[:8],
            type=MemoryType.SEMANTIC,
            content={
                "concept": knowledge.get("concept", "unknown"),
                "definition": knowledge.get("definition", ""),
                "relationships": knowledge.get("relationships", []),
                "examples": knowledge.get("examples", []),
                "category": knowledge.get("category", "general"),
                "confidence": knowledge.get("confidence", 0.8),
                "source": knowledge.get("source", "learned")
            },
            importance=importance,
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat(),
            access_count=0,
            emotional_valence=0.0,  # Neutral for facts
            associations=[],
            tags=knowledge.get("tags", [])
        )
        
        self.memories[memory.id] = memory
        
        print(f"   📚 Semantic memory stored: {memory.id}")
        print(f"      Concept: {knowledge.get('concept', 'unknown')}")
        print(f"      Category: {knowledge.get('category', 'general')}")
        
        return memory.id
    
    def store_procedural_memory(self, procedure: Dict[str, Any],
                                importance: MemoryImportance = MemoryImportance.HIGH) -> str:
        """
        Store procedural memory (how to do things).
        
        Procedural memory remembers SKILLS, PROCEDURES, and HABITS.
        """
        memory = Memory(
            id=str(uuid.uuid4())[:8],
            type=MemoryType.PROCEDURAL,
            content={
                "skill": procedure.get("skill", "unknown"),
                "steps": procedure.get("steps", []),
                "conditions": procedure.get("conditions", []),
                "preconditions": procedure.get("preconditions", []),
                "postconditions": procedure.get("postconditions", []),
                "tools_required": procedure.get("tools", []),
                "success_criteria": procedure.get("success_criteria", []),
                "failure_modes": procedure.get("failure_modes", [])
            },
            importance=importance,
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat(),
            access_count=0,
            emotional_valence=0.1,  # Slightly positive for skills
            associations=[],
            tags=procedure.get("tags", [])
        )
        
        self.memories[memory.id] = memory
        
        print(f"   🔧 Procedural memory stored: {memory.id}")
        print(f"      Skill: {procedure.get('skill', 'unknown')}")
        print(f"      Steps: {len(procedure.get('steps', []))}")
        
        return memory.id
    
    def retrieve_memories(self, query: Dict[str, Any], 
                          memory_type: Optional[MemoryType] = None,
                          limit: int = 5) -> List[Memory]:
        """
        Retrieve memories based on query.
        
        Memory retrieval uses:
        - Recency: Recently accessed memories
        - Frequency: Frequently accessed memories
        - Importance: Important memories
        - Similarity: Content similarity
        - Emotion: Emotionally charged memories
        """
        candidates = list(self.memories.values())
        
        # Filter by type if specified
        if memory_type:
            candidates = [m for m in candidates if m.type == memory_type]
        
        # Score each candidate
        scored = []
        for memory in candidates:
            score = self._calculate_retrieval_score(memory, query)
            scored.append((memory, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return top results
        results = []
        for memory, score in scored[:limit]:
            # Update access metadata
            memory.last_accessed = datetime.now().isoformat()
            memory.access_count += 1
            
            # Add to working memory
            self._addToWorkingMemory(memory.id)
            
            results.append(memory)
        
        return results
    
    def _calculate_retrieval_score(self, memory: Memory, query: Dict) -> float:
        """Calculate retrieval score for a memory."""
        score = 0.0
        
        # Recency score (exponential decay)
        last_accessed = datetime.fromisoformat(memory.last_accessed)
        hours_since = (datetime.now() - last_accessed).total_seconds() / 3600
        recency_score = math.exp(-hours_since / 24)  # Decay over 24 hours
        score += recency_score * 0.2
        
        # Frequency score
        frequency_score = min(memory.access_count / 10, 1.0)
        score += frequency_score * 0.2
        
        # Importance score
        importance_score = memory.importance.value / 4
        score += importance_score * 0.3
        
        # Emotional valence score (emotional memories are more memorable)
        emotion_score = abs(memory.emotional_valence)
        score += emotion_score * 0.1
        
        # Content similarity (simplified)
        query_text = json.dumps(query).lower()
        memory_text = json.dumps(memory.content).lower()
        
        # Simple word overlap
        query_words = set(query_text.split())
        memory_words = set(memory_text.split())
        overlap = len(query_words & memory_words) / max(len(query_words), 1)
        score += overlap * 0.2
        
        return score
    
    def _addToWorkingMemory(self, memory_id: str):
        """Add memory to working memory (limited capacity)."""
        # Remove if already present
        if memory_id in self.working_memory:
            self.working_memory.remove(memory_id)
        
        # Add to front (most recent)
        self.working_memory.insert(0, memory_id)
        
        # Enforce capacity limit
        if len(self.working_memory) > self.working_memory_capacity:
            # Remove oldest (least recently used)
            removed_id = self.working_memory.pop()
            print(f"   🧠 Working memory overflow: evicted {removed_id}")
    
    def consolidate_memories(self):
        """
        Consolidate short-term to long-term memory.
        
        Memory consolidation:
        - Transfer frequently accessed memories to long-term
        - Decay rarely accessed memories
        - Strengthen associations between related memories
        """
        print("\n🔄 Memory Consolidation...")
        
        consolidated = 0
        decayed = 0
        
        for memory in list(self.memories.values()):
            # Consolidation: frequently accessed memories become stronger
            if memory.access_count >= self.consolidation_threshold:
                # Strengthen importance
                if memory.importance.value < 4:
                    memory.importance = MemoryImportance(min(memory.importance.value + 1, 4))
                    consolidated += 1
                    print(f"   ✓ Consolidated: {memory.id} (now {memory.importance.name})")
            
            # Decay: rarely accessed memories fade
            last_accessed = datetime.fromisoformat(memory.last_accessed)
            days_since = (datetime.now() - last_accessed).days
            
            if days_since > 7 and memory.access_count < 2:
                # Apply decay
                decay_factor = math.exp(-self.decay_rate * days_since)
                if decay_factor < 0.3:
                    # Mark for potential deletion (not actually deleting in demo)
                    decayed += 1
                    print(f"   ⚠️  Decaying: {memory.id} (factor: {decay_factor:.2f})")
        
        print(f"   Consolidated: {consolidated}")
        print(f"   Decaying: {decayed}")
    
    def _calculate_emotional_valence(self, event: Dict) -> float:
        """Calculate emotional valence of an event."""
        # Negative events
        negative_keywords = ["attack", "breach", "malware", "ransomware", "failure", "critical"]
        # Positive events
        positive_keywords = ["success", "blocked", "prevented", "recovered", "normal"]
        
        event_text = json.dumps(event).lower()
        
        negative_count = sum(1 for kw in negative_keywords if kw in event_text)
        positive_count = sum(1 for kw in positive_keywords if kw in event_text)
        
        total = negative_count + positive_count
        if total == 0:
            return 0.0
        
        return (positive_count - negative_count) / total
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        type_counts = {}
        importance_counts = {}
        
        for memory in self.memories.values():
            type_counts[memory.type.value] = type_counts.get(memory.type.value, 0) + 1
            importance_counts[memory.importance.name] = importance_counts.get(memory.importance.name, 0) + 1
        
        return {
            "total_memories": len(self.memories),
            "working_memory": len(self.working_memory),
            "working_memory_capacity": self.working_memory_capacity,
            "memories_by_type": type_counts,
            "memories_by_importance": importance_counts,
            "avg_access_count": sum(m.access_count for m in self.memories.values()) / max(len(self.memories), 1)
        }
    
    def generate_memory_report(self) -> str:
        """Generate natural language memory report."""
        stats = self.get_memory_stats()
        
        report = "## Agent Memory Report\n\n"
        report += f"**Total Memories:** {stats['total_memories']}\n"
        report += f"**Working Memory:** {stats['working_memory']}/{stats['working_memory_capacity']}\n\n"
        
        report += "### Memory Distribution\n"
        for mem_type, count in stats['memories_by_type'].items():
            report += f"- {mem_type}: {count}\n"
        
        report += "\n### Importance Distribution\n"
        for importance, count in stats['memories_by_importance'].items():
            report += f"- {importance}: {count}\n"
        
        return report


async def main():
    """Demo agent memory architecture."""
    memory = AgentMemoryArchitecture()
    
    print("🧠 AI Agent Memory Architecture Demo")
    print()
    
    # Store episodic memories
    print("=== Storing Episodic Memories ===")
    memory.store_episodic_memory({
        "type": "ransomware_attack",
        "description": "Detected and blocked ransomware attack",
        "location": "./test_vault",
        "actors": ["attacker", "defender"],
        "outcome": "success",
        "tags": ["ransomware", "detection", "success"]
    }, MemoryImportance.CRITICAL)
    
    memory.store_episodic_memory({
        "type": "malware_detection",
        "description": "Found suspicious malware in downloads",
        "location": "./downloads",
        "actors": ["defender"],
        "outcome": "success",
        "tags": ["malware", "detection"]
    }, MemoryImportance.HIGH)
    
    print()
    
    # Store semantic memories
    print("=== Storing Semantic Memories ===")
    memory.store_semantic_memory({
        "concept": "Ransomware",
        "definition": "Malware that encrypts files and demands ransom",
        "relationships": ["encrypts", "demands", "bitcoin"],
        "examples": ["WannaCry", "Ryuk", "Maze"],
        "category": "threat_type",
        "tags": ["malware", "ransomware"]
    })
    
    memory.store_semantic_memory({
        "concept": "Entropy Analysis",
        "definition": "Measuring randomness in file contents",
        "relationships": ["detects", "encryption", "compression"],
        "category": "detection_method",
        "tags": ["analysis", "entropy"]
    })
    
    print()
    
    # Store procedural memories
    print("=== Storing Procedural Memories ===")
    memory.store_procedural_memory({
        "skill": "Incident Response",
        "steps": [
            "Detect threat",
            "Contain threat",
            "Eradicate threat",
            "Recover systems",
            "Document incident"
        ],
        "conditions": ["threat_detected"],
        "tools": ["scan_directory", "create_snapshot", "generate_report"],
        "tags": ["response", "procedure"]
    })
    
    print()
    
    # Retrieve memories
    print("=== Retrieving Memories ===")
    results = memory.retrieve_memories(
        {"query": "ransomware attack"},
        limit=3
    )
    
    for mem in results:
        print(f"   Retrieved: {mem.id} ({mem.type.value})")
        print(f"      Importance: {mem.importance.name}")
        print(f"      Access count: {mem.access_count}")
    
    print()
    
    # Consolidate memories
    memory.consolidate_memories()
    
    # Get stats
    stats = memory.get_memory_stats()
    print("\n📊 Memory Stats:")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
