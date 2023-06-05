# --------------------------------------------------------------------------
# Simulation of the NIMFA SEIRS model for a homogeneous network with constant parameters
# Author: Laura Quiroga
# --------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from .states import States
from .network import Network

class SEIRS_Model:
    # ------------------ Model definition and initialization -------------------
    def __init__(self, network: Network, rates:dict) -> None:
        # network:= Network object -> Information of devices and connections
        self.network = network
        self.n = self.network.n
        
        # rates := probabilities to change of state {alpha, beta, delta, gamma}
        self.rates = rates

        # resolution:= number of time-steps between one graph visualization and the other
        self.resolution = 50 # 50 => 0.5 time step

        # colour_key:= colours for each compartment's visualization 
        self.colour_key = {'S':'cornflowerblue', 'E':'darkorange', 'I':'red', 'R':'green'}

        # x := probability of being in the S state for every node
        # w := probability of being in the E state for every node
        # y := probability of being in the I state for every node
        # z := probability of being in the R state for every node
        self.x = np.zeros((self.n, 1))
        self.w = np.zeros((self.n, 1))
        self.y = np.zeros((self.n, 1))
        self.z = np.zeros((self.n, 1))

        # Probabilities initialization
        self.x[:,0] = self.network.init_states[States.S.value]
        self.w[:,0] = self.network.init_states[States.E.value]
        self.y[:,0] = self.network.init_states[States.I.value]
        self.z[:,0] = self.network.init_states[States.R.value]

        # totals := total number of nodes on each compartment per iteration
        self.totals = np.zeros((4,1))

        # nodes_comp := list of {iterations/resolution} dictionaries containing the compartment of each node at {resolution}-spaced iterations
        self.nodes_comp = []


    # ------------ Definition of the system of differential equations ------------

    # b(t) = beta* summation over j of: [(a_ij)*y_i(t)]       //using the first order approximation

    def w_prime(self, w, y, z, i):
        """
        The rate of change of the probability of the node (i) being in the Exposed state:
        w'(t) = (1-w(t)-y(t)-z(t))*b(t) - alpha*w(t)
        """
        return (1-w[i]-y[i]-z[i])*self.rates["beta"]*np.dot(self.network.adjMatrix[i,:], y) - self.rates["alpha"]*w[i]

    def y_prime(self, w, y, i):
        """
        The rate of change of the probability of the node (i) being in the Infected state:
        y'(t) =  alpha*w(t) - delta*y(t)
        """
        return self.rates["alpha"] * w[i] - self.rates["delta"] * y[i]

    def z_prime(self, y, z, i):
        """
        The rate of change of the probability of the node (i) being in the Recovered state:
        z'(t) = delta*y(t) - gamma*z(t)
        """
        return self.rates["delta"] * y[i] - self.rates["gamma"] * z[i]

    def run_model(self) -> None:
        """
        Executes the model simulation until convergence is reached
        """
        dt = 1/100
        self.t = [0]
        comp_dict = dict() # Dictionary with each node's compartments

        # Convergence condition: counter=10
        convergence_count = 0
        # Max number of iterations: k=1500 (15 time steps)
        k=1

        for i in range(self.n):
            # Add initial setup for visualization
            comp_dict[i] = self.define_compartment(i,0)
            # Set initial total devices per compartment
            self.totals[comp_dict[i],0]+=1
        self.nodes_comp.append(comp_dict)
        
        # The arrays are filled in the while loop following the formula
        # Numeric solution to the ODE using Euler's method
        while(convergence_count<10 or k==1500):
            visualization = False
            # Add iteration
            self.t.append(self.t[k - 1] + dt)
            self.x = np.pad(self.x, [(0,0),(0,1)], mode='constant')
            self.w = np.pad(self.w, [(0,0),(0,1)], mode='constant')
            self.y = np.pad(self.y, [(0,0),(0,1)], mode='constant')
            self.z = np.pad(self.z, [(0,0),(0,1)], mode='constant')
            self.totals = np.pad(self.totals, [(0,0),(0,1)], mode='constant')

            if k%self.resolution==0:
                visualization = True
                comp_dict = dict()
            
            self.t[k] = self.t[k - 1] + dt
            for i in range(self.n):
                # Calculation of probabilities
                self.w[i, k] = self.w[i, k - 1] + dt * self.w_prime( self.w[:, k - 1], self.y[:, k - 1],  self.z[:, k - 1], i)
                self.y[i, k] = self.y[i, k - 1] + dt * self.y_prime( self.w[:, k - 1], self.y[:, k - 1],  i)
                self.z[i, k] = self.z[i, k - 1] + dt * self.z_prime( self.y[:, k - 1], self.z[:, k - 1], i)
                self.x[i, k] = 1 - self.y[i, k] - self.z[i, k] - self.w[i, k]
                if (self.x[i, k]<0):
                    self.x[i, k]=0

                # Highest probability -> Current compartment
                compartment = self.define_compartment(i,k)
                # Add compartments for visualization
                if visualization:
                    comp_dict[i] = compartment
            if visualization:
                # Add compartments dictionary to list
                self.nodes_comp.append(comp_dict)

            # Convergence test
            diff_s = np.linalg.norm(self.x[:,k] - self.x[:,k-1])
            diff_i = np.linalg.norm(self.y[:,k] - self.y[:,k-1])
            if (diff_s<0.0001 and diff_i<0.0001):
                convergence_count+=1
            else:
                convergence_count=0

            # Advance iteration
            k+=1

    def run_model_fe_node(self):
        """
        Executes the model simulation for each (fe) node in the network
        for a fixed number of iterations
        """
        self.t_steps_fixed = 15
    
    # ----------------- Visualization of the model results ---------------------------

    def define_compartment(self, node, t_step):
        """
        Assign the node a current compartment according to the probabilities
        Highest probability -> Current compartment
        """
        probabilities = [self.x[node, t_step], self.w[node, t_step], self.y[node, t_step], self.z[node, t_step]]
        compartment = probabilities.index(max(probabilities))
        self.totals[compartment, t_step]+=1
        return compartment

    def plot_node_evolution(self, node:int):
        """
        Plot evolution of the given node's probabilities
        """
        fig = plt.figure(figsize=(8, 8))
        plt.plot(self.t, self.x[node, :], label='Susceptible', color=self.colour_key['S'])
        plt.plot(self.t, self.w[node, :], label='Exposed', color=self.colour_key['E'])
        plt.plot(self.t, self.y[node, :], label='Infected', color=self.colour_key['I'])
        plt.plot(self.t, self.z[node, :], label='Recovered', color=self.colour_key['R'])
        plt.ylabel('Probability of being in the compartment')
        plt.xlabel('Time')
        plt.title(f"Evolution of device {node}'s probabilities")
        plt.legend()
        plt.close()
        return fig
    
    def plot_network_evolution(self):
        """
        Plot evolution of the whole network
        """
        fig = plt.figure(figsize=(8, 8))
        plt.plot(self.t, self.totals[States.S.value, :], color=self.colour_key['S'], label='Susceptible')
        plt.plot(self.t, self.totals[States.E.value, :], color=self.colour_key['E'], label='Exposed')
        plt.plot(self.t, self.totals[States.I.value, :], color=self.colour_key['I'], label='Infected')
        plt.plot(self.t, self.totals[States.R.value, :], color=self.colour_key['R'], label='Recovered')
        plt.ylabel('Number of devices')
        plt.xlabel('Time')
        plt.title(f"Evolution of total amount of devices per compartment")
        plt.legend()
        plt.close()
        return fig
    
    def show_graph(self, step:int):
        """
        Plot the graph structure with node colours representing states
        """
        self.network.set_nodes_compartment(self.nodes_comp[step])
        g_colours = [0]*self.n

        for v,data in self.network.graph.nodes(data=True):
            g_colours[v] = self.colour_key[States(data["compartment"]).name]

        fig = plt.figure(figsize=(6, 6))
        nx.draw(self.network.graph, node_color=g_colours, with_labels=True)
        plt.axis("equal")
        s_patch = mpatches.Patch(color=self.colour_key['S'], label='Susceptible')
        e_patch = mpatches.Patch(color=self.colour_key['E'], label='Exposed')
        i_patch = mpatches.Patch(color=self.colour_key['I'], label='Infected')
        r_patch = mpatches.Patch(color=self.colour_key['R'], label='Recuperated')

        # Create a legend and add the custom legend items
        plt.legend(handles=[s_patch, e_patch, i_patch, r_patch], loc="best")
        plt.close()
        return fig
    
    def show_heatmap(self, total_i):
        """
        Plot the heatmap with the evolution of the total amount of infected devices
        by initially infected node
        """
        matrix = np.asarray(total_i, dtype=float)

        fig = plt.figure(figsize=(6, 6))

        # Create the reversed "hot" colormap
        reversed_hot_cmap = plt.cm.hot_r
        plt.imshow(matrix, cmap=reversed_hot_cmap, aspect='equal')
        
        cbar = plt.colorbar()
        cbar.set_label('Number of infected nodes')
        plt.gca().set_aspect(len(total_i[0])/len(total_i))

        # Draw horizontal lines on the grid
        num_lines = len(total_i)-1 # Number of lines to draw

        for i in range(0, num_lines + 1):
            y = i +0.5
            plt.axhline(y=y, color='black', linewidth=0.5)

        plt.xlabel('Time step')
        plt.ylabel('Initially infected device')

        # Set custom ticks for the x-axis
        x_ticks = [x*100 for x in range(self.t_steps_fixed+1)]  # Custom tick positions
        x_labels = [x for x in range(self.t_steps_fixed+1)] # Custom tick labels
        plt.xticks(x_ticks, x_labels)
        
        plt.title('Evolution of total infected nodes by initially infeted device')
        plt.close()
        return fig