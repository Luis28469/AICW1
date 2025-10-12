#DON FORGET THE HEADER WE HAVE TO USE
from a1_state import State

class Agent:
    def __init__(self, size, name="B5-Unit"):
        self.name = name
        self.size = size
        self.modes = ["minimax", "alphabeta"]

    def move(self, state, mode):
        # Placeholder for agent's move logic
        pass
    
    def __str__(self):
        print(f"Agent Name: {self.name}\nGrid Size: {self.size[0]}x{self.size[1]}\nModes: {self.modes}")