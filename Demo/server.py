"""
Emergency Mesh Network Simulator
==================================

Simulates a mesh network with multiple nodes, message routing,
duplicate detection, and priority-based forwarding.

Run: python3 mesh_simulator.py
"""

import uuid
import time
import random
from enum import Enum
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from datetime import datetime


# ==================== Enums ====================

class Priority(Enum):
    """Message priority levels"""
    NORMAL = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


class MessageStatus(Enum):
    """Message processing status"""
    CREATED = "created"
    FORWARDED = "forwarded"
    DELIVERED = "delivered"
    DROPPED = "dropped"


# ==================== Data Classes ====================

@dataclass
class Location:
    """GPS coordinates"""
    latitude: float
    longitude: float
    
    def __str__(self):
        return f"({self.latitude:.4f}, {self.longitude:.4f})"


@dataclass
class EMTPMessage:
    """Emergency Mesh Transfer Protocol Message"""
    message_id: str
    source_id: str
    destination_id: str  
    priority: Priority
    payload: str
    ttl: int = 30
    hop_count: int = 0
    timestamp: float = field(default_factory=time.time)
    forwarding_path: List[str] = field(default_factory=list)
    location: Optional[Location] = None
    
    def is_broadcast(self) -> bool:
        return self.destination_id == "BROADCAST"
    
    def __str__(self):
        return (f"[{self.priority.name}] "
                f"From: {self.source_id} -> {self.destination_id} "
                f"(Hops: {self.hop_count}/{self.ttl}) "
                f"Msg: {self.payload[:30]}...")


@dataclass
class Neighbor:
    """Neighbor node information"""
    node_id: str
    last_seen: float
    signal_strength: int
    
    def is_active(self, timeout: int = 30) -> bool:
        return (time.time() - self.last_seen) < timeout


# ==================== Network Node ====================

