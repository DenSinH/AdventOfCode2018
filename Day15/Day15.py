cave = []
units = []


class Unit(object):

    def __init__(self, i, j, typ):
        self.i = i
        self.j = j
        self.typ = typ

        # distances reachable from a starting point (default is our own pos)
        self.dist_trace = []
        self.init_dist_trace()

        # locations in range of an enemy
        self.in_range = []

    def init_dist_trace(self):
        # reset the distances (-1 everywhere except at our position)
        self.dist_trace = [[-1]*len(cave[i]) for i in xrange(len(cave))]
        self.dist_trace[self.i][self.j] = 0

    def get_in_range(self):
        # get all positions in range of an enemy that are not occupied by a unit other than ourself
        self.in_range = []
        for unit in units:
            # has to be enemy
            if unit.typ != self.typ:
                # directions
                for di, dj in [(-1, 0), (1, 0),
                               (0, -1), (0, 1)]:
                    # has to be in the cave
                    if 0 <= unit.i + di < len(cave) and 0 <= unit.j + dj < len(cave[unit.i + di]):
                        # mustn't be wall
                        if cave[unit.i + di][unit.j + dj] == "." and \
                                (unit.i + di, unit.j + dj) not in [(u.i, u.j) if u != self else (-1, -1) for u in units]:
                            self.in_range.append((unit.i + di, unit.j + dj))

    def trace(self, dist=1, start=None, reset=False):
        if reset:
            # reset the distance (for first call only)
            self.init_dist_trace()
        if start is None:
            # starting position
            start = (self.i, self.j)

        # check all directions
        for di, dj in [(-1, 0), (1, 0),
                       (0, -1), (0, 1)]:
            # must be in cave
            if 0 <= start[0] + di < len(cave) and 0 <= start[1] + dj < len(cave[start[0] + di]):
                # must be in cave and not occupied by anyone (ourself doesn't matter)
                if cave[start[0] + di][start[1] + dj] == "." and \
                        (start[0] + di, start[1] + dj) not in [(u.i, u.j) for u in units]:
                    # if distance is lower than for any path found earlier, or if it is the first path we found
                    # (in which case dist_trace will be -1, we change the value for the distance at this point
                    # we also start a new trace from this new starting point, with an increased distance from ourselves
                    if dist <= self.dist_trace[start[0] + di][start[1] + dj] or \
                            self.dist_trace[start[0] + di][start[1] + dj] == -1:

                        self.dist_trace[start[0] + di][start[1] + dj] = dist
                        self.trace(dist=dist + 1, start=(start[0] + di, start[1] + dj))

    def move(self):
        # trace the distances
        self.trace(reset=True)

        # find all reachable points that are in range of an enemy and not occupied
        # in this case, the distance will no longer be -1
        reachable = filter(lambda spot: self.dist_trace[spot[0]][spot[1]] >= 0, set(self.in_range))

        if len(reachable) > 0:
            # if there are any reachable points, find the closest point
            shortest_d_reachable = min([self.dist_trace[spot[0]][spot[1]] for spot in reachable])
            nearest = filter(lambda spot: self.dist_trace[spot[0]][spot[1]] == shortest_d_reachable, reachable)
            # there may be more than one, choose the first one in reading order
            chosen = min(nearest)

            # trace from the other point
            self.trace(start=chosen, reset=True)

            # find the direction to move in
            # this is the one with the shortest distance, and then the first in reading order
            shortest_path = -1
            best_direction = (0, 0)
            for di, dj in [(-1, 0), (0, -1),
                           (0, 1), (1, 0)]:
                if 0 <= self.i + di < len(cave) and 0 <= self.j + dj < len(cave[self.i + di]):
                    dist_this_dir = self.dist_trace[self.i + di][self.j + dj]
                    if shortest_path == -1 or 0 < dist_this_dir < shortest_path:
                        best_direction = (di, dj)
                        shortest_path = dist_this_dir

            # move unit
            self.i += best_direction[0]
            self.j += best_direction[1]

    def act(self):
        self.get_in_range()
        if (self.i, self.j) in self.in_range:
            pass
        else:
            self.move()


# read the cave
with open("testinput.txt", "r") as f:
    lines = f.readlines()
    for i in xrange(len(lines)):
        cave.append(lines[i].strip().replace("E", ".").replace("G", "."))
        for j in range(len(lines[i])):
            if lines[i][j] in "EG":
                units.append(Unit(i, j, lines[i][j]))

# loop used for testing
for t in xrange(10):
    units.sort(key=lambda u: (u.i, u.j))
    for unit in units:
        unit.act()

    for i in xrange(len(cave)):
        l = ""
        for j in xrange(len(cave[i])):
            for u in units:
                if (u.i, u.j) == (i, j):
                    l += u.typ
                    break
            else:
                l += cave[i][j]
        print l
