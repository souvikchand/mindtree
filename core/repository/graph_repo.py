from typing import Dict, List
from uuid import UUID

from core.schemas.node import Node
from core.schemas.edge import Edge


class GraphRepository:
    """
    In-memory graph repository.
    Acts as a lightweight graph database abstraction.
    
    Thread Safety:
        This repository is NOT thread-safe. When used in a Streamlit application,
        ensure each user session has its own isolated instance by storing it in
        Streamlit's session_state.
    
    Usage with Streamlit:
        ```python
        import streamlit as st
        from core.repository import GraphRepository
        
        # Initialize repository in session state (runs once per user session)
        if "graph_repo" not in st.session_state:
            st.session_state.graph_repo = GraphRepository()
        
        # Use the session-isolated repository
        repo = st.session_state.graph_repo
        repo.add_node(node)
        ```
    
    This pattern ensures that:
        - Each user session maintains its own independent graph data
        - No race conditions occur between concurrent users
        - State persists within a session but remains isolated across sessions
    """

    def __init__(self) -> None:
        # Primary storage
        self._nodes: Dict[UUID, Node] = {}
        self._edges: Dict[UUID, Edge] = {}

        # Adjacency list: node_id -> list of connected node_ids
        self._adjacency: Dict[UUID, List[UUID]] = {}

    # ---------- Node operations ----------

    def add_node(self, node: Node) -> None:
        if node.node_id in self._nodes:
            raise ValueError(f"Node with id '{node.node_id}' already exists")

        self._nodes[node.node_id] = node
        self._adjacency[node.node_id] = []

    def get_node(self, node_id: UUID) -> Node:
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found")

        return self._nodes[node_id]

    def list_nodes(self) -> List[Node]:
        return list(self._nodes.values())

    # ---------- Edge operations ----------

    def add_edge(self, edge: Edge) -> None:
        if edge.edge_id in self._edges:
            raise ValueError(f"Edge with id '{edge.edge_id}' already exists")

        if edge.source_node_id not in self._nodes:
            raise ValueError(f"Source node '{edge.source_node_id}' does not exist")

        if edge.target_node_id not in self._nodes:
            raise ValueError(f"Target node '{edge.target_node_id}' does not exist")

        self._edges[edge.edge_id] = edge
        self._adjacency[edge.source_node_id].append(edge.target_node_id)

    def list_edges(self) -> List[Edge]:
        return list(self._edges.values())

    # ---------- Graph queries ----------

    def get_neighbors(self, node_id: UUID) -> List[Node]:
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found")

        neighbor_ids = self._adjacency.get(node_id, [])
        return [self._nodes[n_id] for n_id in neighbor_ids]

    def get_graph_snapshot(self) -> dict:
        """
        Returns a serializable snapshot of the graph.
        Useful for debugging and testing.
        """
        return {
            "nodes": list(self._nodes.keys()),
            "edges": [
                {
                    "id": e.edge_id,
                    "source": e.source_node_id,
                    "target": e.target_node_id,
                    "label": e.label,
                }
                for e in self._edges.values()
            ],
        }
