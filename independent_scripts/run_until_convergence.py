# --------------------------------------------------------------------------
# Simulation of the NIMFA SEIRS model for a homogeneous network with constant parameters
# Run model starting infection from chosen nodes until convergence is reached
# Author: Laura Quiroga
# --------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# Set default styles for graph
font = {'family': 'Times New Roman', 'size':24}
plt.rc('font', **font)
plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14

# Parameters
#N:= Number of devices in the network
N = 200
# density of the graph edges = # of edges/ max number of edges
density = 0.5
#beta:= Transmission rate (S->E)
beta = 0.5
#alpha:= Rate of infection upon exposure (E->I)
alpha = 0.1
#delta:= Rate of recovery (I->R)
delta = 0.08
#gamma:= Rate of re-suscptibility (R->S)
gamma = 0.5

colours = {'S':'cornflowerblue', 'E':'darkorange', 'I':'red', 'R':'green'}

# Adjancency matrix from given structure
def adj_matrix_from_structure(A, N):
  adj_matrix = np.zeros((N,N))
  for node in range(N):
    adj_matrix[node,:] = A[node]
  return adj_matrix

# Load adjmatrix from file
def load_adj(file_name):
    """
    Load model results from file
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
    
AdjInfo= load_adj('NetworksTC/200_05/AdjMatrix_N200_D05.txt')
# Using same network used for infection parameters tests
A = adj_matrix_from_structure(AdjInfo, N)

# Euler method:
# -------------------------------------------------------------------------

# Define the system of differential equations

# b(t) = beta* summation over j of: [(a_ij)*y_i(t)]       //using the first order approximation

def w_prime(t, w, y, z, i):
  """
  The rate of change of the probability of the node (i) being in the Exposed state:
  w'(t) = (1-w(t)-y(t)-z(t))*b(t) - alpha*w(t)
  """
  return (1-w[i]-y[i]-z[i])*beta*np.dot(A[i][:], y) - alpha*w[i]

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



# ----------------------- INITIAL VALUE CONDITIONS --------------------------

# Running simulation varying initially infected device: Vulnerability assessment of the network’s structure
total_infected = [0]*N
for node in [199]:
  # Initial values of x,w,y,z
  #x:= probability of being in the S state for every node
  #w:= probability of being in the E state for every node
  #y:= probability of being in the I state for every node
  #z:= probability of being in the R state for every node

  # Each is a matrix of N x # of time-steps
  x = np.ones((N, 1)) # all nodes start in susceptible state
  w = np.zeros((N, 1))
  y = np.zeros((N, 1))
  z = np.zeros((N, 1))

  # Total amount of devices per compartment
  totals = np.zeros((4,1))
  totals[0,0]=N-1 # Devices in S init conditions
  totals[2,0]=1 # Devices in I init conditions

  x[node,0] = 0
  y[node, 0] = 1  # the node that has the virus initially

  # Definition of time-steps to calculate the ODE
  dt = 1/1000
  t = [0]
  # -------------------------------------------------------------------------------
  # The arrays are filled in the for loop following the formula
  # Numeric solution to the ODE using Euler's method
  k=1
  convergence_count=0
  all_infected = False
  while(convergence_count<10 and k<=15000):
    # Add iteration
    t.append(t[k - 1] + dt)
    x = np.pad(x, [(0,0),(0,1)], mode='constant')
    w = np.pad(w, [(0,0),(0,1)], mode='constant')
    y = np.pad(y, [(0,0),(0,1)], mode='constant')
    z = np.pad(z, [(0,0),(0,1)], mode='constant')
    totals = np.pad(totals, [(0,0),(0,1)], mode='constant')

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
    #Convergence test
    diffs = np.linalg.norm(x[:,k] - x[:,k-1])
    diffi = np.linalg.norm(y[:,k] - y[:,k-1])
    if (diffs<0.0001 and diffi<0.0001):
      convergence_count+=1
    else:
      convergence_count=0

    if not all_infected and totals[2, k]==N:
      all_infected=True
      print(k) # First time step where all devices are infected

    k+=1


  print(len(totals[0])) # Time step where convergence is reached
  # Plot the evolution of the total values
  plt.plot(t, totals[0, :], label='Susceptible', color=colours['S'])
  plt.plot(t, totals[1, :], label='Exposed', color=colours['E'])
  plt.plot(t, totals[2, :], label='Infected', color=colours['I'])
  plt.plot(t, totals[3, :], label='Recovered', color=colours['R'])
  plt.ylabel('Number of devices', labelpad=20)
  plt.xlabel('Time step', labelpad=20)
  #plt.title(f"Evolution of total amount of devices per compartment (init {node})")
  leg = plt.legend()
  plt.show()
  plt.close()

  