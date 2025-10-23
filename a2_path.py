"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes all the fucntions to retrieve safe paths needed in Task 2

@author: B5 (100530015, 100531901, and 100418808)
@date:   30/10/2025

"""

from a1_state import State
import copy
import time
import tracemalloc
import heapq
from collections import deque

def path_BFS(start, end):

    start_state = State(start)
    end_state = State(end)
    #Validation to confirm there is not already a hinger in the states
    if start_state.numHingers() > 0 or end_state.numHingers() > 0:
        return None
    
    start_grid_tuple = tuple(map(tuple, start_state.grid))
    end_grid_tuple = tuple(map(tuple, end_state.grid))
    
    #Data structures
    queue = deque([(start_state, [])])
    visited = {start_grid_tuple}
    
    while queue:
        current_state, path = queue.popleft()

        current_grid_tuple = tuple(map(tuple, current_state.grid))

        if current_grid_tuple == end_grid_tuple:
            return path

        for r, c in current_state.moves():
            temp_grid = copy.deepcopy(current_state.grid)
            temp_grid[r][c] = 0
            next_state = State(temp_grid)
            
            next_grid_tuple = tuple(map(tuple, next_state.grid))
            
            # Aplying the restrictions of a safe path
            # The next state should not be a hinger and should not be already visited
            if next_state.numHingers() == 0 and next_grid_tuple not in visited:
                visited.add(next_grid_tuple)
                new_path = path + [(r, c)]
                queue.append((next_state, new_path))

    return None


def path_DFS(start, end):
    stack = [(copy.deepcopy(start), [])]
    visited = set()
    visited.add(tuple(map(tuple, start))) #convert to tuple as it is hashable now
    
    while stack:
        (state, path) = stack.pop()
            
            
        if state == end:
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

def path_dls(start, end, limit):
    stack = [(copy.deepcopy(start), [], 0)]  # (state, path, depth)
    visited = set()

    while stack:
        state, path, depth = stack.pop()
        state_tuple = tuple(map(tuple, state))

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if state == end:
            return path

        if depth < limit:  # Only proceed if we haven't reached the depth limit
            for move in State(state).moves():
                new_grid = copy.deepcopy(state)
                new_grid[move[0]][move[1]] -= 1
                new_grid_tuple = tuple(map(tuple, new_grid))

                if new_grid_tuple not in visited:
                    if State(new_grid).numHingers() == 0:
                        stack.append((new_grid, path + [move], depth + 1))
    
    return None


def path_IDDFS(start, end):
    max_depth = sum(map(sum, start)) - sum(map(sum, end)) #maximum depth is the total of moves performed
    for depth in range(max_depth + 1): #try depth from 0 to max_depth
        path = path_dls(start, end, depth)
        if path is not None:
            return path
    return None


#This heuristic is admissible as it uses the Hamming distance, where it counts the number of tiles on the board that are different between the two states so it doesnt overestimate.  For each tile it will have to move at least once.
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

def compare():
    start_grid = [
            [1, 1, 1, 0, 2],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 1, 1]
        ]
    
    goal_grid = [
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1]
        ]
    
    algorithms = [("BFS", path_BFS), ("DFS", path_DFS), ("IDDFS", path_IDDFS), ("A*", path_astar)]

    for name, algorithm in algorithms:
        time_start = time.time()
        tracemalloc.start()
        path = algorithm(start_grid, goal_grid)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_end = time.time()
        if path:
            print(f"{name} found a path.\nMoves: {len(path)}.\nTime: {time_end - time_start:.6f} seconds.\nMemory Peak: {peak / 10**6}MB\nPath: {path}\n\n")
        else:
            print(f"{name} couldn't find a safe path.\nTime used: {time_end - time_start:.6f} seconds.\nMemory Peak: {peak / 10**6}MB\n\n")
    

#this min safe function uses Dijikstra's Algorithm and a Priority queue to explore paths that have lower cost even if it have more moves.
def min_safe(start, end):
    start_state = State(start)
    end_state = State(end)
    #the priority queue will store the total cost, path and current state
    open_list = [(0, [], start_state)]
    heapq.heapify(open_list)
    #this stores minimjum cost found so far and updates the algorithm if a cheaper path is found
    visited={tuple(map(tuple, start_state.grid)):0}

    while open_list:
        #get path with lowest total cost from priority queue
        total_cost, path, current_state = heapq.heappop(open_list)
        #for if the goal is reached, meaning this is the cheapest path
        if current_state.grid == end_state.grid:
            return path
        for move in current_state.moves():
            next_grid = copy.deepcopy(current_state.grid)
            #calculates the cost for the move based on the current board state
            move_cost = current_state.get_move_cost(move)
            next_grid[move[0]][move[1]] -= 1
            next_state = State(next_grid)
            #check for hingers to make sure it remains safe
            if next_state.numHingers() == 0:
                new_total_cost = total_cost + move_cost
                next_grid_tuple = tuple(map(tuple, next_state.grid))

                #for if we havent seen this state or found cheaper path
                if next_grid_tuple not in visited or new_total_cost < visited[next_grid_tuple]:
                    visited[next_grid_tuple] = new_total_cost
                    new_path = path + [move]
                    heapq.heappush(open_list, (new_total_cost, new_path, next_state))

    return None

def calculate_path_cost(start_grid, path):
    total_cost = 0
    #create object that will be updated as we move
    current_state = State(start_grid)
    for move in path:
        move_cost = current_state.get_move_cost(move)
        total_cost += move_cost
        #update the grid with the move to create the updated grid for the next move
        new_grid = copy.deepcopy(current_state.grid)
        new_grid[move[0]][move[1]] -= 1
        current_state = State(new_grid)

    return total_cost


def tester():
    start_grid = [
            [1, 1, 1, 0, 2],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 1, 1]
        ]
    
    goal_grid = [
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1]
        ]
    

    bfs_path = path_BFS(start_grid, goal_grid)
    dfs_path = path_DFS(start_grid, goal_grid)
    iddfs_path = path_IDDFS(start_grid, goal_grid)
    a_path = path_astar(start_grid, goal_grid)

    list_of_paths = {
        "BFS" : bfs_path, 
        "DFS" : dfs_path, 
        "IDDFS" : iddfs_path, 
        "A-Star" : a_path
        }
    
    for name, path in list_of_paths.items():
        if path:
            print(f"{name} found a path with {len(path)} moves: {path}")
        else:
            print(f"{name} couldn't find a safe path.")

    minsafe = min_safe(start_grid, goal_grid)
    if minsafe:
        total_cost = calculate_path_cost(start_grid, minsafe)
        print (f"Minsafe found the cheapest path: {minsafe}")
        print (f"Total cost: {total_cost}")
    else:
        print("Minsafe couldn't find a safe path.")



if __name__ == "__main__":
    compare()
    tester()
