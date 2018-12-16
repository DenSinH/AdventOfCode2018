cave = []
units = []


class Unit(object):

    def __init__(self, i, j, typ, atk):
        # base stats
        self.i = i
        self.j = j
        self.typ = typ

        self.hp = 200
        self.atk = atk

        # keeping track of alive units
        self.alive = True

        # distances reachable from a starting point (default is our own pos)
        self.dist_trace = []
        self.init_dist_trace((self.i, self.j))

        # keeping track of occupied spaces (by others)
        self.occupied = []

        # locations in range of an enemy
        self.in_range = []

    def init_dist_trace(self, pos):
        # reset the distances (-1 everywhere except at pos, which is where we start tracing)
        self.dist_trace = [[-1]*len(cave[i]) for i in xrange(len(cave))]
        self.dist_trace[pos[0]][pos[1]] = 0

    def get_in_range(self):
        # get all positions in range of an enemy that are not occupied by a unit other than ourself
        self.in_range = []
        for unit in units:
            # has to be enemy
            if unit.typ != self.typ and unit.alive:
                # directions
                for di, dj in [(-1, 0), (1, 0),
                               (0, -1), (0, 1)]:
                    # has to be in the cave
                    if 0 <= unit.i + di < len(cave) and 0 <= unit.j + dj < len(cave[unit.i + di]):
                        # mustn't be wall
                        if cave[unit.i + di][unit.j + dj] == "." and \
                                (unit.i + di, unit.j + dj) not in self.occupied:
                            self.in_range.append((unit.i + di, unit.j + dj))

    def get_occupied(self):
        # finding all the occupied spaces
        self.occupied = [(u.i, u.j) if u != self and u.alive else (-1, -1) for u in units]

    def trace(self, start=None, reset=False, left_to_check=None):
        if start is None:
            # starting position
            start = (self.i, self.j)
        if reset:
            # reset the distance (for first call only)
            self.init_dist_trace(start)
        if left_to_check is None:
            left_to_check = []

        dist = self.dist_trace[start[0]][start[1]] + 1

        # check all directions
        for di, dj in [(-1, 0), (1, 0),
                       (0, -1), (0, 1)]:
            # must be in cave
            if 0 <= start[0] + di < len(cave) and 0 <= start[1] + dj < len(cave[start[0] + di]):
                # must be in cave and not occupied by anyone (ourself doesn't matter)
                if cave[start[0] + di][start[1] + dj] == "." and \
                        (start[0] + di, start[1] + dj) not in self.occupied:
                    # if distance is lower than for any path found earlier, or if it is the first path we found
                    # (in which case dist_trace will be -1, we change the value for the distance at this point
                    # we also start a new trace from this new starting point, with an increased distance from ourselves
                    if dist < self.dist_trace[start[0] + di][start[1] + dj] or \
                            self.dist_trace[start[0] + di][start[1] + dj] == -1:

                        self.dist_trace[start[0] + di][start[1] + dj] = dist
                        left_to_check.append((start[0] + di, start[1] + dj))

        # to speed things up, we 'flow outward' from the starting point
        if len(left_to_check) > 0:
            new_start = left_to_check[0]
            self.trace(start=new_start, left_to_check=left_to_check[1:])

    def move(self):
        # trace the distances
        self.trace(reset=True)

        # find all reachable points that are in range of an enemy and not occupied
        # in this case, the distance will no longer be -1
        reachable = filter(lambda spot: self.dist_trace[spot[0]][spot[1]] >= 0, self.in_range)

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
                    if 0 <= dist_this_dir:
                        if shortest_path == -1 or dist_this_dir < shortest_path:
                            best_direction = (di, dj)
                            shortest_path = dist_this_dir

            # move unit
            self.i += best_direction[0]
            self.j += best_direction[1]

    def get_hit(self, atk):
        # get hit by enemy
        self.hp -= atk
        if self.hp <= 0:
            self.alive = False

    def attack(self):
        # find enemies within our own range
        units_in_range = filter(lambda i: units[i].alive and units[i].typ != self.typ and
                                              abs(units[i].i - self.i) + abs(units[i].j - self.j) == 1, range(len(units)))

        if len(units_in_range) > 0:
            # choose the one with the lowest hp, and then in reading order
            chosen = sorted(units_in_range, key=lambda i: (units[i].hp, units[i].i, units[i].j))[0]
            units[chosen].get_hit(self.atk)

    def act(self):
        # find all occupied spaces first (this messed me up at first)
        self.get_occupied()
        # then find all spots that are in range of enemies, and not occupied
        self.get_in_range()
        # move if we can't attack, and try to attack afterwards
        if not (self.i, self.j) in self.in_range:
            self.move()
        self.attack()


# we will look for all attack powers
elve_atk_pow = 3
with open("input.txt", "r") as f:
        lines = f.readlines()

while True:
    print elve_atk_pow

    # we re-initialize everything
    # the cave doesn't need to be re-initialized, but it is easier this way
    no_elves = 0
    cave = []
    units = []

    # read the cave
    for i in xrange(len(lines)):
        cave.append(lines[i].strip().replace("E", ".").replace("G", "."))
        for j in range(len(lines[i])):
            if lines[i][j] == "E":
                units.append(Unit(i, j, "E", elve_atk_pow))
                no_elves += 1
            elif lines[i][j] == "G":
                units.append(Unit(i, j, "G", 3))

    # simulation
    t = 0
    while True:
        # take turns
        units.sort(key=lambda u: (u.i, u.j))
        for unit in units:
            if unit.alive:
                unit.act()

        # remove dead units
        k = 0
        while k < len(units):
            if not units[k].alive:
                del units[k]
            else:
                # remove # to see unit stats each round
                # print t + 1, units[k].i, units[k].j, units[k].typ, units[k].hp
                k += 1

        # remove """ to see board every round
        """
        for i in xrange(len(cave)):
            l = ""
            for j in xrange(len(cave[i])):
                for u in units:
                    if u.alive and (u.i, u.j) == (i, j):
                        l += u.typ
                        break
                else:
                    l += cave[i][j]
            print t + 1, l
        """

        # if there are only creatures of one type left, we stop the simulation
        if len(set([u.typ for u in units])) == 1:
            break

        # otherwise, a full round has been completed, and we proceed
        t += 1

    # reporting part 1 and 2
    if elve_atk_pow == 3:
        print "PART 1", t, sum([u.hp for u in units]), t*sum([u.hp for u in units])
    elif len(units) == no_elves and units[0].typ == "E":
        print elve_atk_pow
        print "PART 2", t, sum([u.hp for u in units]), t*sum([u.hp for u in units])
        break

    elve_atk_pow += 1
