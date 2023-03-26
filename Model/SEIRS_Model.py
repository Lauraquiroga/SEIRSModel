import numpy as np
import random
from .Network import Network

class SEIRS_Model:
    # Model definition and initialization
    def __init__(self, network: Network, rates) -> None:
        # network:= 
        self.network = network
        # iterations:=
        self.iterations = 0
        # n:= number of devices (nodes) in the network
        self.n = network.n
        # rates := probabilities to change of state
        self.parameters = rates

    # Function that executes the model simulation
    def run_model(self) -> None:
        t = 0
        while t< self.iterations:

            # for each node in the network
            for node in range(self.n):
                # S nodes (Susceptible)

                # E nodes (Exposed)

                # I nodes (Infected)

                # R nodes (Recovered)

                pass

            t+=1

    def calculate_beta(self):
        pass