from enum import Enum

class States(Enum):
    S = 0 # Susceptible
    E = 1 # Exposed
    I = 2 # Infected
    R = 3 # Recovered