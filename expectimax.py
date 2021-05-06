import numpy as np
import utils
import json
from copy import deepcopy
import random

# Heuristic function for weighing the grid cells for preferable upper top corner values.
def patternHeuristics(grid):
    grid = np.array(grid)
    weights = np.array([[50,25,10,5],
                        [25,10, 5,1],
                        [10,5,1,0],
                        [5,1,0,0]])     
    result = np.sum(weights*grid)
    return result

# Heuristic function to penalise different values close to eachother.
def clusterHeuristics(grid):
    grid = np.array(grid)
    penalty = 0
    penalty += np.sum(np.abs(grid[:utils.GRID_SIZE-2,:] - grid[1:utils.GRID_SIZE-1,:]))
    penalty += np.sum(np.abs(grid[2:utils.GRID_SIZE,:] - grid[1:utils.GRID_SIZE-1,:]))
    penalty += np.sum(np.abs(grid[:,:utils.GRID_SIZE-2] - grid[:,1:utils.GRID_SIZE-1]))
    penalty += np.sum(np.abs(grid[:,2:utils.GRID_SIZE] - grid[:,1:utils.GRID_SIZE-1]))

    return penalty/2
 
# Heuristic function to promote formation of values at upper and left edge in incremental pattern.
def monotonicHeuristics(grid):
    grid = np.array(grid)
    grid[grid<1] = 0.1

    score1 = grid[1:utils.GRID_SIZE,0]/grid[:utils.GRID_SIZE-1,0]
    score2 = grid[0,1:utils.GRID_SIZE]/grid[0,:utils.GRID_SIZE-1]

    score = np.sum(score1[score1==2])
    score+= np.sum(score2[score2==2])

    return score * 10

# ----------------------------------------------------------------------------------------------

# Expectimax function to build the tree and go up the tree recursively to attain the score for a node.
def expectimax(grid, depth, maxdepth):
    if depth == 0:
        if not utils.canMakeMoreMoves(grid):
            return (-10000)
        else:
            return patternHeuristics(grid) - clusterHeuristics(grid) + monotonicHeuristics(grid)

    if maxdepth:
        heuristic_val = -1
        all_moves = [utils.Moves.LEFT,utils.Moves.RIGHT,utils.Moves.UP,utils.Moves.DOWN]
        for i in all_moves:
            new_grid = deepcopy(grid)
            new_grid,game_score = utils.move(i, new_grid)
            if utils.checkEqualityOfGrids(new_grid, grid):
                continue
            val = expectimax(new_grid, depth-1, False) + game_score
            if val > heuristic_val:
                heuristic_val = val
        return heuristic_val

    else:
        sum_val = 0
        num = 0
        empty_positions = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 0:
                    empty_positions.append((i,j))
        for cell in empty_positions:
            new_grid = deepcopy(grid)
            x,y = cell
            new_grid[x][y] = 2
            sum_val += expectimax(new_grid, depth-1, True)
            num += 1
        if num == 0:
            return expectimax(grid, depth-1, True)
        return sum_val/num


#  Function to get the next move using the score from the expectimax function for a given grid and depth.
def next_move(grid, depth=4):
    heuristic_val = -1
    heuristic_move = None
    empty_positions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                empty_positions.append((i,j))
    if len(empty_positions)>4:
        pass
    else:
        depth = depth+1
    all_moves = [utils.Moves.LEFT,utils.Moves.RIGHT,utils.Moves.UP,utils.Moves.DOWN]
    for i in all_moves:
        new_grid = deepcopy(grid)
        new_grid, game_score = utils.move(i, new_grid)
        if utils.checkEqualityOfGrids(new_grid, grid):
            continue
        val = expectimax(new_grid, depth-1, False) + game_score
        if val > heuristic_val:
            heuristic_val = val
            heuristic_move = i

    return heuristic_move