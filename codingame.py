import sys
import copy
from collections import deque as queue

# Constant
FIELD_MAX_X = 30
FIELD_MAX_Y = 20
INFINITY = FIELD_MAX_X * FIELD_MAX_Y
WALL = -1
DIRECTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]
dRow = [-1, 0, 1, 0]
dCol = [0, -1, 0, 1]


# Functions

# Check if move is valid
def isValid(grid, vis, row, col):
    # If cell lies out of bounds
    if row < 0 or col < 0 or row >= len(grid[0]) or col >= len(grid):
        return False

    # If cell is already visited
    if vis[col][row]:
        return False

    # If cell is a wall
    if grid[col][row] == -1:
        return False

    # Otherwise
    return True


# Function to perform the BFS traversal
def BFS(grid, vis, row, col):
    mapped_field = copy.deepcopy(grid)
    # Stores indices of the matrix cells
    q = queue()

    # Mark the starting cell as visited
    # and push it into the queue
    q.append((row, col))
    vis[col][row] = True

    # Iterate while the queue
    # is not empty

    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]

        # q.pop()
        # Go to the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if isValid(grid, vis, adjx, adjy):
                if mapped_field[y][x] == -1:
                    mapped_field[adjy][adjx] = mapped_field[y][x] + 2
                else:
                    mapped_field[adjy][adjx] = mapped_field[y][x] + 1

                q.append((adjx, adjy))
                vis[adjy][adjx] = True

    return mapped_field


# Voronoi algorithm
def voronoi(game_field, pos, n):
    voronoi_field = [([(-1, (FIELD_MAX_X * FIELD_MAX_Y))] * FIELD_MAX_X) for i in range(FIELD_MAX_Y)]
    for i in range(n):
        visited = [[False] * FIELD_MAX_X for i in range(FIELD_MAX_Y)]
        x = pos[i][0]
        y = pos[i][1]

        mapped_field = BFS(game_field, visited, x, y)

        voronoi_field[y][x] = (i, 0)
        for row in range(FIELD_MAX_Y):
            for col in range(FIELD_MAX_X):
                if game_field[row][col] < 0:
                    voronoi_field[row][col] = (-1, 0)
                else:
                    curr_val = mapped_field[row][col]
                    val = voronoi_field[row][col][1]
                    if val > curr_val:
                        voronoi_field[row][col] = (i, curr_val)
    return voronoi_field


# Display output of Voronoi
def display_state(voronoi_field):
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CWHITE = '\33[37m'
    colors = [CVIOLET, CYELLOW, CBLUE, CGREEN, CWHITE]
    for row in range(FIELD_MAX_Y):
        line = voronoi_field[row]
        print("[ ", end="")
        for col in range(FIELD_MAX_X):
            if line[col][0] != -1:
                print(" " + colors[line[col][0]] + ("0" + str(line[col][1]))[-2:] + colors[-1] + " ", end="")
            else:
                print(" XX ", end="")
        print("]")


# Count the number of cells a certain player controls
def my_score(voronoi_field, j_ind):
    acc = 0
    for row in range(FIELD_MAX_Y):
        line = voronoi_field[row]
        for col in range(FIELD_MAX_X):
            if line[col][0] != -1 and line[col][0] == j_ind:
                acc += 1
    return acc


# Evaluation function of possibles moves
def get_possible_score(grid_history, players_pos, j_ind, n, debug):
    res = []
    # Order is TOP, RIGHT, BOT, LEFT
    for i in range(4):
        j_possible_pos = copy.deepcopy(players_pos)
        grid_future = copy.deepcopy(grid_history)
        if i == 0:
            if j_possible_pos[j_ind][1] > 0 and grid_history[j_possible_pos[j_ind][1] - 1][j_possible_pos[j_ind][0]] != WALL:
                j_possible_pos[j_ind][1] -= 1
            else:
                res.append(WALL)
                continue
        elif i == 1:
            if j_possible_pos[j_ind][0] < FIELD_MAX_X - 1 and grid_history[j_possible_pos[j_ind][1]][j_possible_pos[j_ind][0] + 1] != WALL:
                j_possible_pos[j_ind][0] += 1
            else:
                res.append(WALL)
                continue
        elif i == 2:
            if j_possible_pos[j_ind][1] < FIELD_MAX_Y - 1 and grid_history[j_possible_pos[j_ind][1] + 1][j_possible_pos[j_ind][0]] != WALL:
                j_possible_pos[j_ind][1] += 1
            else:
                res.append(WALL)
                continue
        else:
            if j_possible_pos[j_ind][0] > 0 and grid_history[j_possible_pos[j_ind][1]][j_possible_pos[j_ind][0] - 1] != WALL:
                j_possible_pos[j_ind][0] -= 1
            else:
                res.append(WALL)
                continue

        grid_future[j_possible_pos[j_ind][1]][j_possible_pos[j_ind][0]] = -1
        vor_map = voronoi(grid_future, j_possible_pos, n)

        if debug:
            print("=" * 50)
            display_state(vor_map)
            print("=" * 50)

        score = my_score(vor_map, j_ind)
        res.append(score)
    return res


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# Default data
grid_history = [([INFINITY] * FIELD_MAX_X) for i in range(FIELD_MAX_Y)]  # Grid informations of cells still empty

