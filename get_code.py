from modules.astar import get_path
import math, cv2, numpy as np, toml

def main(start, end):
    junctions = ...
    junctions_inv = ...
    with open('./base/junctions.toml', 'r') as f:
        junctions = toml.load(f)
        junctions_inv = {tuple(v): k for k, v in junctions.items()}

    def get_condition(sensor_vals: list[int]):
        sensor_func = []
        # sensor_func.append(f'{"w" if sensor_vals[0] else "b"}(0)')
        # sensor_func.append(f'{"w" if sensor_vals[2] else "b"}(2)')
        # sensor_func.append(f'{"w" if sensor_vals[4] else "b"}(4)')
        for i in [0, 2, 4]:
            if sensor_vals[i]:
                continue
            sensor_func.append(f'b({i})')
        return ' && '.join(sensor_func)

    maze = cv2.imread('jello2.png')
    path = get_path(maze, start, end)
    orientation = 0
    threshold = 90
    cross_table = []
    robot_path = ""

    # print(maze[path[0][0]][path[0][1]])

    # print("forward")

    for y1, x1, y2, x2, y3, x3 in np.lib.stride_tricks.sliding_window_view(path.flatten(), (6,))[::2]:
        u = [y2 - y1, x2 - x1]
        v = [y3 - y2, x3 - x2]
        w = [-u[1], u[0]]
        angle = math.degrees(math.atan2(u[1], u[0]) - math.atan2(v[1], v[0]))
        angle = angle if angle <= 180 else angle - 360
        angle = angle if angle >= -180 else angle + 360

        direction = ...
        if   angle <= -threshold: direction = 'left'
        elif angle >=  threshold: direction = 'right'
        else                    : direction = 'forward'

        sensors = (
            # TODO: Not hard-coding this
            maze[y2 + 2*w[0]][x2 + 2*w[1]][0] // 255,
            maze[y2 +   w[0]][x2 +   w[1]][0] // 255,
            maze[y2         ][x2         ][0] // 255,
            maze[y2 -   w[0]][x2 -   w[1]][0] // 255,
            maze[y2 - 2*w[0]][x2 - 2*w[1]][0] // 255,
        )
        # print(sensors)
        if sensors in junctions_inv:
            robot_path += f'\t{junctions_inv[sensors]}(); {direction}();\n'
            print(junctions_inv[sensors], direction)
    
    if robot_path[-10:] != "forward();":
        robot_path += "forward();"

    setup = ''
    with open("./base/sim.txt", "r") as f:
        setup = f.read()

    with open('output.txt', 'w') as f:
        f.write(setup)

        for k, v in junctions.items():
            # cond = ' && '.join([f"{'w' if l else 'b'}({i})" for i, l in enumerate(v)])
            cond = get_condition(v)
            print(cond)

            f.write(f"void {k}() {{\n")
            f.write(f"\twhile (true) {{\n")
            f.write(f"\t\tpid();\n")
            f.write(f"\t\tif ({cond}) break;\n")
            f.write(f"\t}}\n")
            f.write(f"\tao();\n")
            f.write(f"}}\n\n")
        
        f.write("void setup() {\n")
        f.write(robot_path)
        f.write("}\n\n")

        f.write("void loop() {}\n")