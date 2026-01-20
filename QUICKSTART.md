# Quick Start Guide

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## Quick Tutorial

### Step 1: Add Your First Node (Root)
1. Enter "Root" in the Node Label field
2. Leave Parent Node as "None (Root Node)"
3. Click "Add Node"

### Step 2: Add Child Nodes
1. Enter "Child 1" in the Node Label field
2. Select "0: Root" from the Parent Node dropdown
3. Click "Add Node"
4. Repeat for "Child 2"

### Step 3: Add a Grandchild
1. Enter "Grandchild" in the Node Label field
2. Select "1: Child 1" from the Parent Node dropdown
3. Click "Add Node"

### Step 4: Add Manual Connection
1. Scroll to "Add Connection" section
2. Select "From (Parent)" node
3. Select "To (Child)" node
4. Click "Add Connection"

### Step 5: Delete a Connection
1. Scroll to "Delete Connection" section
2. Select the connection to remove (e.g., "0 → 1")
3. Click "Delete Connection"

### Step 6: Delete a Node
1. Scroll to "Delete Node" section
2. Select the node to remove
3. Click "Delete Node"
   (Note: This will also remove all connections to/from this node)

### Step 7: Clear Everything
1. Scroll to "Clear All" section
2. Click "Clear All Nodes and Connections"
3. Confirm the action

## Tips
- The tree visualization updates automatically after each operation
- Node IDs are assigned sequentially starting from 0
- You can see in/out degree for each node in the Information panel
- The app uses session state, so your tree persists during the session
- Refreshing the browser will reset the tree
