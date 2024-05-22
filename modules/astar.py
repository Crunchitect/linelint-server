import cv2, numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def get_closest_black_pixel(point, maze):
    print(point)
    distance = 0
    while True:
        for x in range(distance):
            y = distance - x
            for sign in [[-1, -1], [1, 1], [-1, 1], [1, -1]]:
                sx, sy = sign
                if maze[point[1] + (sy * y)][point[0] + (sx * x)]:
                    print([point[1] + (sy * y), point[0] + (sx * x)])
                    return [point[0] + (sx * x), point[1] + (sy * y)]
        distance += 1

def get_path(maze, start, end):
    matrix = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)
    (_, matrix) = cv2.threshold(matrix, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    matrix = cv2.bitwise_not(matrix).transpose().tolist()
    grid = Grid(matrix=matrix)

    # start = grid.node(104, 45)
    # end = grid.node(98, 434)

    startx = grid.node(*get_closest_black_pixel(start, matrix))
    endx = grid.node(*get_closest_black_pixel(end, matrix))
    print(startx.x, startx.y, endx.x, endx.y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(startx, endx, grid)

    print('operations:', runs, 'path length:', len(path))
    return np.array([[node.x, node.y] for node in path])