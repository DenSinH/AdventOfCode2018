import numpy as np
import time

t = time.time()

# input
serial = 3214

# x and y arrays
x, y = np.meshgrid(1 + np.arange(300), 1 + np.arange(300))

# algorithm for power level
rack_ids = 10 + x
power_level = rack_ids * y
power_level += serial
power_level *= rack_ids

power_level = np.floor(power_level / 100) - 10 * np.floor(power_level / 1000)
power_level -= 5


# determining the power at a specific point (not used)
def get_pow(x, y):
    # index of (x, y) is [y - 1, x - 1]
    return power_level[y - 1, x - 1]


# initial values for the maxima
max_pow = -5
max_x = 0
max_y = 0
max_s = 0

# definition of local variables
grid_max = -5
last_s_checked = 0

# storing the maximum (possible) values for values of s
s_to_max = {
    0: 0,
    1: 4
}

for s in xrange(1, 300):
    if not s % 10:
        print s

    """
    Denote old tiles in a square as #, new parts as @ and parts outside of it as .
    We can construct the new squares like this (ex. for s = 6 to s = 8):
    ######@@.....
    ######@@.....
    ######@@.....
    ######@@.....
    ######@@.....
    ######@@.....
    @@@@@@@@.....
    @@@@@@@@.....
    .............
    
    We can build this border out of ds**2 squares. We can build this up out of 2*(s // ds) + 1 blocks with
    values of at most s_to_max[ds] and 2 * (s % ds)*ds blocks with values of at most 4. The maximum possible value
    achievable is thus 
    
    max_possible <= grid_max + s_to_max[ds]*(2*(s // ds) + 1) + 4 * (s % ds) * ds
    
    But we can also build it out of smaller squares we have seen before. The maximum possible value is smaller than
    any way we build it. If we build it out of squares with side s_ and tiles with value 4 for the leftovers, we get
    the formula
    
    max_possible <= grid_max + (ds // s_)*(2*(s // s_) + (ds // s_))*s_to_max[s_] +
                               (ds % s_)*(2*(s % s_) + (ds % s_))*4 for s_ in xrange(1, ds + 1)] + [4*ds*(2*s + ds)
                               
    This is how I got the skipping condition
    """

    # thickness of the border
    ds = s - last_s_checked

    # maximum possible value for the squares
    max_possible = grid_max + min([(ds // s_)*(2*(s // s_) + (ds // s_))*s_to_max[s_] +
                                  (ds % s_)*(2*(s % s_) + (ds % s_))*4 for s_ in xrange(1, ds + 1)] + [4*ds*(2*s + ds)])

    # we need to do part 1 at least
    if s == 3 or max_possible > max_pow:
        # creating the local grid
        grid_size = 300 - s
        s_grid = np.zeros((grid_size, grid_size))

        # add up all the values in the s-square
        for roll_x in xrange(s):
            for roll_y in xrange(s):
                s_grid += np.roll(power_level, -roll_x - 300 * roll_y)[:grid_size, :grid_size]

        # maximum value for the grid
        grid_max = s_grid.max()

        # store it if needed
        if grid_max > max_pow:
            coords = np.nonzero(s_grid == grid_max)
            max_y, max_x = coords[0][0] + 1, coords[1][0] + 1
            max_s = s
            max_pow = int(grid_max)

        # report for s == 3 (part 1)
        if s == 3:
            coords = np.nonzero(s_grid == grid_max)
            print "PART 1: Maximum power:", grid_max
            print "PART 1: At (x, y):", coords[0][0] + 1, coords[1][0] + 1

        # store the last value we checked for s
        last_s_checked = int(s)
        # store the maximum for this value of s as well
        s_to_max[s] = grid_max

    else:
        """
        If we do not evaluate the entire grid, the maximum of the grid is at most the value we estimated it on before
        """
        s_to_max[s] = max_possible

print "Maximum power:", max_pow
print "At (x, y), s:", max_x, max_y, max_s
print "Local grid:", power_level[max_y - 1: max_y - 1 + max_s, max_x - 1: max_x - 1 + max_s]
print time.time() - t
