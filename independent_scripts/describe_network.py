# --------------------------------------------------------------------------
# Load radjacency matrix from file and obtain its key characteristics
# Author: Laura Quiroga
# --------------------------------------------------------------------------

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def generate_adjacency_matrix(n, d):
    """
    Generate random matrix from size and density
    """
    # Calculate the minimum number of edges required for a connected graph
    min_edges = n - 1

    # Calculate the maximum possible number of edges
    max_edges = (n * (n - 1)) // 2

    # Calculate the number of edges based on the desired density
    num_edges = int(d * max_edges)

    # Ensure that the number of edges is at least equal to the minimum required
    num_edges = max(num_edges, min_edges)

    # Generate a connected graph by ensuring there is at least one edge for each node
    adjacency_matrix = np.zeros((n, n), dtype=int)
    last_n_connected=False
    for i in range(n-1):
      j = np.random.randint(i+1, n)
      if j==n-1:
        last_n_connected=True
      adjacency_matrix[i,j]=1
      adjacency_matrix[j,i]=1
    if not last_n_connected:
      j = np.random.randint(0, n-1)
      adjacency_matrix[n-1,j]=1
      adjacency_matrix[j,n-1]=1

    # Randomly add the remaining edges while keeping the graph connected
    remaining_edges = num_edges - (n - 1)

    while remaining_edges > 0:
        i = np.random.randint(0, n-1)
        j = np.random.randint(i+1, n)

        if adjacency_matrix[i, j] == 0:
            adjacency_matrix[i, j] = 1
            adjacency_matrix[j, i] = 1
            remaining_edges -= 1

    return adjacency_matrix

def adj_matrix_from_structure(A, N):
    """
    Build adjancency matrix from given structure
    """
    adj_matrix = np.zeros((N,N))
    for node in range(N):
        adj_matrix[node,:] = A[node]
    return adj_matrix


def load_struc_from_file(file_name):
    """
    Load network from file not including initial probabilities
    """
    try:
        # Open the file
        with open(file_name, 'r') as file:
            # Read lines from the file
            lines = file.readlines()

            # Remove leading and trailing whitespace from each line
            lines = [line.strip() for line in lines]

            # Remove empty lines and lines containing only brackets
            lines = [line for line in lines if line and not line.isspace() and '[' in line and ']' in line]

            # Convert each line to a list using eval
            arrays = [eval(line) for line in lines]

            # Convert the list of lists to a numpy array
            data = np.concatenate(arrays)
            return data
    except FileNotFoundError as fnf:
        mess = str(fnf).split('] ', 1)[1]
        raise FileNotFoundError(mess)
    except Exception:
        raise Exception(f"Unable to parse the file {file_name}")
    
# -------------------------------------------------------------------------
#------------------------Build A: adjacency matrix-------------------------
# -------------------------------------------------------------------------
#N:= Number of devices in the network
# N =1000
# density of the graph edges = # of edges/ max number of edges
#density = 0.5

# OPT 1: Random network
# A = generate_adjacency_matrix(N, density)

# OPT 2: Network from structure
# AdjInfo = []
# A = adj_matrix_from_structure(AdjInfo, N)

# OPT 3: Load network from file
A = load_struc_from_file("NetworksTC/500_05/AdjMatrix_N500_D05.txt")

# --------------------------------------------------------------------------
# ----------------------------Generate Network Graph------------------------
# --------------------------------------------------------------------------
graph = nx.Graph(A)

# Paint graph according to node degree
def show_graph_degree_cmap(graph):
  g_colours = [d for (n, d) in nx.degree(graph)]
  plt.figure(figsize=(20,20))
  nx.draw(graph, node_color=g_colours, with_labels=True, cmap=plt.cm.Reds)
  plt.axis("equal")
  plt.show()

#show_graph_degree_cmap(graph)

# --------------------------------------------------------------------------
# --------Describe the netwrok through its essential characteristics--------
# --------------------------------------------------------------------------

# DENSITY
# Verification of density (not required: density used as a parameter upon creation)
number_of_nodes = graph.number_of_nodes()
print(number_of_nodes)
number_of_edges = graph.number_of_edges()
print(number_of_edges)
max_edges = (number_of_nodes*(number_of_nodes-1))/2
print(max_edges)
density = number_of_edges/max_edges

# ------------------------------------------------------------------------------
# DEGREE
# Calculate average degree of the network nodes
average_degree = sum([d for (n, d) in nx.degree(graph)]) / graph.number_of_nodes()

# Plot node degree distribution
degree_distribution ={}
max_degree = 1 #all nodes are connected
# print(nx.degree(graph))

# Create degree distribution dictionary and fin max degree
for (n, d) in nx.degree(graph):
  if(d in degree_distribution):
    degree_distribution[d]+=1
  else:
    degree_distribution[d]=1

  if(d>max_degree):
    max_degree = d

# Create arrays to plot
degree_count_list = np.zeros(max_degree+1)
degree_keys = list(degree_distribution.keys())
for degree in degree_keys:
  degree_count_list[degree] = degree_distribution[degree]

#bar graph
plt.bar(list(range(max_degree+1)), degree_count_list, color ='maroon', width = 0.4)
plt.xlabel('Node Degree')
plt.ylabel('Node Count')
plt.title('Node Degree Distribution')
plt.grid(axis='y', color='0.95')
plt.show()

# ------------------------------------------------------------------------------
# ASSORTATIVITY
assortativity_coeff = nx.degree_assortativity_coefficient(graph)

# ------------------------------------------------------------------------------
# AVERAGE PATH LENGTH
avg_shortest_path = nx.average_shortest_path_length(graph)
diameter = nx.diameter(graph)

# ------------------------------------------------------------------------------
# CLUSTERING COEFFICIENT
clustering_coeff = nx.average_clustering(graph)

# --------------------------------------------------------------------------
# ----------------------------------SUMMARY---------------------------------
# --------------------------------------------------------------------------
print(f"Size: {number_of_nodes}")
print(f"Density: {density}")
print(f"Average degree: {average_degree}")
print(f"Assortativity coefficient: {assortativity_coeff}")
print(f"Average shortest path length: {avg_shortest_path}")
print(f"Diameter: {diameter}")
print(f"Clustering coefficient: {clustering_coeff}")