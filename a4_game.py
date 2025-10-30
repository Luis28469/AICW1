"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes the core gameplay loop in Terminal

@author: B5 (100530015, 100531901, and 100418808)
@date:   30/10/2025

"""

from collections import deque
from a1_state import State
from a2_path import path_BFS, path_astar, path_IDDFS, path_DFS
from a3_agent import Agent
import random
import copy

def get_human_move(state):
    while True:
        try:
            move_str = input("Enter a move (row,col): ")
            if move_str == "exit":
                exit()
            r_string, c_string = move_str.split(",")
            r, c = int(r_string.strip()), int(c_string.strip())
            #validate move
            if not (0 <= r < state.rows and 0 <= c < state.columns):
                print("Invalid Move: Outside the board")
            elif state.grid[r][c] == 0:
                print("Invalid Move: Cell is empty")
            else:
                return (r, c) #Valid Move
        except (ValueError, IndexError):
            print("Invalid Move: Invalid format")

def play(state, agent1, agent2, mode):
    #simulates a session
    players = [agent1, agent2]
    current_player_id = 0
    print("Starting Game\n")
    while True:
        print(state)
        #for draws
        if all(cell==0 for row in state.grid for cell in row):
            print("Draw - All Cells Removed\n")
            return None
        
        #get current player name (checking if its an agent or human)
        current_player = players[current_player_id]
        if isinstance(current_player, Agent):
            player_name = current_player.name
        else:
            player_name=current_player

        print(f"\nIT IS {player_name}'s TURN\n")

        move=None
        if isinstance(current_player, str):
            move = get_human_move(state)
        else:
            print(f"AI Is Thinking...\n")       
            move = current_player.move(state, mode) #change between alphabeta and montecarlo        


        print(f"{player_name} makes a move: {move}") 
        

        #apply move
        r,c = move
        #use new method
        state.make_move(r,c,player_name) 

        if state.get_winner() is not None:
            print("\nHINGER CREATED, GAME OVER")
            print(f"\n{player_name} Wins!")
            print("Here is the final board state: \n")
            print(state)
            print("\n")
            return player_name

        current_player_id = (current_player_id + 1) % 2
        

#uses BFS to search all possible moves on the board move by move to check if the board wont have any hingers in the next n moves
def is_safe_for_n_moves(initial_state, max_depth):
    queue = deque([(initial_state, 0)])
    visited = {tuple(map(tuple, initial_state.grid))}

    while queue:
        current_state, depth = queue.popleft()

        if current_state.numHingers() > 0:
            return False
        
        if depth < max_depth:
            for move in current_state.moves():
                new_grid = copy.deepcopy(current_state.grid)
                new_grid[move[0]][move[1]] -= 1
                next_state = State(new_grid)
                new_grid_tuple = tuple(map(tuple, next_state.grid))

                if new_grid_tuple not in visited:
                    visited.add(new_grid_tuple)
                    queue.append((State(new_grid), depth + 1))

    return True


#code for hard mode, changes the weighting of each cell in the grid to have a higher chance of having a number >1
def hard_mode(rows,columns):
    #up to 4 now, might change rates for balancing
    while True:
        grid = [[random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.3, 0.18, 0.02], k=1)[0] for _ in range(columns)]for _ in range(rows)]

        initial_state = State(grid)
        
        if is_safe_for_n_moves(initial_state, 3): #change the integer to change the number of moves checked to not have a hinger state
            print("------------------")
            print("Safe Grid Found! Starting Game")
            print("------------------\n")
            return grid

def play_again():
    while True:
        play_again = input("Play Again? (Y/N): ")
        if play_again.lower() == "y":
            tester()
        elif play_again.lower() == "n":
            return False



def tester():
    rows, columns = 4, 5
    start_grid = None

    #select difficulty
    while True:
        difficulty = input("\nSelect Difficulty:\nEASY:1\nMEDIUM:2\nHARD:3\nEnter Difficulty: ")
        if difficulty == "1":
            start_grid = [[random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.25, 0.05 ], k=1)[0] for _ in range(columns)]for _ in range(rows)]
            break
        if difficulty == "2":
            start_grid = [[random.choices([0, 1, 2, 3], weights=[0.3, 0.3, 0.3, 0.1 ], k=1)[0] for _ in range(columns)]for _ in range(rows)]
            break
        if difficulty == "3":
            print("Generating Hard Mode Grid...\n")
            start_grid = hard_mode(rows,columns)
            break
        if difficulty == "exit":
            exit()
        else:
            print("Invalid Input")
    
    game_state = State(start_grid)
    agent1 = Agent(size=(4, 5), name="AIAgent1")
    agent2 = Agent(size=(4, 5), name="AIAgent2")
    global Gamemode
    Gamemode = input("Select Game Mode: \n1. HUMAN VS HUMAN\n2. HUMAN VS AI\n3. AI VS AI\nEnter Game Mode: ")
    
    if Gamemode == "1":
        #MODE 1
        print("MODE 1: HUMAN VS HUMAN")
        name1 = input("Enter Player 1 Name: ")
        name2 = input("Enter Player 2 Name: ")
        winner = play(copy.deepcopy(game_state),name1, name2)
        play_again()
        return winner
    elif Gamemode == "2":
        #MODE 2
        print("\nMODE 2: HUMAN VS AI")
        name1 = input("Enter Player 1 Name: ")
        mode = input("Select AI Mode:\n1. MINIMAX\n2. ALPHABETA\n3. MONTECARLO\nEnter Mode: ")
        if mode == "1":
            mode = "minimax"
        elif mode == "2":
            mode = "alphabeta"
        elif mode == "3":
            mode = "montecarlo"
        winner = play(copy.deepcopy(game_state),name1, agent2, mode)
        play_again()
        return winner
    elif Gamemode == "3":
        #MODE 3
        print("\nMODE 3: AI VS AI")
        mode = input("Select AI Mode:\n1. MINIMAX\n2. ALPHABETA\n3. MONTECARLO\nEnter Mode: ")
        if mode == "1":
            mode = "minimax"
        elif mode == "2":
            mode = "alphabeta"
        elif mode == "3":
            mode = "montecarlo"
        winner = play(copy.deepcopy(game_state),agent1, agent2, mode)
        play_again()
        return winner
            
    else:
        print("Invalid Input")


if __name__ == "__main__":
    tester()
