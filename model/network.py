import numpy as np
import json
import networkx as nx
from .states import States

class Network:

    def __init__(self, mode:int, file_name:str="", net_size:int=0) -> None:
        """
        n:= number of nodes in the network
        adjMatrix := adjacency matrix representing connection between nodes
            adjMatrix[i][j] = 1 , i and j are neighbours
            adjMatrix[i][j] = 0 , i and j are not neighbours
        graph:= graph that represents the network (created from adjMatrix)
        init_states = the initial probabilities for every node for every state
        """
        # mode:= the modality to initialize the network
        if mode==1:
            self.load_from_json_prob(file_name)
        elif mode==2:
            self.load_struc_from_json(file_name)
        else:
            self.generate_random(net_size)


    def load_from_json_prob(self, file_name):
        """
        Load network from json file including initial probabilities
        """
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
                self.n = len(data)
                self.adjMatrix = np.zeros((self.n,self.n), dtype = int)
                for i in range(self.n):
                    self.adjMatrix[i,:] = data[i]['adjList']
                # graph:= graph that represents the network (created from adjMatrix)
                self.graph = nx.Graph(self.adjMatrix)
                # initialize probabilities
                self.init_states = np.zeros((4,self.n), dtype=float)
                for node in range(self.n):
                    self.init_states[States.S.value][node]=data[node]['S']
                    self.init_states[States.E.value][node]=data[node]['E']
                    self.init_states[States.I.value][node]=data[node]['I']
                    self.init_states[States.R.value][node]=data[node]['R']
        except FileNotFoundError as fnf:
            mess = str(fnf).split('] ', 1)[1]
            raise FileNotFoundError(mess)
        except Exception as e:
            raise Exception(f"Unable to parse te json file {file_name}")

    def load_struc_from_json(self, file_name):
        """
        Load network from json file not including initial probabilities
        """
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
                self.n = len(data)
                self.adjMatrix = np.zeros((self.n,self.n), dtype = int)
                for i in range(self.n):
                    self.adjMatrix[i,:] = data[i]['adjList']
                # graph:= graph that represents the network (created from adjMatrix)
                self.graph = nx.Graph(self.adjMatrix)
                self.init_states = np.zeros((4,self.n), dtype=float)
        except FileNotFoundError as fnf:
            mess = str(fnf).split('] ', 1)[1]
            raise FileNotFoundError(mess)
        except Exception as e:
            raise Exception(f"Unable to parse te json file {file_name}")

    def generate_random(self, net_size):
        """
        Generate random adjacency matrix making sure it creates a connected graph
        """
        self.n = net_size
        self.init_states = np.zeros((4,self.n), dtype=float)
        self.adjMatrix = np.random.randint(2, size=(self.n, self.n))
        for i in range(self.n):
            is_connected=False
            for j in range(i,self.n):
                if i==j:
                    self.adjMatrix[i,j]=0
                else:
                    self.adjMatrix[i,j]=self.adjMatrix[j,i]
                if self.adjMatrix[i,j]==1:
                    is_connected=True
            if not is_connected and i+1<self.n:
                neighbour= np.random.randint(i+1, self.n)
                self.adjMatrix[i,neighbour]=1
                self.adjMatrix[neighbour, i]=1
        self.graph = nx.Graph(self.adjMatrix)

    def initialize_probs(self, infected_node):
        """
        Initialize the probabilities for each of the nodes for each compartment
        infected_node: node where the infection starts
        """
        self.init_states[States.S.value]=np.ones(self.n, dtype=float)
        self.init_states[States.S.value][infected_node]=0
        self.init_states[States.I.value][infected_node]=1

    def set_nodes_compartment(self,compartments:dict):
        """
        Set each node's compartment (graph's attribute)
        """
        nx.set_node_attributes(self.graph, compartments, "compartment")