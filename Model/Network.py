import numpy as np
import networkx as nx
from .states import States

class Network:
    def __init__(self, adjMatrix: np.array, init_states: list) -> None:
        # n:= number of nodes in the network
        self.n = len(adjMatrix)
        # adjMatrix := adjacency matrix representing connection between nodes
            # adjMatrix[i][j] = 1 , i and j are neighbours
            # adjMatrix[i][j] = 0 , i and j are not neighbours
        self.adjMatrix = adjMatrix

        # graph:= graph that represents the network (created from adjMatrix)
        self.graph = nx.Graph(adjMatrix)
        

        """
        # initialize states
        for node in range(self.n):
            nx.set_node_attributes(self.graph, init_states[node], 'state')
        """