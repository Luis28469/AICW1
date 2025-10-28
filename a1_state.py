"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes a State class for Task 1

@author: B5 (100530015, 100531901, and 100418808)
@date:   30/10/2025

"""

import copy
from collections import deque

class State:
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.rows = len(grid)
        self.columns = len(grid[0]) if self.rows > 0 else 0
        self.startRegions = self.numRegions()
        self.last_move = None  # To who track the last move made

    def __str__(self):
        col_header = "    | " + " ".join(str(c) for c in range(self.columns))
        separator = " ---|" + "-" * (self.columns * 2)
        board_rows = []
        for r in range(self.rows):
            row_content = " ".join(str(self.grid[r][c]) for c in range(self.columns))
            board_rows.append(f"r{r}  | {row_content}")
        return f"      c o l u m n s\n{col_header}\n{separator}\n" + "\n".join(board_rows)

        #return "\n".join([" ".join(str(x) for x in row) for row in self.grid])

    #Generate possible moves (generator)
    def moves(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] > 0:
                    yield (r, c)
    
    #Determine if there is a winner and return the winner
    def get_winner(self):
        if self.numRegions() > self.startRegions:
            return self.last_move
        
        return None
    
    #Check if state is terminal
    def is_terminal(self):
        return self.get_winner() is not None or not list(self.moves())
    
    #Evaluate state for playing algorithms (1 for win, 0 for draw, -1 for loss)
    def evaluate(self, player):
        winner = self.get_winner()
        if winner == player:
            return 1
        elif winner is None:
            return 0
        return -1
    
    #Make a move on the board
    def make_move(self, r, c, player):
        self.startRegions = self.numRegions()
        if self.grid[r][c] > 0:
            self.grid[r][c] -= 1
            self.last_move = player
            return True
        return False

    #Get adjacent cells for a given cell (to help with region and hinger calculations)
    def get_adjacent_cells(self, r, c):
        positions = []
        #Loop through the 3x3 square centered at (r, c)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                #Skip the center cell itself
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                #Check if the new coordinates are within the board's bounds
                if 0 <= nr < self.rows and 0 <= nc < self.columns:
                    positions.append((nr, nc))
        return positions

    #Calculate number of regions in the current state and return it
    def numRegions(self):
        visited = set()
        regions = 0
        for r in range(self.rows):
            for c in range(self.columns):
                #for when a cell has a counter and is unvisited
                if self.grid[r][c] > 0 and (r, c) not in visited:
                    regions += 1
                    #BFS
                    queue = deque([(r, c)])
                    #mark as visited
                    visited.add((r, c))
                    
                    while queue:
                        #explore neighbours
                        current_r, current_c = queue.popleft()
                        #for when neighbour has counters but unvisited
                        for nr, nc in self.get_adjacent_cells(current_r, current_c):
                            if self.grid[nr][nc] > 0 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
        return regions

    #Calculate number of hingers in the current state and return it
    def numHingers(self):
        initial_regions = self.numRegions()
        hinger = 0
        #loop through every cell that could be a hinger
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] == 1:
                    temp_grid = copy.deepcopy(self.grid)
                    temp_grid[r][c] = 0
                    temp_state = State(temp_grid)
                    
                    if temp_state.numRegions() > initial_regions:
                        hinger += 1
        return hinger

    #Calculate the cost of a move based on adjacent active cells
    def get_move_cost(self,move):
        r,c = move
        if self.grid[r][c] == 0:
            return 0
        
        adjacent_active = sum(1 for nr, nc in self.get_adjacent_cells(r,c) if self.grid[nr][nc] > 0)

        return 1 + adjacent_active 
        
def tester():
    state_a_grid = [
        [1, 1, 1, 0, 2],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1]
    ]
    sa = State(state_a_grid)
    print("State A:")
    print(sa)
    print("\nPossible moves in State A:", list(sa.moves()))
    print("Number of regions in State A:", sa.numRegions())
    print("Number of hingers in State A:", sa.numHingers())
    
    state_b_grid = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1]
    ]
    sb = State(state_b_grid)
    print("\nState B:")
    print(sb)
    print("\nPossible moves in State B:", list(sb.moves()))
    print("Number of regions in State B:", sb.numRegions())
    print("Number of hingers in State B:", sb.numHingers())

if __name__ == "__main__":
    tester()