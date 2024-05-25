# Add friends = Add Node into graph
# Delete friends = Remove Node 
# Show friends list = Show adjacency list (*)
# Suggestion for adding friends = Show adjacency list of (*)
import networkx as nx
import matplotlib.pyplot as plt

class NetworkGraph:
    def __init__(self):
        self.adjacency_list = {} # Ma trận kề

    def add_edge(self, node1, node2):
        if node1 not in self.adjacency_list: # If node 1 is not belonging to matrix
            self.adjacency_list[node1] = [] # create NONE adjacency
        if node2 not in self.adjacency_list:
            self.adjacency_list[node2] = []
        
        self.adjacency_list[node1].append(node2) # Insert node 2 into node1's adjacency list
        self.adjacency_list[node2].append(node1)

    def __repr__(self):
        return str(self.adjacency_list)
    
    def draw(self):
        G = nx.Graph()
        for node, neighbors in self.adjacency_list.items(): # neighbors là danh sách kề
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=15, font_weight='bold')
        plt.show()