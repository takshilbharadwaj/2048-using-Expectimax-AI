import json
import expectimax
import utils
import numpy as np
import random
import time
import sys

game_iterations = int(sys.argv[len(sys.argv)-2])
game_depth = int(sys.argv[-1])

# Main Function to execute the Expectimax AI over given iterations and recording the results.
def main(number_of_plays = 1, Depth_val = game_depth):
    
    directions = {"LEFT" : [0, -1], "RIGHT" : [0, 1], "UP" : [-1, 0], "DOWN" : [1, 0]}
    store_data = {}
    executionTimeArr = []

    # Initiating for loop with a fresh grid with 2 valued random tiles and other empty tilesfor the given number of iterations.
    for i in range(number_of_plays):
        startTime = time.time()
        init_grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        grid = utils.generateNewNumber(utils.generateNewNumber(init_grid))
        End_game = False
        count = 0

        print("GAME-%d started."%(i+1))

        game_id = "GAME_%d "%(i+1)
        store_data[game_id] = {}
        game_score = 0
        
        # AI playing game till it either wins or loses.
        while End_game == False:
            count += 1
            # Predicting next direction using built expectimax algorithm over the current grid.
            predicted_direction = expectimax.next_move(grid, depth = Depth_val)

            try:
                # Move to the predicted direction.
                grid, game_score = utils.move(predicted_direction, grid, game_score)

            except:
                # If game reaches end, record the scores in dictionary.
                executionTime = float(round(time.time() - startTime, 2))
                executionTimeArr.append(executionTime)
                toggle_move = False
                End_game = True
                win_toggle = False

                grid = np.array(grid).flatten()
                max_value_in_grid = int(max(grid))
                if max_value_in_grid >= 2048:
                    win_toggle = True
                store_data[game_id]["MAX_VALUE"] = max_value_in_grid
                store_data[game_id]["GAME_SCORE"] = game_score
                store_data[game_id]["WIN"] = win_toggle
                
                print("MAX VALUE :",max_value_in_grid)
                print("GAME SCORE :",game_score)
                print("EXECUTION TIME :",executionTime)
                print("GAME-%d complete."%(i+1))
                print("\n")
    
    # Average execution time.
    print("MEAN EXECUTION TIME : %f seconds"%np.mean(executionTimeArr))

    # Write attained results in json file.
    with open(('expectimax_results_%d_depth_%d.json'%(number_of_plays,Depth_val)), 'w') as file:
        json.dump(store_data, file)

main()