class MeshNode:
    """A node in the mesh network"""
    
    def __init__(self, node_id: str, location: Optional[Location] = None):
        self.node_id = node_id
        self.location = location
        
        # Routing tables
        self.message_cache: Dict[str, dict] = {}
        self.forwarding_history: Dict[str, List[str]] = {}
        self.neighbors: Dict[str, Neighbor] = {}
        
        # Configuration
        self.max_cache_size = 1000
        self.cache_ttl = 3600  # 1 hour
        self.neighbor_timeout = 30
        
        # Statistics
        self.stats = {
            'messages_received': 0,
            'messages_forwarded': 0,
            'messages_delivered': 0,
            'duplicates_dropped': 0,
            'ttl_exceeded': 0
        }
        
        # For simulation visualization
        self.received_messages: List[EMTPMessage] = []
        
    def __str__(self):
        return f"Node[{self.node_id}] Neighbors: {len(self.neighbors)} Cache: {len(self.message_cache)}"
    
    # ==================== Message Handling ====================
    
    def receive_message(self, message: EMTPMessage, from_node: str) -> bool:
        """
        Main message receiving and processing logic
        
        Returns:
            True if message was processed successfully
            False if message was dropped
        """
        self.stats['messages_received'] += 1
        
        print(f"\n[{self.node_id}] Received message from {from_node}")
        print(f"  Message: {message}")
        
        # Step 1: Check TTL
        if message.hop_count >= message.ttl:
            print(f" DROP: TTL exceeded ({message.hop_count}/{message.ttl})")
            self.stats['ttl_exceeded'] += 1
            return False
        
        # Step 2: Check for duplicates
        if self.is_duplicate(message.message_id):
            print(f" DROP: ข้อความซ้ำ (Message ID: {message.message_id})")
            self.stats['duplicates_dropped'] += 1
            return False
        
        # Step 3: Cache the message
        self.cache_message(message, from_node)
        
        # Step 4: Check if this is the destination
        if message.destination_id == self.node_id or message.is_broadcast():
            print(f"DELIVER: ข้อความถึงปลายทาง ({self.node_id})")
            self.deliver_to_application(message)
            self.stats['messages_delivered'] += 1
            
            # If not broadcast, stop here
            if not message.is_broadcast():
                return True
        
        # Step 5: Forward the message
        self.forward_message(message, from_node)
        
        return True
    
    def is_duplicate(self, message_id: str) -> bool:
        """Check if message has already been processed"""
        if message_id in self.message_cache:
            cached_time = self.message_cache[message_id]['timestamp']
            if (time.time() - cached_time) < self.cache_ttl:
                return True
            else:
                # Remove expired message
                del self.message_cache[message_id]
        return False
    
    def cache_message(self, message: EMTPMessage, from_node: str):
        """Cache message to prevent duplicates"""
        self.message_cache[message.message_id] = {
            'timestamp': time.time(),
            'source': message.source_id,
            'from_node': from_node,
            'priority': message.priority
        }
        
        # Limit cache size
        if len(self.message_cache) > self.max_cache_size:
            self.cleanup_cache()
    
    def deliver_to_application(self, message: EMTPMessage):
        """Deliver message to application layer (show to user)"""
        self.received_messages.append(message)
        
        if message.priority in [Priority.HIGH, Priority.CRITICAL]:
            print(f" EMERGENCY ALERT: {message.payload}")
            if message.location:
                print(f"     Location: {message.location}")
    
    def forward_message(self, message: EMTPMessage, from_node: str):
        """
        Forward message to eligible neighbors
        
        Logic:
        1. Don't send back to sender
        2. Don't send to nodes in forwarding path
        3. Send to all other active neighbors
        """
        # Increment hop count
        message.hop_count += 1
        
        # Add this node to forwarding path
        message.forwarding_path.append(self.node_id)
        
        # Get eligible neighbors
        eligible = self.get_eligible_neighbors(message, from_node)
        
        if not eligible:
            print(f"ไม่มี node ที่สามารถส่งต่อได้")
            return
        
        # Record forwarding history
        self.forwarding_history[message.message_id] = eligible
        self.stats['messages_forwarded'] += len(eligible)
        
        # Forward to eligible neighbors
        print(f"  → FORWARD to: {', '.join(eligible)}")
        for neighbor_id in eligible:
            # This will be handled by the network simulator
            pass
    
    def get_eligible_neighbors(self, message: EMTPMessage, from_node: str) -> List[str]:
        """
        Get list of neighbors that can receive the message
        
        Rules:
        - Don't send back to sender
        - Don't send to nodes in forwarding path
        - Only send to active neighbors
        """
        eligible = []
        
        for node_id, neighbor in self.neighbors.items():
            # Don't send back to sender
            if node_id == from_node:
                continue
            
            # Don't send to nodes already in path
            if node_id in message.forwarding_path:
                continue
            
            # Only send to active neighbors
            if not neighbor.is_active(self.neighbor_timeout):
                continue
            
            eligible.append(node_id)
        
        return eligible
    
    # ==================== Neighbor Management ====================
    
    def add_neighbor(self, node_id: str, signal_strength: int = -50):
        """Add a neighbor to this node"""
        self.neighbors[node_id] = Neighbor(
            node_id=node_id,
            last_seen=time.time(),
            signal_strength=signal_strength
        )
    
    def update_neighbor(self, node_id: str):
        """Update neighbor's last_seen timestamp"""
        if node_id in self.neighbors:
            self.neighbors[node_id].last_seen = time.time()
    
    def remove_neighbor(self, node_id: str):
        """Remove a neighbor"""
        if node_id in self.neighbors:
            del self.neighbors[node_id]
            print(f"[{self.node_id}] Neighbor {node_id} removed")
    
    # ==================== Utility ====================
    
    def cleanup_cache(self):
        """Remove expired messages from cache"""
        current_time = time.time()
        expired = [
            msg_id for msg_id, meta in self.message_cache.items()
            if (current_time - meta['timestamp']) > self.cache_ttl
        ]
        
        for msg_id in expired:
            del self.message_cache[msg_id]
        
        if expired:
            print(f"[{self.node_id}] Cleaned {len(expired)} expired messages")
    
    def get_stats(self) -> dict:
        """Get node statistics"""
        return {
            'node_id': self.node_id,
            'neighbors': len(self.neighbors),
            'cache_size': len(self.message_cache),
            **self.stats
        }


# ==================== Network Simulator ====================

