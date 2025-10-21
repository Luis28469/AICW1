#DON FORGET THE HEADER WE HAVE TO USE
from a1_state import State
import copy
import random
import math

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.moves = list(state.moves())  # Remaining moves to explore

    def is_fully_expanded(self):
        return len(self.moves) == 0
    
    def best_child(self, c=1.4):
        choices_weights = [
            (child.wins / child.visits) + c * math.sqrt((math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

class Agent:
    def __init__(self, size, name="B5-Unit"):
        self.name = name
        self.size = size
        self.modes = ["minimax", "alphabeta", "montecarlo"]

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
        
    def rollout(self, state):

        current_state = copy.deepcopy(state)
        
        player = "Opponent"  # Start with opponent's turn
        
        while not current_state.is_terminal():
            move = random.choice(list(current_state.moves()))
            current_state.make_move(move[0], move[1], player)
            player = self.name if player == "Opponent" else "Opponent"
        
        return current_state.evaluate(self.name)

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
        elif mode == "montecarlo":
            root = Node(state)
            for t in range(3000): # Number of simulations
                node = root

                # Selection
                while node.is_fully_expanded() and not node.state.is_terminal():
                    node = node.best_child()
                
                # Expansion
                if node.moves and not node.state.is_terminal():
                    state_copy = copy.deepcopy(state)
                    move = node.moves.pop()
                    state_copy.make_move(move[0], move[1], self.name)
                    child_node = Node(state_copy, parent=node, move=move)
                    node.children.append(child_node)
                    node = child_node
                
                # Simulation
                result = self.rollout(node.state)
                
                # Backpropagation
                while node is not None:
                    node.visits += 1
                    node.wins += result
                    node = node.parent
            # Choose the move with the most visits
            return root.best_child(c=0).move
    
    def __str__(self):
        out = f"Agent Name: {self.name}\nGrid Size: {self.size[0]}x{self.size[1]}\nModes: {self.modes}"
        return out

def tester():
    initial_grid = [
            [1, 1, 1, 0, 2],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1]
        ]
    
    print("Agent Created:\n")
    state = State(initial_grid)
    agent = Agent((4, 5), "TestAgent")
    print(agent)

    print("\n\nInitial Board State:\n")
    print(state)

    print("\nTesting Minimax Move Selection:")
    move = agent.move(state, mode="alphabeta")
    print(f"Chosen Move: {move}")

    print("\nTesting Alpha-Beta Move Selection:")
    move = agent.move(state, mode="alphabeta")
    print(f"Chosen Move: {move}")

    print("\nTesting Monte Carlo Move Selection:")
    move = agent.move(state, mode="montecarlo")
    print(f"Chosen Move: {move}")

if __name__ == "__main__":
    tester()