from a1_state import State
from a2_path import Path
from a3_agent import Agent

import random
import copy

def get_human_move(state):
    while True:
        try:
            move_str = input("Enter a move (row,col): ")
            r_string, c_string = move_str.split(",")
            r, c = int(r_string.stript()), int(c_string.stript())
            #validate move
            if not (0 <= r < state.rows and 0 <= c < state)
                print("Invalid Move: Outside the board")
            elif state.grid[r][c] == 0:
                print("Invalid Move: Cell is empty")
            else:
                return (r, c) #Valid Move
        except (ValueError, IndexError):
            print("Invalid Move: Invalid format")

def play(state, agent1, agent2):
    #simulates a session
