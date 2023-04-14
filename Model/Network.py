import numpy as np
import json
import networkx as nx
from .states import States

class Network:
    """
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
    def __init__(self, mode:int, file_name:str="", net_size:int=0) -> None:
        if mode==0:
            self.load_from_json_prob(self, file_name)
        elif mode==1:
            self.load_struc_from_json(self, file_name)
        else:
            self.generate_random(self, net_size)

    def load_from_json_prob(self, file_name):
        pass

    def load_struc_from_json(self, file_name):
        pass

    def generate_random(self, net_size):
        pass