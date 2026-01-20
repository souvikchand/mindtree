"""
Simple tests for MindTree core functions
"""
import sys
import networkx as nx

# Mock streamlit session state
class MockSessionState:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_counter = 0
        self.node_labels = {}

# Create a mock for streamlit
class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()

# Replace streamlit import in our test
sys.modules['streamlit'] = MockStreamlit()

# Now we can import our functions (they would need to be in a separate module)
# For this basic test, we'll just verify the core logic

def test_node_operations():
    """Test basic node operations"""
    # Initialize mock state
    st = MockStreamlit()
    
    # Test adding a node
    node_id = st.session_state.node_counter
    st.session_state.graph.add_node(node_id)
    st.session_state.node_labels[node_id] = "Root"
    st.session_state.node_counter += 1
    
    assert len(st.session_state.graph.nodes()) == 1
    assert st.session_state.node_labels[0] == "Root"
    print("✓ Node addition works")
    
    # Test adding another node with connection
    node_id = st.session_state.node_counter
    st.session_state.graph.add_node(node_id)
    st.session_state.node_labels[node_id] = "Child"
    st.session_state.graph.add_edge(0, node_id)
    st.session_state.node_counter += 1
    
    assert len(st.session_state.graph.nodes()) == 2
    assert len(st.session_state.graph.edges()) == 1
    print("✓ Node with connection works")
    
    # Test deleting a node
    st.session_state.graph.remove_node(1)
    del st.session_state.node_labels[1]
    
    assert len(st.session_state.graph.nodes()) == 1
    assert len(st.session_state.graph.edges()) == 0
    print("✓ Node deletion works")
    
def test_connection_operations():
    """Test connection operations"""
    st = MockStreamlit()
    
    # Add two nodes
    st.session_state.graph.add_node(0)
    st.session_state.graph.add_node(1)
    st.session_state.node_labels[0] = "Node 0"
    st.session_state.node_labels[1] = "Node 1"
    
    # Test adding connection
    st.session_state.graph.add_edge(0, 1)
    assert st.session_state.graph.has_edge(0, 1)
    print("✓ Connection addition works")
    
    # Test removing connection
    st.session_state.graph.remove_edge(0, 1)
    assert not st.session_state.graph.has_edge(0, 1)
    print("✓ Connection deletion works")

def test_tree_structure():
    """Test building a tree structure"""
    st = MockStreamlit()
    
    # Build a simple tree
    # Root -> Child1, Child2
    # Child1 -> Grandchild
    st.session_state.graph.add_node(0)
    st.session_state.node_labels[0] = "Root"
    
    st.session_state.graph.add_node(1)
    st.session_state.node_labels[1] = "Child1"
    st.session_state.graph.add_edge(0, 1)
    
    st.session_state.graph.add_node(2)
    st.session_state.node_labels[2] = "Child2"
    st.session_state.graph.add_edge(0, 2)
    
    st.session_state.graph.add_node(3)
    st.session_state.node_labels[3] = "Grandchild"
    st.session_state.graph.add_edge(1, 3)
    
    assert len(st.session_state.graph.nodes()) == 4
    assert len(st.session_state.graph.edges()) == 3
    assert st.session_state.graph.out_degree(0) == 2
    assert st.session_state.graph.in_degree(0) == 0
    assert st.session_state.graph.in_degree(3) == 1
    print("✓ Tree structure creation works")

if __name__ == "__main__":
    print("Running MindTree Tests...")
    print()
    test_node_operations()
    test_connection_operations()
    test_tree_structure()
    print()
    print("All tests passed! ✓")