class MeshNetwork:
    """Simulates the entire mesh network"""
    
    def __init__(self):
        self.nodes: Dict[str, MeshNode] = {}
        self.message_log: List[dict] = []
        
    def add_node(self, node: MeshNode):
        """Add a node to the network"""
        self.nodes[node.node_id] = node
        print(f"Added {node.node_id} to network")
    
    def connect_nodes(self, node1_id: str, node2_id: str):
        """Create a bidirectional connection between two nodes"""
        if node1_id in self.nodes and node2_id in self.nodes:
            self.nodes[node1_id].add_neighbor(node2_id)
            self.nodes[node2_id].add_neighbor(node1_id)
            print(f"Connected {node1_id} <-> {node2_id}")
    
    def send_message(self, message: EMTPMessage):
        """
        Initiate message sending from source node
        
        This simulates the message propagating through the network
        """
        source_node = self.nodes.get(message.source_id)
        if not source_node:
            print(f" Source node {message.source_id} not found")
            return
        
        print(f"\n{'='*60}")
        print(f"SENDING MESSAGE")
        print(f"{'='*60}")
        print(message)
        
        # Log message creation
        self.message_log.append({
            'timestamp': time.time(),
            'message_id': message.message_id,
            'source': message.source_id,
            'destination': message.destination_id,
            'priority': message.priority.name,
            'status': 'created'
        })
        
        # Add source to forwarding path
        message.forwarding_path.append(message.source_id)
        
        # Start flooding from source
        self._propagate_message(message, message.source_id, None)
        
        print(f"\n{'='*60}")
        print(f"✓ MESSAGE PROPAGATION COMPLETE")
        print(f"{'='*60}\n")
    
    def _propagate_message(self, message: EMTPMessage, current_node_id: str, from_node: Optional[str]):
        """
        Recursively propagate message through the network
        
        This simulates actual message forwarding in the mesh network
        """
        current_node = self.nodes[current_node_id]
        
        # Node receives and processes the message
        success = current_node.receive_message(message, from_node or "ORIGIN")
        
        if not success:
            return
        
        # Get neighbors that should receive the message
        eligible_neighbors = current_node.get_eligible_neighbors(message, from_node or "ORIGIN")
        
        # Propagate to eligible neighbors
        for neighbor_id in eligible_neighbors:
            # Create a copy of the message for each neighbor
            import copy
            msg_copy = copy.deepcopy(message)
            
            # Small delay to simulate network latency
            time.sleep(0.1)
            
            # Recursively propagate
            self._propagate_message(msg_copy, neighbor_id, current_node_id)
    
    def disconnect_node(self, node_id: str):
        """Simulate a node failure"""
        if node_id not in self.nodes:
            return
        
        print(f"\n⚠️  SIMULATING NODE FAILURE: {node_id}")
        
        # Remove this node from all neighbors
        for other_node in self.nodes.values():
            other_node.remove_neighbor(node_id)
        
        # Remove all neighbors from this node
        self.nodes[node_id].neighbors.clear()
    
    def print_topology(self):
        """Print network topology"""
        print(f"\n{'='*60}")
        print(f"NETWORK TOPOLOGY")
        print(f"{'='*60}")
        
        for node_id, node in self.nodes.items():
            neighbors = ', '.join(node.neighbors.keys()) if node.neighbors else "None"
            print(f"{node_id:10} -> Neighbors: {neighbors}")
    
    def print_statistics(self):
        """Print network statistics"""
        print(f"\n{'='*60}")
        print(f"NETWORK STATISTICS")
        print(f"{'='*60}")
        
        for node_id, node in self.nodes.items():
            stats = node.get_stats()
            print(f"\n{node_id}:")
            print(f"  Received:  {stats['messages_received']}")
            print(f"  Forwarded: {stats['messages_forwarded']}")
            print(f"  Delivered: {stats['messages_delivered']}")
            print(f"  Dropped (Duplicate): {stats['duplicates_dropped']}")
            print(f"  Dropped (TTL): {stats['ttl_exceeded']}")


# ==================== Demo Scenarios ====================

