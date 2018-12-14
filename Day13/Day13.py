rails = []
carts = []


class Cart(object):

    # directions for initialization
    dirs = {
        "v": (1, 0),
        "^": (-1, 0),
        "<": (0, -1),
        ">": (0, 1)
    }

    def __init__(self, i, j, dir):
        # i, j positions and initial direction
        self.i = i
        self.j = j
        self.dir = self.dirs[dir]

        # direction to go at crosses
        self.turns = "<.>"
        self.turn = 0

    def turn_dir(self):
        # new direction after crosses
        if self.turns[self.turn] == "<":
            return -self.dir[1], self.dir[0]
        elif self.turns[self.turn] == ".":
            return self.dir
        else:
            return self.dir[1], -self.dir[0]

    def turn_corner(self, corner):
        # new direction after corner
        # the new direction for / is - the new direction for \, hence the typ variable
        typ = 1 if corner == "\\" else -1
        if self.dir == (0, 1):
            return typ, 0
        elif self.dir == (-1, 0):
            return 0, -typ
        elif self.dir == (0, -1):
            return -typ, 0
        return 0, typ

    def move(self):
        # moving and determining the new direction
        self.i += self.dir[0]
        self.j += self.dir[1]

        if rails[self.i][self.j] == "+":
            self.dir = self.turn_dir()
            self.turn = (self.turn + 1) % 3

        elif rails[self.i][self.j] in "\\/":
            self.dir = self.turn_corner(rails[self.i][self.j])

        elif rails[self.i][self.j] not in "|-":
            print "SOMETHING WENT WRONG", rails[self.i][self.j]

        # checking for crashes and returning if we are still alive
        for c in carts:
            if c != self and c.i == self.i and c.j == self.j:
                print "CRASHED AT (y, x)", self.i, self.j
                return False
        return True


# reading the rail system
with open("input.txt", "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        row = ""
        for j in range(len(lines[i].strip("\n"))):
            char = lines[i].strip("\n")[j]

            # change character if we find a cart
            if char in "v<>^":
                carts.append(Cart(i, j, char))
                row += {"v": "|", "<": "-", ">": "-", "^": "|"}[char]
            else:
                row += char
        rails.append(row)


while True:
    # we cannot remove the carts while we are updating them
    to_remove = []

    # update them from top to bottom
    """
    It might go wrong if they collide like this: ><<
    """
    for cart in sorted(carts, key=lambda cart: (cart.i, cart.j)):
        if not cart.move():
            # location of the crash
            crash_loc = cart.i, cart.j
            for c in xrange(len(carts)):
                if (carts[c].i, carts[c].j) == crash_loc:
                    to_remove.append(c)

    # remove the carts we need to
    for d in xrange(len(to_remove)):
        del carts[to_remove[d] - d]

    # report the last cart
    if len(carts) == 1:
        print "LAST CART, (y, x):", carts[0].i, carts[0].j
        break
