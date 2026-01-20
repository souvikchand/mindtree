// MindTree Application - Tree Making App
class TreeNode {
    constructor(id, text, x, y, color = '#4CAF50') {
        this.id = id;
        this.text = text;
        this.x = x;
        this.y = y;
        this.color = color;
        this.children = [];
        this.parent = null;
    }

    addChild(child) {
        this.children.push(child);
        child.parent = this;
    }

    removeChild(child) {
        const index = this.children.indexOf(child);
        if (index > -1) {
            this.children.splice(index, 1);
            child.parent = null;
        }
    }
}

class MindTree {
    constructor() {
        this.nodes = [];
        this.selectedNode = null;
        this.nodeIdCounter = 0;
        this.isDragging = false;
        this.dragNode = null;
        this.offset = { x: 0, y: 0 };

        this.svg = document.getElementById('treeSvg');
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Toolbar buttons
        document.getElementById('addRoot').addEventListener('click', () => this.addRootNode());
        document.getElementById('addChild').addEventListener('click', () => this.addChildNode());
        document.getElementById('deleteNode').addEventListener('click', () => this.deleteSelectedNode());
        document.getElementById('save').addEventListener('click', () => this.saveTree());
        document.getElementById('load').addEventListener('click', () => this.loadTree());
        document.getElementById('export').addEventListener('click', () => this.exportTree());
        document.getElementById('clear').addEventListener('click', () => this.clearAll());
        document.getElementById('loadTemplate').addEventListener('click', () => this.loadTemplate());

        // Edit panel buttons
        document.getElementById('saveEdit').addEventListener('click', () => this.saveNodeEdit());
        document.getElementById('cancelEdit').addEventListener('click', () => this.cancelNodeEdit());

        // SVG events
        this.svg.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.svg.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.svg.addEventListener('mouseup', () => this.handleMouseUp());
        this.svg.addEventListener('mouseleave', () => this.handleMouseUp());
    }

    addRootNode() {
        if (this.nodes.length > 0) {
            alert('Root node already exists! Add child nodes instead.');
            return;
        }
        const node = new TreeNode(this.nodeIdCounter++, 'Root', 400, 100);
        this.nodes.push(node);
        this.render();
    }

    addChildNode() {
        if (!this.selectedNode) {
            alert('Please select a parent node first!');
            return;
        }
        const parent = this.selectedNode;
        const childCount = parent.children.length;
        const spacing = 150;
        const offset = (childCount - 0) * spacing - (childCount * spacing) / 2;
        
        const child = new TreeNode(
            this.nodeIdCounter++,
            'New Node',
            parent.x + offset,
            parent.y + 120,
            parent.color
        );
        
        parent.addChild(child);
        this.nodes.push(child);
        this.render();
    }

    deleteSelectedNode() {
        if (!this.selectedNode) {
            alert('Please select a node to delete!');
            return;
        }

        if (!this.selectedNode.parent) {
            alert('Cannot delete root node! Use Clear All instead.');
            return;
        }

        const nodeToDelete = this.selectedNode;
        
        // Remove from parent
        if (nodeToDelete.parent) {
            nodeToDelete.parent.removeChild(nodeToDelete);
        }

        // Remove node and all its descendants
        const nodesToRemove = [nodeToDelete];
        while (nodesToRemove.length > 0) {
            const node = nodesToRemove.pop();
            nodesToRemove.push(...node.children);
            const index = this.nodes.indexOf(node);
            if (index > -1) {
                this.nodes.splice(index, 1);
            }
        }

        this.selectedNode = null;
        this.render();
    }

    clearAll() {
        if (confirm('Are you sure you want to clear all nodes?')) {
            this.nodes = [];
            this.selectedNode = null;
            this.nodeIdCounter = 0;
            this.render();
        }
    }

    saveTree() {
        if (this.nodes.length === 0) {
            alert('No tree to save!');
            return;
        }
        const treeData = this.serializeTree();
        localStorage.setItem('mindtree_saved', JSON.stringify(treeData));
        alert('Tree saved successfully!');
    }

    loadTree() {
        const savedData = localStorage.getItem('mindtree_saved');
        if (!savedData) {
            alert('No saved tree found!');
            return;
        }
        
        if (confirm('This will replace the current tree. Continue?')) {
            this.deserializeTree(JSON.parse(savedData));
            this.render();
            alert('Tree loaded successfully!');
        }
    }