# game loop
while True:
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    n, p = [int(i) for i in input().split()]
    pos = []

    for i in range(n):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        pos.append([x0, y0, x1, y1])
        grid_history[y1][x1] = -1
        grid_history[y0][x0] = -1

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    x1 = pos[p][2]
    y1 = pos[p][3]

    xJ1 = pos[0][2]
    yJ1 = pos[0][3]
    xJ2 = pos[1][2]
    yJ2 = pos[1][3]

    if n > 2:  # If 3 players
        xJ3 = pos[2][2]
        yJ3 = pos[2][3]
    else:
        xJ3 = 0
        yJ3 = 0

    if n > 3:  # If 4 players
        xJ4 = pos[3][2]
        yJ4 = pos[3][3]
    else:
        xJ4 = 0
        yJ4 = 0

    player_score = []  # Player score for each direction ordered by UP, RIGHT, DOWN, LEFT
    player_score = get_possible_score(grid_history, [[xJ1, yJ1], [xJ2, yJ2], [xJ3, yJ3], [xJ4, yJ4]], p, n, False)

    print(player_score, file=sys.stderr, flush=True)

    i = 0
    while i < len(player_score):
        best_direction = player_score.index(max(player_score))
        print(best_direction, file=sys.stderr, flush=True)
        player_score[best_direction] = WALL
        # Moves authorized if cell not empty and that direction dont lead to a wall
        if DIRECTIONS[best_direction] == "LEFT" and x1 > 0 and grid_history[y1][x1 - 1] == INFINITY:
            print(DIRECTIONS[3])  # LEFT
            break
        elif DIRECTIONS[best_direction] == "UP" and y1 > 0 and grid_history[y1 - 1][x1] == INFINITY:
            print(DIRECTIONS[0])  # UP
            break
        elif DIRECTIONS[best_direction] == "RIGHT" and x1 < (FIELD_MAX_X - 1) and grid_history[y1][x1 + 1] == INFINITY:
            print(DIRECTIONS[1])  # RIGHT
            break
        elif DIRECTIONS[best_direction] == "DOWN" and y1 < (FIELD_MAX_Y - 1) and grid_history[y1 + 1][x1] == INFINITY:
            print(DIRECTIONS[2])  # DOWN
            break
        i += 1

    if i == len(player_score):
        print(DIRECTIONS[0])

#####################################
#####################################

# TEST
"""
# Players position
xJ1 = 3
yJ1 = 15
xJ2 = 5
yJ2 = 17

# Set their positions on the field
grid_history = [([INFINITY] * FIELD_MAX_X) for i in range(FIELD_MAX_Y)]

grid_history[yJ2][xJ2+1] = -1

for j2c in range(16):
    grid_history[yJ2-j2c][xJ2] = -1
for j2l in range(24):
    grid_history[1][xJ2+j2l] = -1
    
for j1c in range(16):
    grid_history[0+j1c][xJ1] = -1
for j1l in range(26):
    grid_history[0][xJ1+j1l] = -1

for i in range(len(grid_history)):
    print(grid_history[i])
    

xJ1 = 28
yJ1 = 0
xJ2 = 28
yJ2 = 1

player_score = [] # Player score for each directions ordered by UP, RIGHT, DOWN, LEFT
player_score = get_possible_score(grid_history, [[xJ2, yJ2], [xJ1, yJ1]], 0, 2, True)
print("res", player_score)

best_direction = player_score.index(max(player_score))
print("On optimise le parcours en allant à ", DIRECTIONS[best_direction])
"""
