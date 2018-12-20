# read input file
with open("input.txt", "r") as f:
    inp = f.readline()[1:-2]


class Path(object):

    # using ij notation for N, E, S, W directions
    dirs = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

    def __init__(self, path, main=True):
        self.path = []
        self.children = []

        current_path = ""  # current parent path
        current_children = []  # current children in ()
        open_count = 0  # keeping track of depth of ()
        child_start = 0  # latest index of child found

        for i in xrange(len(path)):
            char = path[i]

            # we cannot have a negative parenthesis count
            assert open_count >= 0
            if char == "(":
                # start looking for children if () layer is 0 (1 after this)
                if open_count == 0:
                    child_start = int(i)
                    self.path.append(current_path)
                    current_path = ""
                open_count += 1

            elif char == ")":
                open_count -= 1

                # if we are at the parent layer again, add the children to the children list, and reset values
                if open_count == 0:
                    current_children.append(Path(path[child_start + 1:i], main=False))
                    child_start = 0

                    self.children.append(current_children)
                    current_children = []

            elif open_count == 0:
                # add character to parent path if depth is 0
                current_path += char
            elif open_count == 1:
                # if depth is 1, we might have multiple children in 1 layer
                if char == "|" and child_start != 0:
                    current_children.append(Path(path[child_start + 1:i], main=False))
                    child_start = int(i)

        assert open_count == 0, "Missing closing parenthesis"
        self.path.append(current_path)
        self.children.append(current_children)
        assert len(self.path) == len(self.children)

        self.doors = {}
        self.dist_chart = {}
        if main:
            self.doors = self.find_doors()

    def find_doors(self, start=(0, 0)):
        # walking the route
        (x, y) = start
        doors = {}

        for i in xrange(len(self.path)):
            for dr in self.path[i]:
                doors[(x + self.dirs[dr][0], y + self.dirs[dr][1])] = 1
                x += 2*self.dirs[dr][0]
                y += 2*self.dirs[dr][1]

            for child in self.children[i]:
                doors = dict(doors, **child.find_doors(start=(x, y)))

        return doors

    def flow(self, start=(0, 0), dist=1):
        # flow outward once
        to_do = []

        # check all directions
        for (di, dj) in self.dirs.values():
            # must be a door in this direction
            door_pos = (start[0] + di, start[1] + dj)
            if door_pos in self.doors:
                # new position from moving in this direction
                new_pos = (start[0] + 2*di, start[1] + 2*dj)
                # only change dist/create new to_do if we haven't reached this point before or if we found
                # a shorter path
                if new_pos not in self.dist_chart or self.dist_chart[new_pos] > dist:
                    self.dist_chart[new_pos] = dist
                    to_do.append((new_pos, dist + 1))

        return to_do

    def get_dist(self):
        # couldn't do recursion, so had to do it this way...
        to_do = [((0, 0), 1)]
        while len(to_do) > 0:
            new_pos, new_dist = to_do.pop(0)
            to_do += self.flow(start=new_pos, dist=new_dist)

    def __str__(self):
        # string representation of this tree
        """This wont work on the actual input because of recursion depth, but was nice for testing"""
        out = ""
        for i in xrange(len(self.path)):
            out += self.path[i]
            for child in self.children[i]:
                for line in str(child).split("\n"):
                    out += "\n    " + line

        return out

    def __repr__(self):
        return self.__str__()


test = Path(inp)

drs = sorted(test.find_doors().keys())
print len(drs), "doors found"

test.get_dist()
print "PART 1:", max(test.dist_chart.values())
print "PART 2:", len(filter(lambda dist: dist >= 1000, test.dist_chart.values()))