    exportTree() {
        if (this.nodes.length === 0) {
            alert('No tree to export!');
            return;
        }
        const treeData = this.serializeTree();
        const dataStr = JSON.stringify(treeData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'mindtree_export.json';
        link.click();
        URL.revokeObjectURL(url);
    }

    serializeTree() {
        return {
            nodes: this.nodes.map(node => ({
                id: node.id,
                text: node.text,
                x: node.x,
                y: node.y,
                color: node.color,
                parentId: node.parent ? node.parent.id : null
            })),
            nodeIdCounter: this.nodeIdCounter
        };
    }

    deserializeTree(data) {
        this.nodes = [];
        this.selectedNode = null;
        this.nodeIdCounter = data.nodeIdCounter;

        const nodeMap = new Map();
        
        // Create all nodes
        data.nodes.forEach(nodeData => {
            const node = new TreeNode(
                nodeData.id,
                nodeData.text,
                nodeData.x,
                nodeData.y,
                nodeData.color
            );
            this.nodes.push(node);
            nodeMap.set(node.id, node);
        });

        // Rebuild parent-child relationships
        data.nodes.forEach(nodeData => {
            if (nodeData.parentId !== null) {
                const parent = nodeMap.get(nodeData.parentId);
                const child = nodeMap.get(nodeData.id);
                if (parent && child) {
                    parent.addChild(child);
                }
            }
        });
    }

    loadTemplate() {
        const templateType = document.getElementById('treeType').value;
        
        if (this.nodes.length > 0 && !confirm('This will replace the current tree. Continue?')) {
            return;
        }

        this.nodes = [];
        this.selectedNode = null;
        this.nodeIdCounter = 0;

        switch (templateType) {
            case 'mindmap':
                this.createMindMapTemplate();
                break;
            case 'family':
                this.createFamilyTreeTemplate();
                break;
            case 'org':
                this.createOrgChartTemplate();
                break;
        }

        this.render();
    }

    createMindMapTemplate() {
        const root = new TreeNode(this.nodeIdCounter++, 'Main Topic', 400, 100, '#FF6B6B');
        this.nodes.push(root);

        const topics = [
            { text: 'Subtopic 1', color: '#4ECDC4' },
            { text: 'Subtopic 2', color: '#45B7D1' },
            { text: 'Subtopic 3', color: '#FFA07A' }
        ];

        topics.forEach((topic, i) => {
            const x = 400 + (i - 1) * 200;
            const child = new TreeNode(this.nodeIdCounter++, topic.text, x, 220, topic.color);
            root.addChild(child);
            this.nodes.push(child);

            // Add sub-items
            const subItem = new TreeNode(this.nodeIdCounter++, 'Detail', x, 340, topic.color);
            child.addChild(subItem);
            this.nodes.push(subItem);
        });
    }

    createFamilyTreeTemplate() {
        const root = new TreeNode(this.nodeIdCounter++, 'Grandparents', 400, 100, '#8B4513');
        this.nodes.push(root);

        const parents = new TreeNode(this.nodeIdCounter++, 'Parents', 400, 220, '#D2691E');
        root.addChild(parents);
        this.nodes.push(parents);

        const children = [
            { text: 'Child 1', x: 300 },
            { text: 'Child 2', x: 400 },
            { text: 'Child 3', x: 500 }
        ];

        children.forEach(child => {
            const node = new TreeNode(this.nodeIdCounter++, child.text, child.x, 340, '#F4A460');
            parents.addChild(node);
            this.nodes.push(node);
        });
    }

    createOrgChartTemplate() {
        const ceo = new TreeNode(this.nodeIdCounter++, 'CEO', 400, 100, '#2C3E50');
        this.nodes.push(ceo);

        const managers = [
            { text: 'Manager 1', x: 250 },
            { text: 'Manager 2', x: 400 },
            { text: 'Manager 3', x: 550 }
        ];

        managers.forEach(mgr => {
            const manager = new TreeNode(this.nodeIdCounter++, mgr.text, mgr.x, 220, '#34495E');
            ceo.addChild(manager);
            this.nodes.push(manager);

            // Add employees
            const emp1 = new TreeNode(this.nodeIdCounter++, 'Employee', mgr.x - 60, 340, '#7F8C8D');
            const emp2 = new TreeNode(this.nodeIdCounter++, 'Employee', mgr.x + 60, 340, '#7F8C8D');
            manager.addChild(emp1);
            manager.addChild(emp2);
            this.nodes.push(emp1);
            this.nodes.push(emp2);
        });
    }

    handleMouseDown(e) {
        const clickedElement = e.target.closest('.tree-node');
        if (!clickedElement) return;

        const nodeId = parseInt(clickedElement.getAttribute('data-node-id'));
        const node = this.nodes.find(n => n.id === nodeId);

        if (e.detail === 2) {
            // Double click - edit
            this.editNode(node);
        } else {
            // Single click - select and prepare for drag
            this.selectNode(node);
            this.isDragging = true;
            this.dragNode = node;
            const pt = this.svg.createSVGPoint();
            pt.x = e.clientX;
            pt.y = e.clientY;
            const svgPt = pt.matrixTransform(this.svg.getScreenCTM().inverse());
            this.offset.x = svgPt.x - node.x;
            this.offset.y = svgPt.y - node.y;
        }
    }

    handleMouseMove(e) {
        if (!this.isDragging || !this.dragNode) return;

        const pt = this.svg.createSVGPoint();
        pt.x = e.clientX;
        pt.y = e.clientY;
        const svgPt = pt.matrixTransform(this.svg.getScreenCTM().inverse());
        
        this.dragNode.x = svgPt.x - this.offset.x;
        this.dragNode.y = svgPt.y - this.offset.y;
        
        this.render();
    }

    handleMouseUp() {
        this.isDragging = false;
        this.dragNode = null;
    }

    selectNode(node) {
        this.selectedNode = node;
        this.render();
    }

    editNode(node) {
        this.selectedNode = node;
        document.getElementById('nodeText').value = node.text;
        document.getElementById('nodeColor').value = node.color;
        document.getElementById('editPanel').classList.remove('hidden');
    }

    saveNodeEdit() {
        if (!this.selectedNode) return;
        
        this.selectedNode.text = document.getElementById('nodeText').value || 'Node';
        this.selectedNode.color = document.getElementById('nodeColor').value;
        
        document.getElementById('editPanel').classList.add('hidden');
        this.render();
    }

    cancelNodeEdit() {
        document.getElementById('editPanel').classList.add('hidden');
    }

    render() {
        // Clear SVG
        while (this.svg.lastChild && this.svg.lastChild.tagName !== 'defs') {
            this.svg.removeChild(this.svg.lastChild);
        }

        // Draw links first (so they appear behind nodes)
        this.nodes.forEach(node => {
            node.children.forEach(child => {
                this.drawLink(node, child);
            });
        });

        // Draw nodes
        this.nodes.forEach(node => {
            this.drawNode(node);
        });
    }

    drawLink(parent, child) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const d = `M ${parent.x} ${parent.y + 25} L ${child.x} ${child.y - 25}`;
        path.setAttribute('d', d);
        path.setAttribute('class', 'tree-link');
        path.setAttribute('marker-end', 'url(#arrowhead)');
        this.svg.appendChild(path);
    }

    drawNode(node) {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'tree-node');
        g.setAttribute('data-node-id', node.id);
        g.setAttribute('transform', `translate(${node.x}, ${node.y})`);

        if (this.selectedNode === node) {
            g.classList.add('selected');
        }

        // Node background
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', -70);
        rect.setAttribute('y', -25);
        rect.setAttribute('width', 140);
        rect.setAttribute('height', 50);
        rect.setAttribute('rx', 8);
        rect.setAttribute('fill', node.color);
        rect.setAttribute('stroke', '#333');
        rect.setAttribute('stroke-width', 2);
        g.appendChild(rect);

        // Node text
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', 0);
        text.setAttribute('y', 5);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('fill', 'white');
        text.setAttribute('font-size', '14');
        text.setAttribute('font-weight', 'bold');
        text.textContent = node.text.length > 15 ? node.text.substring(0, 15) + '...' : node.text;
        g.appendChild(text);

        this.svg.appendChild(g);
    }
}

// Initialize the application
const app = new MindTree();
