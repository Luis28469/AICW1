from a1_state import State
import copy
import heapq
def dfs_path(start, end):
    stack = [(copy.deepcopy(start), [])]
    visited = set()
    visited.add(tuple(map(tuple, start))) #convert to tuple as it is hashable now
    
    while stack:
        (state, path) = stack.pop()
            
            
        if state == end:
            print(f"DFS found a path with {len(path)} moves: {path}")
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
                    visited.add(new_grid_tuple)
                    stack.append((new_grid, path + [move]))
        
    return None
def heuristic(current_grid, end_grid):
    diff = 0
    rows = len(current_grid)
    cols = len(current_grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if current_grid[r][c] != end_grid[r][c]:
                diff += 1
    return diff

def path_astar(start, end):
    start_state = State(start)
    end_state = State(end)

    open_list = [(0, 0, [], start_state)]
    heapq.heapify(open_list)
    closed_list = set()

    while open_list:
        f_cost, g_cost, path, current_state = heapq.heappop(open_list)
        current_grid_tuple = tuple(map(tuple, current_state.grid))

        if current_grid_tuple in closed_list:
            continue

        if current_state.grid == end_state.grid:
            return path
            
        closed_list.add(current_grid_tuple)

        #Explore neighbors (next possible moves)
        for move in current_state.moves():
            next_grid = copy.deepcopy(current_state.grid)
            next_grid[move[0]][move[1]] -= 1
            next_state = State(next_grid)
            next_grid_tuple = tuple(map(tuple, next_state.grid))

            #Skip this path if we've already explored this state
            if next_grid_tuple in closed_list:
                continue

            #Check the safe path condition
            if next_state.numHingers() == 0:
                #Calculate costs for the new node
                new_g_cost = g_cost + 1 #Cost of each move is 1
                h_cost = heuristic(next_state.grid, end_state.grid)
                new_f_cost = new_g_cost + h_cost
                #Add the new node to the open list and the visited list
                new_path = path + [move]
                heapq.heappush(open_list, (new_f_cost, new_g_cost, new_path, next_state))

    return None



def dfs_tester():
    start_grid = [
            [1, 1, 1, 0, 2],
            [1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1]
        ]
    
    goal_grid = [
            [1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0]
        ]
    
    path = dfs_path(start_grid, goal_grid)
    a_path = path_astar(start_grid, goal_grid)
    
    if a_path:
        print(f"A* found a path with {len(a_path)} moves: {a_path}")
    else:
        print("A* couldn't find a safe path.")

if __name__ == "__main__":
    dfs_tester()