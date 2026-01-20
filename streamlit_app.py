"""
MindTree - A Streamlit app for creating and managing tree structures
"""
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
if 'node_counter' not in st.session_state:
    st.session_state.node_counter = 0
if 'node_labels' not in st.session_state:
    st.session_state.node_labels = {}

# Node Management Functions
def add_node(label: str, parent_id: Optional[int] = None) -> int:
    """
    Add a new node to the tree.
    
    Args:
        label: The label/text for the node
        parent_id: Optional parent node ID to create a connection
        
    Returns:
        The ID of the newly created node
    """
    node_id = st.session_state.node_counter
    st.session_state.graph.add_node(node_id)
    st.session_state.node_labels[node_id] = label
    st.session_state.node_counter += 1
    
    # If parent is specified, add connection
    if parent_id is not None and parent_id in st.session_state.graph.nodes():
        add_connection(parent_id, node_id)
    
    return node_id

def delete_node(node_id: int) -> bool:
    """
    Delete a node from the tree.
    
    Args:
        node_id: The ID of the node to delete
        
    Returns:
        True if successful, False otherwise
    """
    if node_id in st.session_state.graph.nodes():
        st.session_state.graph.remove_node(node_id)
        if node_id in st.session_state.node_labels:
            del st.session_state.node_labels[node_id]
        return True
    return False

# Connection Management Functions
def add_connection(parent_id: int, child_id: int) -> bool:
    """
    Add a connection (edge) between two nodes.
    
    Args:
        parent_id: The ID of the parent node
        child_id: The ID of the child node
        
    Returns:
        True if successful, False otherwise
    """
    if (parent_id in st.session_state.graph.nodes() and 
        child_id in st.session_state.graph.nodes()):
        st.session_state.graph.add_edge(parent_id, child_id)
        return True
    return False

def delete_connection(parent_id: int, child_id: int) -> bool:
    """
    Delete a connection (edge) between two nodes.
    
    Args:
        parent_id: The ID of the parent node
        child_id: The ID of the child node
        
    Returns:
        True if successful, False otherwise
    """
    if st.session_state.graph.has_edge(parent_id, child_id):
        st.session_state.graph.remove_edge(parent_id, child_id)
        return True
    return False

def get_all_nodes() -> List[Tuple[int, str]]:
    """
    Get all nodes with their labels.
    
    Returns:
        List of tuples (node_id, label)
    """
    return [(node_id, st.session_state.node_labels.get(node_id, f"Node {node_id}"))
            for node_id in st.session_state.graph.nodes()]

def get_all_connections() -> List[Tuple[int, int]]:
    """
    Get all connections in the tree.
    
    Returns:
        List of tuples (parent_id, child_id)
    """
    return list(st.session_state.graph.edges())

