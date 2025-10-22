from collections import deque
from a1_state import State
from a2_path import path_BFS, path_astar, path_IDDFS, path_DFS
from a3_agent import Agent
import random
import copy
import pygame
import time
import sys
import threading


#PYGAME SETUP
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000,700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hinger Game")
font_small = pygame.font.Font("freesansbold.ttf", 20)
font_medium = pygame.font.Font("freesansbold.ttf", 50)
font_large = pygame.font.Font("freesansbold.ttf", 70)
clock = pygame.time.Clock()


try:
    pop_sound = pygame.mixer.Sound("Pop.mp3")
except pygame.error:
    print("Pop.mp3 not found")
    pop_sound = None

try:
    win_sound = pygame.mixer.Sound("gamewin.mp3")
except pygame.error:
    print("Win.mp3 not found")
    win_sound = None

#colours
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
BLUE, RED, GREEN = (100, 149, 237), (255, 99, 71), (50, 205, 50)
CELL_SIZE, MARGIN = 80, 10
GRID_X_OFFSET, GRID_Y_OFFSET = 100, 150


#NEW PYGAME FUNCTIONS

#draws text on screen
def draw_text(text, font, color, surface, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_board(state):
    draw_text("C O L U M N S", font_medium, BLACK, GRID_X_OFFSET + (state.columns * (CELL_SIZE + MARGIN)) / 2, GRID_Y_OFFSET - 60)
    for r in range(state.rows):
        row_label = ["R", "O", "W", "S"]
        label = row_label[r] if r<len(row_label) else str(" ")
        draw_text(f"{label} {r}", font_medium, BLACK, GRID_X_OFFSET - 60, GRID_Y_OFFSET + r * (CELL_SIZE + MARGIN) + CELL_SIZE / 2)
        for c in range(state.columns):
            if r == 0:
                draw_text(str(c), font_small, BLACK, GRID_X_OFFSET + c * (CELL_SIZE + MARGIN) + CELL_SIZE / 2, GRID_Y_OFFSET - 25)
            rect = pygame.Rect(GRID_X_OFFSET + c * (CELL_SIZE + MARGIN), GRID_Y_OFFSET + r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            val = state.grid[r][c]
            if val > 0:
                draw_text(str(val), font_medium, BLACK, rect.centerx, rect.centery)

#converts mouse coordinates to row and column
def get_clicked(pos, state):
    for r in range(state.rows):
        for c in range(state.columns):
            rect = pygame.Rect(GRID_X_OFFSET + c * (CELL_SIZE + MARGIN), GRID_Y_OFFSET + r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
            if rect.collidepoint(pos):
                return r, c
            
    return None


def show_menu(title, options):
    buttons = []
    for i, option_text in enumerate(options):
        rect = pygame.Rect(SCREEN_WIDTH / 2 - 150, 200 + i * 60, 300, 60)
        buttons.append((rect, option_text))
    #quit function and button click detection in menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #returns index of anyu button clicked
                for i, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        return i + 1

        screen.fill(WHITE)
        draw_text(title, font_large, BLACK, SCREEN_WIDTH / 2, 100)
        for rect, option_text in buttons:
            pygame.draw.rect(screen, BLUE, rect)
            draw_text(option_text, font_medium, WHITE, rect.centerx, rect.centery)

        pygame.display.flip()
        clock.tick(30)


def get_text_input(input_text):
    input_box = pygame.Rect(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 25, 400, 50)
    user_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(WHITE)
        draw_text(input_text, font_medium, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
        pygame.draw.rect(screen, GRAY, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        draw_text(user_text, font_medium, BLACK, input_box.centerx, input_box.centery)    

        pygame.display.flip()
        clock.tick(30)




    

#GAME FUNCTIONS ----------------------------

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

def play(state, agent1, agent2, mode="alphabeta"):
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
        #num of regions prior to move

        move=None
        if isinstance(current_player, str):
            move = get_human_move(state)
        else:
            print(f"AI Is Thinking...\n")
            #move = current_player.move(state, mode= "montecarlo") #change between alphabeta and montecarlo        
            move = current_player.move(state, mode) #change between alphabeta and montecarlo        


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
    # start_grid = [
    #     [1, 1, 1, 0, 2],
    #     [1, 1, 0, 0, 0],
    #     [1, 1, 0, 1, 1],
    #     [1, 0, 0, 1, 1]
    # ]
    rows, columns = 4, 5
    #random grid
    # start_grid = [[random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1 ], k=1)[0] for _ in range(columns)]for _ in range(rows)]
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
        print("\nMODE 1: HUMAN VS HUMAN")
        name1 = input("Enter Player 1 Name: ")
        name2 = input("Enter Player 2 Name: ")
        winner = play(copy.deepcopy(game_state),name1, name2)
        play_again()
        return winner
    elif Gamemode == "2":
        #MODE 2
        print("\nMODE 2: HUMAN VS AI")
        name1 = input("\nEnter Player 1 Name: ")
        mode = input("Select AI Mode (1, 2 or 3):\n1. MINIMAX (Not Recommended)\n2. ALPHABETA\n3. MONTECARLO\nEnter Mode: ")
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
        mode = input("Select AI Mode (1, 2, or 3):\n1. MINIMAX (Not Recommended)\n2. ALPHABETA\n3. MONTECARLO\nEnter Mode: ")
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











































#CODE WITHOUT PYGAME 22/10/2025
# def get_human_move(state):
#     while True:
#         try:
#             move_str = input("Enter a move (row,col): ")
#             if move_str == "exit":
#                 exit()
#             r_string, c_string = move_str.split(",")
#             r, c = int(r_string.strip()), int(c_string.strip())
#             #validate move
#             if not (0 <= r < state.rows and 0 <= c < state.columns):
#                 print("Invalid Move: Outside the board")
#             elif state.grid[r][c] == 0:
#                 print("Invalid Move: Cell is empty")
#             else:
#                 return (r, c) #Valid Move
#         except (ValueError, IndexError):
#             print("Invalid Move: Invalid format")

# def play(state, agent1, agent2, mode="alphabeta"):
#     #simulates a session
#     players = [agent1, agent2]
#     current_player_id = 0
#     print("Starting Game\n")
#     while True:
#         print(state)
#         #for draws
#         if all(cell==0 for row in state.grid for cell in row):
#             print("Draw - All Cells Removed\n")
#             return None
        
#         #get current player name (checking if its an agent or human)
#         current_player = players[current_player_id]
#         if isinstance(current_player, Agent):
#             player_name = current_player.name
#         else:
#             player_name=current_player

#         print(f"\nIT IS {player_name}'s TURN\n")
#         #num of regions prior to move

#         move=None
#         if isinstance(current_player, str):
#             move = get_human_move(state)
#         else:
#             print(f"AI Is Thinking...\n")
#             #move = current_player.move(state, mode= "montecarlo") #change between alphabeta and montecarlo        
#             move = current_player.move(state, mode) #change between alphabeta and montecarlo        


#         print(f"{player_name} makes a move: {move}") 
        

#         #apply move
#         r,c = move
#         #use new method
#         state.make_move(r,c,player_name) 
#         #check if a player has won
#         # if state.numRegions() > initial_regions:
#         #     print("\nHINGER CREATED, GAME OVER")
#         #     print(f"\n{player_name} Wins!")
#         #     return player_name

#         if state.get_winner() is not None:
#             print("\nHINGER CREATED, GAME OVER")
#             print(f"\n{player_name} Wins!")
#             print("Here is the final board state: \n")
#             print(state)
#             print("\n")
#             return player_name

#         current_player_id = (current_player_id + 1) % 2
        

# #uses BFS to search all possible moves on the board move by move to check if the board wont have any hingers in the next n moves
# def is_safe_for_n_moves(initial_state, max_depth):
#     queue = deque([(initial_state, 0)])
#     visited = {tuple(map(tuple, initial_state.grid))}

#     while queue:
#         current_state, depth = queue.popleft()

#         if current_state.numHingers() > 0:
#             return False
        
#         if depth < max_depth:
#             for move in current_state.moves():
#                 new_grid = copy.deepcopy(current_state.grid)
#                 new_grid[move[0]][move[1]] -= 1
#                 next_state = State(new_grid)
#                 new_grid_tuple = tuple(map(tuple, next_state.grid))

#                 if new_grid_tuple not in visited:
#                     visited.add(new_grid_tuple)
#                     queue.append((State(new_grid), depth + 1))

#     return True


# #code for hard mode, changes the weighting of each cell in the grid to have a higher chance of having a number >1
# def hard_mode(rows,columns):
#     #up to 4 now, might change rates for balancing
#     while True:
#         grid = [[random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.3, 0.18, 0.02], k=1)[0] for _ in range(columns)]for _ in range(rows)]

#         initial_state = State(grid)
        
#         if is_safe_for_n_moves(initial_state, 3): #change the integer to change the number of moves checked to not have a hinger state
#             print("------------------")
#             print("Safe Grid Found! Starting Game")
#             print("------------------\n")
#             return grid

# def play_again():
#     while True:
#         play_again = input("Play Again? (Y/N): ")
#         if play_again.lower() == "y":
#             tester()
#         elif play_again.lower() == "n":
#             return False



# def tester():
#     # start_grid = [
#     #     [1, 1, 1, 0, 2],
#     #     [1, 1, 0, 0, 0],
#     #     [1, 1, 0, 1, 1],
#     #     [1, 0, 0, 1, 1]
#     # ]
#     rows, columns = 4, 5
#     #random grid
#     # start_grid = [[random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1 ], k=1)[0] for _ in range(columns)]for _ in range(rows)]
#     start_grid = None

#     #select difficulty
#     while True:
#         difficulty = input("\nSelect Difficulty:\nEASY:1\nMEDIUM:2\nHARD:3\nEnter Difficulty: ")
#         if difficulty == "1":
#             start_grid = [[random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.25, 0.05 ], k=1)[0] for _ in range(columns)]for _ in range(rows)]
#             break
#         if difficulty == "2":
#             start_grid = [[random.choices([0, 1, 2, 3], weights=[0.3, 0.3, 0.3, 0.1 ], k=1)[0] for _ in range(columns)]for _ in range(rows)]
#             break
#         if difficulty == "3":
#             print("Generating Hard Mode Grid...\n")
#             start_grid = hard_mode(rows,columns)
#             break
#         if difficulty == "exit":
#             exit()
#         else:
#             print("Invalid Input")
    
#     game_state = State(start_grid)
#     agent1 = Agent(size=(4, 5), name="AIAgent1")
#     agent2 = Agent(size=(4, 5), name="AIAgent2")
#     global Gamemode
#     Gamemode = input("Select Game Mode: \n1. HUMAN VS HUMAN\n2. HUMAN VS AI\n3. AI VS AI\nEnter Game Mode: ")
    
#     if Gamemode == "1":
#         #MODE 1
#         print("\nMODE 1: HUMAN VS HUMAN")
#         name1 = input("Enter Player 1 Name: ")
#         name2 = input("Enter Player 2 Name: ")
#         winner = play(copy.deepcopy(game_state),name1, name2)
#         play_again()
#         return winner
#     elif Gamemode == "2":
#         #MODE 2
#         print("\nMODE 2: HUMAN VS AI")
#         name1 = input("\nEnter Player 1 Name: ")
#         mode = input("Select AI Mode (1, 2 or 3):\n1. MINIMAX (Not Recommended)\n2. ALPHABETA\n3. MONTECARLO\nEnter Mode: ")
#         if mode == "1":
#             mode = "minimax"
#         elif mode == "2":
#             mode = "alphabeta"
#         elif mode == "3":
#             mode = "montecarlo"
#         winner = play(copy.deepcopy(game_state),name1, agent2, mode)
#         play_again()
#         return winner
#     elif Gamemode == "3":
#         #MODE 3
#         print("\nMODE 3: AI VS AI")
#         mode = input("Select AI Mode (1, 2, or 3):\n1. MINIMAX (Not Recommended)\n2. ALPHABETA\n3. MONTECARLO\nEnter Mode: ")
#         if mode == "1":
#             mode = "minimax"
#         elif mode == "2":
#             mode = "alphabeta"
#         elif mode == "3":
#             mode = "montecarlo"
#         winner = play(copy.deepcopy(game_state),agent1, agent2, mode)
#         play_again()
#         return winner
            
#     else:
#         print("Invalid Input")


# if __name__ == "__main__":
#     tester()

