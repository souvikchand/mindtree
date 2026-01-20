# 🌳 MindTree - Tree Making App

A Streamlit-based interactive web application for creating and managing tree structures with nodes and connections.

## Features

- **Add Nodes**: Create nodes with custom labels and optional parent connections
- **Delete Nodes**: Remove nodes from the tree
- **Add Connections**: Create directed edges between nodes to build tree relationships
- **Delete Connections**: Remove specific connections between nodes
- **Visual Rendering**: Interactive graph visualization using NetworkX and Matplotlib
- **Tree Information**: Real-time statistics about nodes and connections
- **Session Persistence**: Tree structure is maintained during the session

## Installation

1. Clone the repository:
```bash
git clone https://github.com/souvikchand/mindtree.git
cd mindtree
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

The app will open in your default web browser at `http://localhost:8501`

## How to Use

### Adding Nodes
1. Enter a label for your node in the "Node Label" field
2. Optionally select a parent node to automatically create a connection
3. Click "Add Node"

### Deleting Nodes
1. Select a node from the "Select Node to Delete" dropdown
2. Click "Delete Node"
3. Note: Deleting a node also removes all its connections

### Adding Connections
1. Select the parent node from "From (Parent)" dropdown
2. Select the child node from "To (Child)" dropdown
3. Click "Add Connection"

### Deleting Connections
1. Select a connection from the "Select Connection to Delete" dropdown
2. Click "Delete Connection"

### Clear All
Click "Clear All Nodes and Connections" to reset the entire tree

## Screenshots

### Initial State
![MindTree Initial State](https://github.com/user-attachments/assets/7e964560-1d79-44da-9e9d-c52b763ba562)

### Tree with Nodes and Connections
![MindTree with Tree](https://github.com/user-attachments/assets/033f30b0-b726-45ee-b9b0-be0caa5e14f4)

## Project Structure

```
mindtree/
├── streamlit_app.py    # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Dependencies

- streamlit >= 1.28.0
- networkx >= 3.1
- matplotlib >= 3.7.0

## License

This project is open source and available under the MIT License.
