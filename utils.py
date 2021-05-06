import math
import numpy as np
import random
from random import randint, choice
from copy import deepcopy

class Moves:
    LEFT = [0, -1]
    RIGHT = [0, 1]
    UP = [-1, 0]
    DOWN = [1, 0]

GRID_SIZE = 4

# Function for generating value in empty tile. 0.1 probability for 4 and 0.9 probability for 2.
def generateNewNumber(grid_text):
    empty_spaces = []
    for i in range(len(grid_text)):
        for j in range(len(grid_text[i])):
            if grid_text[i][j] == 0:
                empty_spaces.append([i,j,grid_text[i][j]])
    if len(empty_spaces) - 1 < 0 and not canMakeMoreMoves(grid_text):
        print("game over")
        return grid_text
    elif len(empty_spaces) - 1 < 0:
        return grid_text
    random_empty_position = choice(empty_spaces)
    r = random.random()
    if r >= 0.9: 
        grid_text[random_empty_position[0]][random_empty_position[1]] = 4
    else:
        grid_text[random_empty_position[0]][random_empty_position[1]] = 2
    return grid_text

# Checking whether for given grid, there are any possible moves.
def canMakeMoreMoves(grid):
    canMakeMove = False
    for i1, x in enumerate(grid):
        for i2, y in enumerate(x):
            if i1 + 1 < GRID_SIZE:
                if grid[i1][i2] == grid[i1 + 1][i2]:
                    canMakeMove = True
            if i1 - 1 >= 0:
                if grid[i1][i2] == grid[i1 - 1][i2]:
                    canMakeMove = True
            if i2 - 1 >= 0:
                if grid[i1][i2] == grid[i1][i2 - 1]:
                    canMakeMove = True
            if i2 + 1 < GRID_SIZE:
                if grid[i1][i2] == grid[i1][i2 + 1]:
                    canMakeMove = True
    return canMakeMove


# Checks whether two grids are same or not.
def checkEqualityOfGrids(grid_one, grid_two):
    for i, j in zip(grid_one, grid_two):
        for y, z in zip(i, j):
            if y != z:
                return False
    return True


# Simulates all the possible results for a given state, i.e. LEFT, RIGHT, UP, DOWN.
def StatePossibleSolutions(grid):
    moves = [Moves.LEFT,Moves.RIGHT,Moves.UP,Moves.DOWN]
    possible_states = []
    movements = []
    for a_move in moves:
        grid_curr = deepcopy(grid)
        grid_curr,_ = move(a_move, grid_curr, newNumberFlag=False)
        possible_states.append(grid_curr)
        movements.append(a_move)
    return [possible_states,movements]

# Checks whether for a given grid the parsed direction movement is possible or not.
def checkForValidMove(direction, grid):
    newGrid = deepcopy(grid)
    for i, j in zip(newGrid, grid):
        for y, z in zip(i, j):
            y = z
    cont = True
    visited = []
    while cont:
        cont = False
        empty_spaces = []
        for i1, x in list(enumerate(newGrid))[::-direction[0] if direction[0] else 1]:
            for i2, y in list(enumerate(x))[::-direction[1] if direction[1] else 1]:
                if y != 0:
                    if 0 <= i1 + direction[0] < 4 and 0 <= i2 + direction[1] < 4:
                        if newGrid[i1 + direction[0]][i2 + direction[1]] == y:
                            if (i1, i2) not in visited:
                                newGrid[i1 + direction[0]][i2 + direction[1]] = y * 2
                                newGrid[i1][i2] = 0
                                visited.append((i1 + direction[0], i2 + direction[1]))
                                cont = True
                        elif newGrid[i1 + direction[0]][i2 + direction[1]] == 0:
                            if ((i1, i2)) in visited:
                                visited.remove((i1, i2))
                                visited.append((i1 + direction[0], i2 + direction[1]))
                            newGrid[i1 + direction[0]][i2 + direction[1]] = y
                            newGrid[i1][i2] = 0
                            cont = True
                elif y == 0:
                    empty_spaces.append(y)
    return not checkEqualityOfGrids(grid, newGrid)


# Function to make the move in the grid.
def move(direction, grid_text, game_score = 0, newNumberFlag = True):
    cont = True
    visited = []
    if checkForValidMove(direction, grid_text):
        while cont:
            cont = False
            empty_spaces = []
            for i1, x in list(enumerate(grid_text))[::-direction[0] if direction[0] else 1]:
                for i2, y in list(enumerate(x))[::-direction[1] if direction[1] else 1]:
                    if y != 0:
                        if 0 <= i1 + direction[0] < 4 and 0 <= i2 + direction[1] < 4:
                            if grid_text[i1 + direction[0]][i2 + direction[1]] == y:
                                if (i1, i2) not in visited:
                                    grid_text[i1 + direction[0]][i2 + direction[1]] = y * 2
                                    visited.append((i1 + direction[0], i2 + direction[1]))
                                    grid_text[i1][i2] = 0
                                    cont = True
                                    if newNumberFlag:
                                        game_score = game_score + (y * 2)
                            elif grid_text[i1 + direction[0]][i2 + direction[1]] == 0:
                                if ((i1, i2)) in visited:
                                    visited.remove((i1, i2))
                                    visited.append((i1 + direction[0], i2 + direction[1]))
                                grid_text[i1 + direction[0]][i2 + direction[1]] = y
                                grid_text[i1][i2] = 0
                                cont = True
                    if y == 0:
                        empty_spaces.append(y)
        if newNumberFlag:
            grid_text = generateNewNumber(grid_text)
    return grid_text, game_score