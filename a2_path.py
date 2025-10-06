from a1_state import State
import copy

def dfs_path(start, end):
    stack = [(copy.deepcopy(start), [])]
    visited = list()
    
    while stack:
        (state, path) = stack.pop()
        if state not in visited:
            
            if state == end:
                    print("Path to goal:", path)
                    return path
            
            visited.append(copy.deepcopy(state))

            grid = copy.deepcopy(start)

            for move in path: #apply the path to the grid so far
                grid[move[0]][move[1]] -= 1

            for move in State(grid).move():
                new_grid = copy.deepcopy(grid)
                new_grid[move[0]][move[1]] -= 1

                if State(new_grid).numHingers() == 0: #only add to stack if no hingers are created
                    stack.append((new_grid, path + [move]))
    
    return None

def dfs_tester():
    start_grid = [
            [1, 1, 1, 0, 2],
            [1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1]
        ]
    
    goal_grid = [
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1]
        ]
    
    path = dfs_path(start_grid, goal_grid)

if __name__ == "__main__":
    dfs_tester()