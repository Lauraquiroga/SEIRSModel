import numpy as np
import networkx as nx
from .States import States

class Network:
    def __init__(self, adjMatrix: np.array, init_states: list) -> None:
        # n:= number of nodes in the network
        self.n = len(adjMatrix)
        # adjMatrix := adjacency matrix representing connection between nodes
            # adjMatrix[i][j] = 1 , i and j are neighbours
            # adjMatrix[i][j] = 0 , i and j are not neighbours
        self.adjMatrix = adjMatrix
        # graph:= graph that represents the network
        self.graph = nx.Graph()

        # add the nodes and edges to the nx graph
        for i in range(self.n):
            for j in range(i+1, self.n): #since network is undirected graph
                if self.adjMatrix[i, j] == 1:
                    self.graph.add_edge(i,j)
        
        # initialize states
        for node in range(self.n):
            nx.set_node_attributes(self.graph, init_states[node], 'state')


    # Funtion that finds list of infected neighbours for the given node(source)
    def get_infected_neigbours(self, source:int) -> list:
        neighbours = []
        #find neighbours
        for j in range(self.n):
            if self.adjMatrix[source][j]:
                neighbours.append(j)

        resp = []
        #find if infected
        for i in neighbours:
            if self.graph.nodes[i]['state'] == States.I.value:
                resp.append(i)

        return resp