def demo_basic_routing():
    """Demo: Basic message routing through 3 nodes"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Routing (A -> B -> C)")
    print("="*60)
    
    network = MeshNetwork()
    
    # Create nodes
    node_a = MeshNode("Node_A", Location(13.7563, 100.5018))  # Bangkok
    node_b = MeshNode("Node_B", Location(13.7580, 100.5050))
    node_c = MeshNode("Node_C", Location(13.7600, 100.5080))
    
    # Add to network
    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_c)
    
    # Connect: A -- B -- C
    network.connect_nodes("Node_A", "Node_B")
    network.connect_nodes("Node_B", "Node_C")
    
    network.print_topology()
    
    # Send message from A to C
    message = EMTPMessage(
        message_id=str(uuid.uuid4()),
        source_id="Node_A",
        destination_id="Node_C",
        priority=Priority.NORMAL,
        payload="Hello from Node A!",
        location=node_a.location
    )
    
    network.send_message(message)
    network.print_statistics()


def demo_mesh_topology():
    """Demo: Full mesh network with 6 nodes"""
    print("\n" + "="*60)
    print("DEMO 2: Mesh Topology (6 Nodes)")
    print("="*60)
    print("""
    Network Topology:
        A --- B --- C
        |     |     |
        D --- E --- F
    """)
    
    network = MeshNetwork()
    
    # Create nodes
    nodes = {
        'Node_A': MeshNode("Node_A", Location(13.7563, 100.5018)),
        'Node_B': MeshNode("Node_B", Location(13.7580, 100.5050)),
        'Node_C': MeshNode("Node_C", Location(13.7600, 100.5080)),
        'Node_D': MeshNode("Node_D", Location(13.7540, 100.5018)),
        'Node_E': MeshNode("Node_E", Location(13.7560, 100.5050)),
        'Node_F': MeshNode("Node_F", Location(13.7580, 100.5080)),
    }
    
    for node in nodes.values():
        network.add_node(node)
    
    # Create mesh connections
    connections = [
        ("Node_A", "Node_B"),
        ("Node_A", "Node_D"),
        ("Node_B", "Node_C"),
        ("Node_B", "Node_E"),
        ("Node_C", "Node_F"),
        ("Node_D", "Node_E"),
        ("Node_E", "Node_F"),
    ]
    
    for n1, n2 in connections:
        network.connect_nodes(n1, n2)
    
    network.print_topology()
    
    #Message Str
    message = EMTPMessage(
        message_id=str(uuid.uuid4()),
        source_id="Node_A",
        destination_id="BROADCAST",
        priority=Priority.CRITICAL,
        payload="EMERGENCY: Need immediate assistance!",
        location=nodes['Node_A'].location
    )
    
    network.send_message(message)
    network.print_statistics()


def demo_node_failure():
    """Demo: Node failure and self-healing"""
    print("\n" + "="*60)
    print("DEMO 3: Node Failure & Self-Healing")
    print("="*60)
    
    network = MeshNetwork()
    
    # Create nodes
    nodes = {
        'Node_A': MeshNode("Node_A"),
        'Node_B': MeshNode("Node_B"),
        'Node_C': MeshNode("Node_C"),
        'Node_D': MeshNode("Node_D"),
        'Node_E': MeshNode("Node_E"),
        'Node_F': MeshNode("Node_F"),
    }
    
    for node in nodes.values():
        network.add_node(node)
    
    # Create mesh topology
    connections = [
        ("Node_A", "Node_B"),
        ("Node_A", "Node_D"),
        ("Node_B", "Node_C"),
        ("Node_B", "Node_E"),
        ("Node_C", "Node_F"),
        ("Node_D", "Node_E"),
        ("Node_E", "Node_F"),
    ]
    
    for n1, n2 in connections:
        network.connect_nodes(n1, n2)
    
    print("\n--- BEFORE NODE FAILURE ---")
    network.print_topology()
    
    # Send message A -> F (should go through E)
    message1 = EMTPMessage(
        message_id=str(uuid.uuid4()),
        source_id="Node_A",
        destination_id="Node_F",
        priority=Priority.HIGH,
        payload="Test message before failure"
    )
    network.send_message(message1)
    
    # Simulate Node E failure
    network.disconnect_node("Node_E")
    
    print("\n--- AFTER NODE E FAILURE ---")
    network.print_topology()
    
    # Send another message (should reroute)
    message2 = EMTPMessage(
        message_id=str(uuid.uuid4()),
        source_id="Node_A",
        destination_id="Node_F",
        priority=Priority.HIGH,
        payload="Test message after Node E failure"
    )
    network.send_message(message2)
    
    network.print_statistics()


def demo_priority_system():
    """Demo: Priority-based message handling"""
    print("\n" + "="*60)
    print("DEMO 4: Priority System")
    print("="*60)
    
    network = MeshNetwork()
    
    # Create simple 3-node network
    nodes = [
        MeshNode("Node_A"),
        MeshNode("Node_B"),
        MeshNode("Node_C"),
    ]
    
    for node in nodes:
        network.add_node(node)
    
    network.connect_nodes("Node_A", "Node_B")
    network.connect_nodes("Node_B", "Node_C")
    
    # Send messages with different priorities
    priorities = [
        (Priority.NORMAL, "Regular status update"),
        (Priority.MEDIUM, "Need water supply"),
        (Priority.HIGH, "Injured person needs help"),
        (Priority.CRITICAL, "URGENT: Building collapse!"),
    ]
    
    for priority, payload in priorities:
        message = EMTPMessage(
            message_id=str(uuid.uuid4()),
            source_id="Node_A",
            destination_id="BROADCAST",
            priority=priority,
            payload=payload
        )
        network.send_message(message)
        time.sleep(0.2)
    
    network.print_statistics()


# ==================== Main ====================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   Emergency Mesh Network Simulator                     ║
    ║   Infrastructure-Free Communication System             ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Run all demos
    demo_basic_routing()
    time.sleep(1)
    
    demo_mesh_topology()
    time.sleep(1)
    
    demo_node_failure()
    time.sleep(1)
    
    demo_priority_system()
    
    print("\n" + "="*60)
    print("✓ ALL SIMULATIONS COMPLETE")
    print("="*60)
