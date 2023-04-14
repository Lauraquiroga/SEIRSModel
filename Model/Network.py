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
        self.init_states = np.zeros((4,self.n), dtype=float)

        if mode==0:
            self.load_from_json_prob(self, file_name)
        elif mode==1:
            self.load_struc_from_json(self, file_name)
        else:
            self.generate_random(self, net_size)


    def load_from_json_prob(self, file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            self.n = len(data)
            self.adjMatrix = np.zeros((self.n,self.n), dtype = int)
            for i in range(self.n):
                self.adjMatrix[i,:] = data[i]['adjList']
            # graph:= graph that represents the network (created from adjMatrix)
            self.graph = nx.Graph(self.adjMatrix)
            # initialize probabilities
            for node in range(self.n):
                self.init_states[States.S.value][node]=data[node]['S']
                self.init_states[States.E.value][node]=data[node]['E']
                self.init_states[States.I.value][node]=data[node]['I']
                self.init_states[States.R.value][node]=data[node]['R']

    def load_struc_from_json(self, file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            self.n = len(data)
            self.adjMatrix = np.zeros((self.n,self.n), dtype = int)
            for i in range(self.n):
                self.adjMatrix[i,:] = data[i]['adjList']
            # graph:= graph that represents the network (created from adjMatrix)
            self.graph = nx.Graph(self.adjMatrix)

    def generate_random(self, net_size):
        """
        Generate random adjacency matrix making sure it creates a connected graph
        """
        self.n = net_size
        self.adjMatrix = np.zeros((self.n,self.n), dtype = int)

        #########Actually generate

    def generate_positions(self):
        """
        Generate node positions for graphic display
        """
        pass

    def initialize_probs(self, infected_node):
        """
        Initialize the probabilities to be in every state
        for each of the nodes
        infected_node: node where the infection starts
        """
        self.init_states[States.S.value]=np.ones(self.n, dtype=float)
        self.init_states[States.S.value][infected_node]=0
        self.init_states[States.I.value][infected_node]=1