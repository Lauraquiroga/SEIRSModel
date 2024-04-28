# --------------------------------------------------------------------------
# Network class: IoT device network construction
# Author: Laura Quiroga
# --------------------------------------------------------------------------

import numpy as np
import json
import networkx as nx
import matplotlib.pyplot as plt
from .states import States

class Network:

    def __init__(self, mode:int, file_name:str="", net_size:int=0, density:float=0.0) -> None:
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
            self.generate_random(net_size, density)


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
            raise Exception(f"Unable to parse the json file {file_name}")

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
            raise Exception(f"Unable to parse the json file {file_name}")

    def generate_random(self, net_size, density):
        """
        Generate random adjacency matrix making sure it creates a connected graph
        net_size:= the number of nodes (devices in the network)
        density:= # edges / max # of edges
        (If the given density indicates that the created network should have less than the
         minimum number of edges required to create a connected graph, the given density is replaced
         by density = net_size-1 / max # of edges)
        """
        self.n = net_size
        # Calculate the minimum number of edges required for a connected graph
        min_edges = self.n - 1
        # Calculate the maximum possible number of edges
        max_edges = (self.n * (self.n - 1)) // 2 #Floor division
        # Calculate the number of edges based on the desired density
        num_edges = int(density * max_edges)
        # Ensure that the number of edges is at least equal to the minimum required
        num_edges = max(num_edges, min_edges)

        self.init_states = np.zeros((4,self.n), dtype=float)
        self.adjMatrix =  np.zeros((self.n, self.n), dtype=int)
        last_n_connected=False
        for i in range(self.n-1):
            j = np.random.randint(i+1, self.n)
            if j==self.n-1:
                last_n_connected=True
            self.adjMatrix[i,j]=1
            self.adjMatrix[j,i]=1
        if not last_n_connected:
            j = np.random.randint(0, self.n-1)
            self.adjMatrix[self.n-1,j]=1
            self.adjMatrix[j,self.n-1]=1

        # Randomly add the remaining edges while keeping the graph connected
        remaining_edges = num_edges - (self.n - 1)

        while remaining_edges > 0:
            i = np.random.randint(0, self.n-1)
            j = np.random.randint(i+1, self.n)
            
            if self.adjMatrix[i, j] == 0:
                self.adjMatrix[i, j] = 1
                self.adjMatrix[j, i] = 1
                remaining_edges -= 1

        # Initialize graph from adjacency matrux
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

    def draw_graph_structure(self):
        """
        Plot the graph structure
        """
        fig = plt.figure(figsize=(6, 6))
        nx.draw(self.graph,  with_labels=True)
        plt.axis("equal")
        plt.close()
        return fig
