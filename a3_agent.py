#DON FORGET THE HEADER WE HAVE TO USE
from a1_state import State
import copy

class Agent:
    def __init__(self, size, name="B5-Unit"):
        self.name = name
        self.size = size
        self.modes = ["minimax", "alphabeta"]

    def minimax(self, state, depth, is_maximizing):
        if state.is_terminal() or depth == 0:
            return state.evaluate(self.name)
        
        if is_maximizing: #If it's the AI's turn
            best_value = float('-inf')
            for (r, c) in state.moves():
                new_state = copy.deepcopy(state)
                new_state.make_move(r, c, self.name)
                value = self.minimax(new_state, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else: #If it's the opponent's turn
            best_value = float('inf')
            for (r, c) in state.moves():
                new_state = copy.deepcopy(state)
                new_state.make_move(r, c, "Opponent") #Generic name for opponent
                value = self.minimax(new_state, depth - 1, True)
                best_value = min(best_value, value)
            return best_value
        
    def alphabeta(self, state, depth, alpha, beta, is_maximazing):
        if state.is_terminal() or depth == 0:
            return state.evaluate(self.name)
        
        if is_maximazing:
            best_value = float('-inf')
            for (r, c) in state.moves():
                new_state = copy.deepcopy(state)
                new_state.make_move(r, c, self.name)
                value = self.alphabeta(new_state, depth - 1, alpha, beta, False)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:   #prune
                    break
            return best_value
        else:
            best_value = float('inf')
            for (r, c) in state.moves():
                new_state = copy.deepcopy(state)
                new_state.make_move(r, c, "Opponent") #Generic name for opponent
                value = self.alphabeta(new_state, depth - 1, alpha, beta, True)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:   #prune
                    break
            return best_value

    def move(self, state, mode="minimax"):
        if mode == "minimax":
            best_value = float('-inf')
            best_move = None
            for (r, c) in state.moves():
                new_state = copy.deepcopy(state)
                new_state.make_move(r, c, self.name)
                value = self.minimax(new_state, 3, False) #Sending False because next turn is opponent's
                if value > best_value:
                    best_value = value
                    best_move = (r, c)
            return best_move
        elif mode == "alphabeta":
            best_value = float('-inf')
            best_move = None
            alpha = float('-inf')
            beta = float('inf')
            for (r, c) in state.moves():
                new_state = copy.deepcopy(state)
                new_state.make_move(r, c, self.name)
                value = self.alphabeta(new_state, 5, alpha, beta, False) #Sending False because next turn is opponent's
                if value > best_value:
                    best_value = value
                    best_move = (r, c)
                alpha = max(alpha, best_value)
            return best_move
    
    def __str__(self):
        out = f"Agent Name: {self.name}\nGrid Size: {self.size[0]}x{self.size[1]}\nModes: {self.modes}"
        return out

def tester():
    initial_grid = [
            [1, 1, 1, 0, 2],
            [1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1]
        ]
    
    state = State(initial_grid)
    agent = Agent((4, 5), "TestAgent")
    print(agent)

    move = agent.move(state, mode="alphabeta")
    print(f"Chosen Move: {move}")

if __name__ == "__main__":
    tester()