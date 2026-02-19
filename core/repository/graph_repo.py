from typing import Dict, List
from uuid import UUID

from core.schemas.node import Node
from core.schemas.edge import Edge


class GraphRepository:
    """
    In-memory graph repository.
    Acts as a lightweight graph database abstraction.
    manages nodes and edges within a specific graph context.

    NOTE:
    GraphRepository currently supports create/read operations only.
    Mutation (update/delete) will be introduced once graph edit
    semantics and consistency rules are finalized.
    TASK:
    - Implement mutation operations with proper consistency checks.
    
    NOTE:
    This repository is NOT thread-safe by design.
    In Streamlit, each user session must maintain
    its own repository instance (e.g. via st.session_state).
    TASK:
    - Consider thread-safety if used in multi-threaded environments.
    """

    def __init__(self, graph_id:UUID) -> None:
        self.graph_id = graph_id   
        # Primary storage
        self._nodes: Dict[UUID, Node] = {}
        self._edges: Dict[UUID, Edge] = {}

        # Adjacency list: node_id -> list of connected node_ids
        self._adjacency: Dict[UUID, List[UUID]] = {}
        # self._reverse_adjacency: Dict[UUID, List[UUID]] = {}  # for future use 

    # ---------- Node operations ----------

    def add_node(self, node: Node) -> None:
        if node.graph_id != self.graph_id:
            raise ValueError(f"Node graph_id '{node.graph_id}' does not match repository graph_id '{self.graph_id}'")
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
        # edge validation checks
        if edge.graph_id != self.graph_id:
            raise ValueError(f"Edge graph_id '{edge.graph_id}' does not match repository graph_id '{self.graph_id}'")
        
        if edge.edge_id in self._edges:
            raise ValueError(f"Edge with id '{edge.edge_id}' already exists")

        if edge.source_node_id not in self._nodes:
            raise ValueError(f"Source node '{edge.source_node_id}' does not exist")

        if edge.target_node_id not in self._nodes:
            raise ValueError(f"Target node '{edge.target_node_id}' does not exist")
        
        # For simplicity, we disallow self-loops in this graph implementation.
        if edge.source_node_id == edge.target_node_id:
            raise ValueError("Self-loops are not allowed in this graph")

        self._edges[edge.edge_id] = edge
        self._adjacency[edge.source_node_id].append(edge.target_node_id)

    
    def list_edges(self) -> List[Edge]:
        return list(self._edges.values())
    
    
    def get_edge(self, edge_id: UUID) -> Edge:
        if edge_id not in self._edges:
            raise KeyError(f"Edge '{edge_id}' not found")

        return self._edges[edge_id]

    # ---------- Graph queries ----------

    def get_neighbors(self, node_id: UUID) -> List[Node]:
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found")

        neighbor_ids = self._adjacency.get(node_id, [])
        return [self._nodes[n_id] for n_id in neighbor_ids]

    def get_graph_snapshot(self) -> dict:
        """
        Returns a JSON-serializable snapshot of the graph.
        Useful for debugging and testing.
        """
        return {
            #"nodes": list(self._nodes.keys()),
            "nodes": [str(node_id) for node_id in self._nodes.keys()],
            "edges": [
                {
                    "id": str(e.edge_id),
                    "source": str(e.source_node_id),
                    "target": str(e.target_node_id),
                    "label": e.label,
                }
                for e in self._edges.values()
            ],
        }