# Visualization Functions
def render_tree():
    """
    Render the tree structure using matplotlib and networkx.
    """
    if len(st.session_state.graph.nodes()) == 0:
        st.info("No nodes to display. Add a node to get started!")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Try to use hierarchical layout if it's a tree
    try:
        # Find root nodes (nodes with no incoming edges)
        root_nodes = [node for node in st.session_state.graph.nodes() 
                     if st.session_state.graph.in_degree(node) == 0]
        
        if root_nodes:
            # Use hierarchical layout
            pos = nx.spring_layout(st.session_state.graph, k=2, iterations=50)
        else:
            # Use spring layout for cyclic graphs
            pos = nx.spring_layout(st.session_state.graph, k=2, iterations=50)
    except:
        pos = nx.spring_layout(st.session_state.graph, k=2, iterations=50)
    
    # Draw the graph
    nx.draw(st.session_state.graph, pos, 
            labels=st.session_state.node_labels,
            with_labels=True,
            node_color='lightblue',
            node_size=2000,
            font_size=10,
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            edge_color='gray',
            width=2,
            ax=ax)
    
    plt.title("MindTree Visualization", fontsize=16, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def clear_tree():
    """Clear all nodes and connections from the tree."""
    st.session_state.graph.clear()
    st.session_state.node_labels.clear()
    st.session_state.node_counter = 0

# Main Streamlit App
def main():
    st.set_page_config(page_title="MindTree", page_icon="🌳", layout="wide")
    
    st.title("🌳 MindTree - Tree Making App")
    st.markdown("Create and manage tree structures with nodes and connections")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        # Add Node Section
        st.subheader("➕ Add Node")
        node_label = st.text_input("Node Label", key="new_node_label")
        
        # Parent selection for new node
        nodes = get_all_nodes()
        parent_options = ["None (Root Node)"] + [f"{nid}: {label}" for nid, label in nodes]
        parent_selection = st.selectbox("Parent Node", parent_options, key="parent_select")
        
        if st.button("Add Node"):
            if node_label:
                parent_id = None
                if parent_selection != "None (Root Node)":
                    parent_id = int(parent_selection.split(":")[0])
                
                new_id = add_node(node_label, parent_id)
                st.success(f"Node '{node_label}' added with ID {new_id}")
                st.rerun()
            else:
                st.error("Please enter a node label")
        
        st.divider()
        
        # Delete Node Section
        st.subheader("➖ Delete Node")
        if nodes:
            delete_options = [f"{nid}: {label}" for nid, label in nodes]
            delete_selection = st.selectbox("Select Node to Delete", delete_options, key="delete_select")
            
            if st.button("Delete Node"):
                node_id = int(delete_selection.split(":")[0])
                if delete_node(node_id):
                    st.success(f"Node {node_id} deleted")
                    st.rerun()
                else:
                    st.error("Failed to delete node")
        else:
            st.info("No nodes to delete")
        
        st.divider()
        
        # Add Connection Section
        st.subheader("🔗 Add Connection")
        if len(nodes) >= 2:
            node_options = [f"{nid}: {label}" for nid, label in nodes]
            parent_conn = st.selectbox("From (Parent)", node_options, key="parent_conn")
            child_conn = st.selectbox("To (Child)", node_options, key="child_conn")
            
            if st.button("Add Connection"):
                parent_id = int(parent_conn.split(":")[0])
                child_id = int(child_conn.split(":")[0])
                
                if parent_id == child_id:
                    st.error("Cannot connect a node to itself")
                elif add_connection(parent_id, child_id):
                    st.success(f"Connection added: {parent_id} → {child_id}")
                    st.rerun()
                else:
                    st.error("Failed to add connection")
        else:
            st.info("Need at least 2 nodes to create connections")
        
        st.divider()
        
        # Delete Connection Section
        st.subheader("✂️ Delete Connection")
        connections = get_all_connections()
        if connections:
            conn_options = [f"{p} → {c}" for p, c in connections]
            conn_selection = st.selectbox("Select Connection to Delete", conn_options, key="conn_delete")
            
            if st.button("Delete Connection"):
                parent_id, child_id = map(int, conn_selection.split(" → "))
                if delete_connection(parent_id, child_id):
                    st.success(f"Connection {parent_id} → {child_id} deleted")
                    st.rerun()
                else:
                    st.error("Failed to delete connection")
        else:
            st.info("No connections to delete")
        
        st.divider()
        
        # Clear All
        st.subheader("🗑️ Clear All")
        if st.button("Clear All Nodes and Connections", type="secondary"):
            clear_tree()
            st.success("Tree cleared")
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Tree Visualization")
        render_tree()
    
    with col2:
        st.header("Tree Information")
        
        # Display statistics
        num_nodes = len(st.session_state.graph.nodes())
        num_edges = len(st.session_state.graph.edges())
        
        st.metric("Total Nodes", num_nodes)
        st.metric("Total Connections", num_edges)
        
        # Display nodes
        if nodes:
            st.subheader("Nodes")
            for node_id, label in sorted(nodes):
                in_degree = st.session_state.graph.in_degree(node_id)
                out_degree = st.session_state.graph.out_degree(node_id)
                st.text(f"• {node_id}: {label} (in:{in_degree}, out:{out_degree})")
        
        # Display connections
        if connections:
            st.subheader("Connections")
            for parent, child in connections:
                parent_label = st.session_state.node_labels.get(parent, f"Node {parent}")
                child_label = st.session_state.node_labels.get(child, f"Node {child}")
                st.text(f"• {parent_label} → {child_label}")

if __name__ == "__main__":
    main()
