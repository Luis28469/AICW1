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

def play(state, agent1, agent2):
    #simulates a session
    players = [agent1, agent2]

    current_player_id = 0
    print("Starting Game\n")
    while True:
        print(state)
        #for draws
        if all(cell==0 for row in state.grid for cell in row):
            print("Draw - All Cells Removed")
            return None
        
        #get current player name (checking if its an agent or human)
        current_player = players[current_player_id]
        if isinstance(current_player, Agent):
            player_name = current_player.name
        else:
            player_name=current_player

        print(f"\nIT IS {player_name}'s TURN\n")
        #num of regions prior to move

        move=None
        if isinstance(current_player, str):
            move = get_human_move(state)
        else:
            print(f"AI Is Thinking...\n")
            move = current_player.move(state, mode= "alphabeta")
        


        print(f"{player_name} makes a move: {move}") 
        

        #apply move
        r,c = move
        #use new method
        state.make_move(r,c,player_name) 
        #check if a player has won
        # if state.numRegions() > initial_regions:
        #     print("\nHINGER CREATED, GAME OVER")
        #     print(f"\n{player_name} Wins!")
        #     return player_name

        if state.get_winner() is not None:
            print("\nHINGER CREATED, GAME OVER")
            print(f"\n{player_name} Wins!")
            return player_name

        current_player_id = (current_player_id + 1) % 2
        



def tester():
    # start_grid = [
    #     [1, 1, 1, 0, 2],
    #     [1, 1, 0, 0, 0],
    #     [1, 1, 0, 1, 1],
    #     [1, 0, 0, 1, 1]
    # ]
    rows, columns = 4, 5
    #random grid
    start_grid = [[random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1 ], k=1)[0] for _ in range(columns)]
        for _ in range(rows)]
    
    game_state = State(start_grid)
    agent1 = Agent(size=(4, 5), name="AIAgent1")
    agent2 = Agent(size=(4, 5), name="AIAgent2")
    global Gamemode
    Gamemode = input("Select Game Mode: \n1. HUMAN VS HUMAN\n2. HUMAN VS AI\n3. AI VS AI\n")
    
    if Gamemode == "1":
        #MODE 1
        print("MODE 1: HUMAN VS HUMAN")
        name1 = input("Enter Player 1 Name: ")
        name2 = input("Enter Player 2 Name: ")
        winner = play(copy.deepcopy(game_state),name1, name2)
        return winner
    if Gamemode == "2":
        #MODE 2
        print("\nMODE 2: HUMAN VS AI")
        name1 = input("Enter Player 1 Name: ")
        winner = play(copy.deepcopy(game_state),name1, agent2)
        return winner
    if Gamemode == "3":
        #MODE 3
        print("\nMODE 3: AI VS AI")
        winner = play(copy.deepcopy(game_state),agent1, agent2)
        return winner


if __name__ == "__main__":
    tester()

