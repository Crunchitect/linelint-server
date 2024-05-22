import cv2


def thin():
    maze = cv2.imread('map.png')

    thinned = cv2.ximgproc.thinning(cv2.bitwise_not(cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)))
    thinned = cv2.bitwise_not(thinned)

    for i, row in enumerate(thinned):
        for j, pixel in enumerate(row):
            if pixel == 255:
                for k in range(4):
                    try:
                        i_offset = 1 if k & 2 else -1
                        j_offset = 1 if k & 1 else -1
                        # print(i_offset, j_offset)
                        if thinned[i + i_offset][j] | thinned[i][j + j_offset] | thinned[i + i_offset * 2][j] | thinned[i][j + j_offset * 2] == 0:
                            thinned[i][j] = 0
                            thinned[i + i_offset][j + j_offset] = 255
                    except IndexError:
                        pass

    cv2.imwrite('jello2.png', thinned)
