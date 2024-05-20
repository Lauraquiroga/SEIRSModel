# --------------------------------------------------------------------------
# Simulation of the NIMFA SEIRS model for a homogeneous network with constant parameters
# Author: Laura Quiroga
# Test cases where Size is varied while network density and the infection parameters are kept constant
# --------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig
import heapq

# Random matrix from size and density

def generate_adjacency_matrix(n, d):
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
        i = np.random.randint(0, n)
        j = i
        while j==i:
          j = np.random.randint(0, n)

        if adjacency_matrix[i, j] == 0:
            adjacency_matrix[i, j] = 1
            adjacency_matrix[j, i] = 1
            remaining_edges -= 1

    return adjacency_matrix

#-------------------------------------------- Stanard values ------------------------------------
# Colour code for graphs
colours = {'S':'cornflowerblue', 'E':'darkorange', 'I':'red', 'R':'green'}

# Parameters
#N:= Number of devices in the network
N_values = [50, 100, 500, 1000] #500 es el mismo caso de la densiad
# density of the graph edges = # of edges/ max number of edges
density = 0.5
#beta:= Transmission rate (S->E)
beta = 0.1
#alpha:= Rate of infection upon exposure (E->I)
alpha = 0.4
#delta:= Rate of recovery (I->R)
delta = 0.1
#gamma:= Rate of re-suscptibility (R->S)
gamma = 0.6


# -------------------------Set up the model -------------------------------------
# Define the system of differential equations

# b(t) = beta* summation over j of: [(a_ij)*y_i(t)]       //using the first order approximation

def w_prime(t, w, y, z, i):
  """
  The rate of change of the probability of the node (i) being in the Exposed state:
  w'(t) = (1-w(t)-y(t)-z(t))*b(t) - alpha*w(t)
  """
  return (1-w[i]-y[i]-z[i])*beta*np.dot(A[i,:], y) - alpha*w[i]

def y_prime(t, w, y, z, i):
  """
  The rate of change of the probability of the node (i) being in the Infected state:
  y'(t) =  alpha*w(t) - delta*y(t)
  """
  return alpha * w[i] - delta * y[i]

def z_prime(t, w, y, z, i):
  """
  The rate of change of the probability of the node (i) being in the Recovered state:
  z'(t) = delta*y(t) - gamma*z(t)
  """
  return delta * y[i] - gamma * z[i]

def push_to_heap(item, top):
    """
    Reorganize the heap containing the nodes that infect the network the fastest
    """
    if len(top)<10:
      heapq.heappush(top, item)
    else:
      heapq.heappushpop(top, item)



for N in N_values:
    # Generate random matrix an save it in a file
    A = generate_adjacency_matrix(N, density)

    file_name = f"AdjMatrix_N{N}_D{str(density).replace('.', '')}"
    with open(f'{file_name}.txt', 'w') as file:
        file.write('[\n')
        for row in A:
            file.write('[' + ','.join(map(str, row))+ '],'+ '\n')
        file.write(']')

    # ----------------------- INITIAL VALUE CONDITIONS --------------------------
    #n_times := Number of time-steps
    n_times = 1000
    total_infected = [0]*N
    top_50 = []
    top_75 = []
    top_100 = []

    #---------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------RUN MODEL----------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------

    for node in range(N):
        # To maintain top
        percentage_infected = 0

        # Initial values of x,w,y,z
            #x:= probability of being in the S state for every node
            #w:= probability of being in the E state for every node
            #y:= probability of being in the I state for every node
            #z:= probability of being in the R state for every node

        # Each is a matrix of N x # of time-steps
        x = np.zeros((N, n_times))
        x[:,0]=np.ones(N)# all nodes start in susceptible state
        w = np.zeros((N, n_times))
        y = np.zeros((N, n_times))
        z = np.zeros((N, n_times))
        x[node,0] = 0
        y[node, 0] = 1  # 4th node has the virus initially
        # Total amount of devices per compartment
        totals = np.zeros((4,n_times))
        totals[0,0]=N-1
        totals[2,0]=1

        # Definition of time-steps to calculate the ODE
        min_t=0.0
        max_t=n_times/100
        t = np.linspace(min_t, max_t, n_times)
        dt = t[1] - t[0]

        # -------------------------------------------------------------------------------
        # The arrays are filled in the for loop following the formula
        # Numeric solution to the ODE using Euler's method
        for k in range(1, n_times):
            t[k] = t[k - 1] + dt
            for i in range(N):
                z[i, k] = z[i, k - 1] + dt * z_prime(t[k - 1], w[:, k - 1], y[:, k - 1],  z[:, k - 1], i)
                w[i, k] = w[i, k - 1] + dt * w_prime(t[k - 1], w[:, k - 1], y[:, k - 1],  z[:, k - 1], i)
                y[i, k] = y[i, k - 1] + dt * y_prime(t[k - 1], w[:, k - 1], y[:, k - 1],  z[:, k - 1], i)
                x[i, k] = 1 - y[i, k] - z[i, k] - w[i, k]
                if (x[i, k]<0):
                    x[i, k]=0
                #compartments = {0:'S', 1:'E', 2:'I',3:'R'}
                probabilities = [x[i, k], w[i, k], y[i, k], z[i, k]]
                compartment = probabilities.index(max(probabilities))
                totals[compartment, k]+=1

            if (totals[2,k]>=N*0.5 and percentage_infected==0):
                push_to_heap((-k, totals[2,k], node), top_50)
                percentage_infected=50
            elif (totals[2,k]>=N*0.75 and percentage_infected==50):
                push_to_heap((-k, totals[2,k], node), top_75)
                percentage_infected=75
            elif (totals[2,k]>=N and percentage_infected==75):
                push_to_heap((-k, totals[2,k], node), top_100)
                percentage_infected=100 

        # Add total infected nodes to structure for comparisson
        total_infected[node] = totals[2,:]

    file_name = f"TCnResults_N{N}_D{str(density).replace('.', '')}_a{str(alpha).replace('.', '')}_b{str(beta).replace('.', '')}_d{str(delta).replace('.', '')}_g{str(gamma).replace('.', '')}"
    with open(f'{file_name}.txt', 'w') as file:
        file.write('[\n')
        for orgNode in total_infected:
            file.write('[' + ','.join(map(str, orgNode))+ '],'+ '\n')
        file.write(']')
    file_name_top = f"TCnTop_N{N}_D{str(density).replace('.', '')}_a{str(alpha).replace('.', '')}_b{str(beta).replace('.', '')}_d{str(delta).replace('.', '')}_g{str(gamma).replace('.', '')}"
    with open(f'{file_name_top}.txt', 'w') as file:
        file.write('\n50% Top-10: '+f'{sorted(top_50)}')
        file.write('\n75% Top-10: '+f'{sorted(top_75)}')
        file.write('\n100% Top-10: '+f'{sorted(top_100)}')