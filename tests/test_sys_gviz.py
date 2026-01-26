from networkx.drawing.nx_pydot import graphviz_layout
import networkx as nx

G = nx.DiGraph()
G.add_edge("A", "B")
print(graphviz_layout(G, prog="dot"))
