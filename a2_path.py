from a1_state import State
import copy

def dfs_path(start, end):
    stack = [(copy.deepcopy(start), [])]
    visited = list() #switched back to list because it wasnt working
    
    while stack:
        (state, path) = stack.pop()
        if state not in visited:
            
            if state == end:
                print("Path to goal:", path)
                return path

            # grid = copy.deepcopy(start)

            # for move in path: #apply the path to the grid so far
            #     grid[move[0]][move[1]] -= 1
            #btw this remakes the grid each time, we dont need this i think

            for move in State(state).moves():
                new_grid = copy.deepcopy(state)
                new_grid[move[0]][move[1]] -= 1

                new_grid_tuple = tuple(map(tuple, new_grid))

                if new_grid_tuple not in visited:
                    if State(new_grid).numHingers() == 0: #only add to stack if no hingers are created
                        visited.append(new_grid_tuple)
                        stack.append((new_grid, path + [move]))
    
    return None

def path_astar(start, end):
    open_list = list()
    closed_list = list()
    open_list.append((start, 0, []))

    while not open_list:
        #



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