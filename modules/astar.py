import cv2, numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from copy import deepcopy

def get_closest_black_pixel(point, maze):
    nonzero = cv2.findNonZero(cv2.bitwise_not(maze))
    distances = np.sqrt((nonzero[:,:,0] - point[0]) ** 2 + (nonzero[:,:,1] - point[1]) ** 2)
    nearest_index = np.argmin(distances)
    print(nonzero[nearest_index])
    return nonzero[nearest_index][0][::-1]

def get_path(maze, start, end):
    matrix = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)
    (_, matrix) = cv2.threshold(matrix, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    matrix_p = deepcopy(matrix)
    matrix = cv2.bitwise_not(matrix).transpose().tolist()
    grid = Grid(matrix=matrix)

    # start = grid.node(104, 45)
    # end = grid.node(98, 434)

    startx = grid.node(*get_closest_black_pixel(start, matrix_p))
    endx = grid.node(*get_closest_black_pixel(end, matrix_p))
    print(startx.x, startx.y, endx.x, endx.y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(startx, endx, grid)

    print('operations:', runs, 'path length:', len(path))
    return np.array([[node.x, node.y] for node in path])