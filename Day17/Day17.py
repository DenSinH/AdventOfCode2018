import numpy as np

with open("input.txt") as f:
    lines = f.readlines()

walls = []

# make initial state for the scan
for line in lines:
    info = line.strip().split(", ")

    # first coordinate given
    c1 = int(info[0].split("=")[1])
    # second coordinate
    c2_lst = [int(n) for n in info[1].split("=")[1].split("..")]

    for c2 in xrange(c2_lst[0], c2_lst[1] + 1):
        # first can be both x or y
        walls.append((c1, c2) if info[0][0] == "x" else (c2, c1))

# find min/max values for x and y
min_x = min([c[0] for c in walls])
max_x = max([c[0] for c in walls])
min_y = min([c[1] for c in walls])
max_y = max([c[1] for c in walls])

# translate the well to use minimal memory space
well = (500 - min_x + 1, 0)

# add walls to scan
"""
in scan:
    -1: moving water
    0 : empty
    1 : wall
    2 : still water
"""
scan = np.zeros((max_y + 1, max_x - min_x + 1 + 2))  # 2 is for empty borders
for c in walls:
    scan[c[1], c[0] - min_x + 1] = 1


# function to output the scan to check the results
def write_scan():
    with open("output.txt", "w+") as f:
        for y in scan:
            f.write("".join([".#~|"[int(w)] for w in y]) + "\n")


"""
We are going to release droplets from the well. Each droplet will move downward until it hits a 1 or 2, then it will
check to the sides to see if there is a wall. If there is before it can fall down further, it stops, otherwise, a pool
cannot be created, and a new droplet is made to fall down further.
"""
droplets = []


class Droplet(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        # keep dropping down
        while self.y + 1 < scan.shape[0]:
            if scan[self.y + 1, self.x] <= 0:
                self.y += 1
                # leave a trail of moving water
                scan[self.y, self.x] = -1
            else:
                break
        else:
            # droplet reached bottom
            return False

        # keeping track if we can create a puddle
        create_puddle = True
        dx = [0, 0]
        for direction in xrange(2):
            # keep going to the right while we are in the scan, and while there is a 1 or 2 below us
            while self.x + dx[direction] < scan.shape[1] >= 0 >= scan[self.y, self.x + dx[direction]]:
                scan[self.y][self.x + dx[direction]] = -1
                if scan[self.y + 1][self.x + dx[direction]] > 0:
                    # left must decrease, right must increase
                    dx[direction] += (-1)**(direction + 1)
                else:
                    # droplet can fall further
                    if (self.x + dx[direction], self.y) not in [(d.x, d.y) for d in droplets]:
                        droplets.append(Droplet(self.x + dx[direction], self.y))
                    create_puddle = False
                    break

        # if we can create a puddle, set still water where needed
        if create_puddle:
            for x in xrange(self.x + dx[0] + 1, self.x + dx[1]):
                scan[self.y, x] = 2.

        return True


# keeping track of the amount of water spaces (-1 and 2)
water_count = [0]*3

# make an initial movement
Droplet(well[0], well[1]).move()

# add water count and remove 1
water_count.append(np.count_nonzero(np.logical_or(scan[min_y:, :] == 2, scan[min_y:, :] == -1)))
water_count.pop(0)

# keep going until no more water is created
while water_count[-1] != water_count[-3]:
    Droplet(well[0], well[1]).move()

    # keep going until all droplets are gone
    while len(droplets) > 0:
        droplets[0].move()
        droplets.pop(0)

    # keep track of water count
    water_count.append(np.count_nonzero(np.logical_or(scan[min_y:, :] == 2, scan[min_y:, :] == -1)))
    print water_count[-1]
    water_count.pop(0)

write_scan()
print "PART 1:", water_count[-1]
print "PART 2:", np.count_nonzero(scan[min_y:, :] == 2)
