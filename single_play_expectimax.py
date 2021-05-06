import json
import expectimax
import utils
import numpy as np
import random
import sys
import time

game_depth = int(sys.argv[-1])

# Beautify grid to print in command line.
def grid_beautify(grid):
    s = [[str(e) for e in row] for row in grid]
    lens = [max(map(len, col)) for col in zip(*s)]
    formatting = "\t".join('{{:{}}}'.format(x) for x in lens)
    table = [formatting.format(*row) for row in s]
    result = ("\n".join(table))
    return result

# Main Function to execute the Expectimax AI game with given depth for demo purpose.
def main(number_of_plays = 1, Depth_val = game_depth):
    directions = {"LEFT" : [0, -1], "RIGHT" : [0, 1], "UP" : [-1, 0], "DOWN" : [1, 0]}
    executionTimeArr = []
    startTime = time.time()
    init_grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    grid = utils.generateNewNumber(utils.generateNewNumber(init_grid))
    End_game = False
    count = 0

    print("GAME started.")
    for item in grid:
        print(item)
    game_score = 0
    
    # AI playing game till it either wins or loses.
    while End_game == False:
        count += 1
        predicted_direction = expectimax.next_move(grid, depth = Depth_val)
        print("MOVE COUNT: ", count)
        for direction in directions:
            if predicted_direction == directions[direction]:
                print("AI's MOVE: ", direction)
        try:
            # Move to the predicted direction.
            grid, game_score = utils.move(predicted_direction, grid, game_score)
            grid, game_score = utils.move(predicted_direction, grid, game_score)
            print("SCORE: ",game_score)
            beautified_grid = grid_beautify(grid)
            print(beautified_grid,"\n")

        # If game reaches end, record the scores in dictionary.
        except:
            executionTime = float(round(time.time() - startTime, 2))
            executionTimeArr.append(executionTime)
            toggle_move = False
            End_game = True
            win_toggle = False
            grid = np.array(grid).flatten()
            max_value_in_grid = int(max(grid))
            if max_value_in_grid >= 2048:
                win_toggle = True
            print("\n")
            # Printing the results from the game.
            if win_toggle:
                print("GAME WON")
            else:
                print("GAME OVER")
            print("MAX VALUE :",max_value_in_grid)
            print("GAME SCORE :",game_score)
            print("MEAN EXECUTION TIME : %f seconds"%np.mean(executionTimeArr))
main()
