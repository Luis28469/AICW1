import copy

class State:
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.rows = len(grid)
        self.columns = len(grid[0]) if self.rows > 0 else 0
        
    def __str__(self):
        
        return "\n".join([" ".join(str(x) for x in row) for row in self.grid])

    def move(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] > 0:
                    yield (r, c)
                    
    def get_adjacent_cells(self, r, c):
        positions = []
        #Loop through the 3x3 square centered at (r, c)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:#Skip the center cell itself
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                #Check if the new coordinates are within the board's bounds
                if 0 <= nr < self.rows and 0 <= nc < self.columns:
                    positions.append((nr, nc))
        return positions

    def numRegions(self):
        visited = set()
        regions = 0
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c]>0 and (r,c) not in visited: #for when a cell has a counter and is unvisited
                    regions += 1
                    #BFS
                    queue=[(r,c)]
                    visited.add((r,c)) #mark as visited
                    
                    while queue:
                        current_r, current_c = queue.pop(0) #explore neighbours
                        for nr, nc in self.get_adjacent_cells(current_r, current_c):#for when neighbour has counters but unvisited
                            if self.grid[nr][nc] > 0 and (nr, nc) not in visited:
                                visited.add((nr,nc))
                                queue.append((nr,nc))
        return regions
        
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
                    
                    if temp_state.numRegions() != initial_regions:
                        hinger += 1
        return hinger
            
            
            
        
            
            
            
            
    
def tester():
    state_a_grid = [
        [1, 1, 0, 0, 2],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1]
    ]
    sa = State(state_a_grid)
    print("State A:")
    print(sa)
    print("\nPossible moves in State A:", list(sa.move()))
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
    print("\nPossible moves in State B:", list(sb.move()))
    print("Number of regions in State B:", sb.numRegions())
    print("Number of hingers in State B:", sb.numHingers()) 

        
        
        
        
                
if __name__ == "__main__":
    tester()
