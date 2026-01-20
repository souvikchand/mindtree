# 🌳 MindTree - Tree Making Application

A versatile web-based tree making application for creating mind maps, family trees, and organizational charts.

## Features

- **Multiple Tree Types**: Create mind maps for study topics, family trees, or organization charts
- **Interactive Interface**: 
  - Click to select nodes
  - Double-click to edit node text and colors
  - Drag nodes to reposition them
- **Template System**: Quick start with pre-built templates for different use cases
- **Persistence**: Save and load trees from browser local storage
- **Export**: Export trees as JSON files for backup or sharing
- **Customization**: Change node colors and text to suit your needs

## Usage

1. **Open the Application**: Simply open `index.html` in a web browser
2. **Create a Tree**:
   - Click "Add Root Node" to create the main node
   - Select a node and click "Add Child Node" to add children
   - Double-click nodes to edit their text and color
   - Drag nodes to reposition them
3. **Use Templates**: Select a template type (Mind Map, Family Tree, or Organization Chart) and click "Load Template"
4. **Save Your Work**: Click "Save Tree" to save to browser storage or "Export as JSON" to download

## Templates

### Mind Map
Perfect for organizing study topics, brainstorming sessions, or project planning. Features a central topic with multiple subtopics branching out.

### Family Tree
Ideal for mapping family relationships across generations. Start with grandparents and work down through the family line.

### Organization Chart
Great for visualizing team structures and reporting hierarchies in organizations.

## Controls

- **Add Root Node**: Create the first node in your tree
- **Add Child Node**: Add a child to the selected node
- **Delete Node**: Remove the selected node and all its children
- **Save Tree**: Save to browser local storage
- **Load Tree**: Load previously saved tree
- **Export as JSON**: Download tree as JSON file
- **Clear All**: Remove all nodes and start fresh

## Technical Details

Built with vanilla HTML, CSS, and JavaScript. No external dependencies required. Uses SVG for rendering the tree visualization.

## Browser Compatibility

Works on all modern browsers supporting SVG and ES6 JavaScript features.

## License

MIT License - Feel free to use and modify as needed.
