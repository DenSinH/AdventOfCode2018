import numpy as np

points = []


# keeping the info for all the points
class Point(object):

    def __init__(self, inp):
        # parsing input of the following format:
        """position=< 9,  1> velocity=< 0,  2>"""
        split_inp = inp.split("<")
        self.x = int(split_inp[1].split(",")[0])
        self.y = int(split_inp[1].split(",")[1].split(">")[0])

        self.xv = int(split_inp[2].split(",")[0])
        self.yv = int(split_inp[2].split(",")[1].split(">")[0])

    def move(self):
        # moving every second
        self.x += self.xv
        self.y += self.yv


# read the input
with open("input.txt", "r") as f:
    for line in f.readlines():
        points.append(Point(line.strip("\n")))


t = 0
while True:
    # the space they will be put in
    space = np.zeros((1, 1))
    t += 1

    # we only wish to increase the size of space (and check if we are done) if the points are close enough
    # otherwise we would cause a MemoryError
    expand_space = False

    # they are close enough if the furthest points in the x-direction are closer than the amount of points
    if max([point.x for point in points]) - min([point.x for point in points]) < len(points):
        expand_space = True

    for point in points:
        # move all points
        point.move()

        # put them in space (and expand space) if they are close enough
        if expand_space:
            # expand space:
            if point.x >= space.shape[0] or point.y >= space.shape[1]:
                new_space = np.zeros((max(point.x + 1, space.shape[0]), max(point.y + 1, space.shape[1])))
                new_space[:space.shape[0], :space.shape[1]] += space
                space = new_space

            space[point.x, point.y] += 1

    # we dont need to check for a word if they are not close enough
    if not expand_space:
        continue

    # we expect that there is a word if all rockets have at least one neighbor
    for point in points:
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                       (0, -1),           (0, 1),
                       (1, -1), (1, 0), (1, 1)]:
            if 0 <= point.x + dx < space.shape[0] and 0 <= point.y + dy < space.shape[1]:
                if space[point.x + dx, point.y + dy] > 0:
                    # break once a neighbor was found
                    break
        else:
            # if we haven't found neighbors for some point, we break
            break
    else:
        # if we found neighbors for all points, we report this and break the loop
        with open("output.txt", "w+") as o:
            for i in xrange(space.shape[1]):
                line = ""
                for j in xrange(space.shape[0]):
                    line += "#" if space[j, i] > 0 else "."
                o.write(line + "\n")
        print t
        break
