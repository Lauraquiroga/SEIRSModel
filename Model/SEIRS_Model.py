import numpy as np
import random
from .network import Network

class SEIRS_Model:
    # ------------------ Model definition and initialization -------------------
    def __init__(self, network: Network, iterations: int, **rates) -> None:
        # network:= 
        self.network = network

        # rates := probabilities to change of state
        self.parameters = rates

        # n_times:= number of time-steps considered
        self.n_times = iterations

        # x := probability of being in the S state for every node
        # w := probability of being in the E state for every node
        # y := probability of being in the I state for every node
        # z := probability of being in the R state for every node
        self.x = np.ones((self.n, iterations)) # all nodes start in susceptible state
        self.w = np.zeros((self.n, iterations))
        self.y = np.zeros((self.n, iterations))
        self.z = np.zeros((self.n, iterations))
        # !!!!!!!!!!!!!por ahora lo voy a inicializar en un nodo cualquiera
        self.x[3,0] = 0
        self.y[3, 0] = 1  # 4th node has the virus initially

    # ------------ Definition of the system of differential equations ------------

    # b(t) = beta* summation over j of: [(a_ij)*y_i(t)]       //using the first order approximation

    def w_prime(self, w, y, z, i):
        """
        The rate of change of the probability of the node (i) being in the Exposed state:
        w'(t) = (1-w(t)-y(t)-z(t))*b(t) - alpha*w(t)
        """
        return (1-w[i]-y[i]-z[i])*np.dot(self.network.adjMatrix[i,:], y) - self.rates["alpha"]*w[i]

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
        Executes the model simulation
        """
        min_t = 0
        max_t = self.n_times/100
        t = np.linspace(min_t, max_t, self.n_times)
        dt = t[1] - t[0]
        
        # The arrays are filled in the for loop following the formula
        # Numeric solution to the ODE using Euler's method
        for k in range(1, self.n_times):
            t[k] = t[k - 1] + dt
            for i in range(self.network.n):
                self.w[i, k] = self.w[i, k - 1] + dt * self.w_prime( self.w[:, k - 1], self.y[:, k - 1],  self.z[:, k - 1], i)
                self.y[i, k] = self.y[i, k - 1] + dt * self.y_prime( self.w[:, k - 1], self.y[:, k - 1],  i)
                self.z[i, k] = self.z[i, k - 1] + dt * self.z_prime( self.y[:, k - 1], self.z[:, k - 1], i)
                self.x[i, k] = 1 - self.y[i, k] - self.z[i, k] - self.w[i, k]
                if (self.x[i, k]<0):
                    self.x[i, k]=0

        