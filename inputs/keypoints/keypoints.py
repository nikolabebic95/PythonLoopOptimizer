import os
import math


def distance_point_to_line(x0, y0, x1, y1, x2, y2):
    return (math.fabs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)) / (math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))


def is_negative(x1, y1, x2, y2, x3, y3):
    d = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    return d < 0


def process_one_line(relative_path, line_index, floats):
    x0 = float(floats[0])
    y0 = float(floats[1])
    xx = float(floats[2])
    yx = float(floats[3])
    xy = float(floats[4])
    yy = float(floats[5])
    x1 = float(floats[6])
    y1 = float(floats[7])

    out_x = distance_point_to_line(x1, y1, x0, y0, xy, yy)
    out_y = distance_point_to_line(x1, y1, x0, y0, xx, yx)

    if is_negative(x0, y0, xy, yy, x1, y1) != is_negative(x0, y0, xy, yy, xx, yx):
        out_x = -out_x
    if is_negative(x0, y0, xx, yx, x1, y1) != is_negative(x0, y0, xx, yx, xy, yy):
        out_y = -out_y
    print(relative_path, line_index, out_x, out_y)


def keypoints():
    folder = "keypoints_tests/set"
    for sub_folder in os.listdir(folder):
        for file_name in os.listdir(os.path.join(folder, sub_folder)):
            with open(os.path.join(folder, sub_folder, file_name), "r") as file:
                lines = file.readlines()
                i = 0
                for line in lines:
                    floats = line.split()
                    process_one_line(os.path.join(sub_folder, file_name), i, floats)
                    i = i + 1


if __name__ == '__main__':
    from time import time
    start = time()
    keypoints()
    end = time()
    print(end - start)
