import numpy as np
import time as tim

t0 = tim.time()

# read depth and target from input file
with open("input.txt", "r") as f:
    depth = int(f.readline().split(": ")[1])
    target = tuple([int(n) for n in f.readline().split(": ")[1].split(",")])

# find the geological index
geologic_index = np.zeros((target[1] + 50, target[0] + 100))

# these values can be craeted quicker
geologic_index[0, :] = np.arange(geologic_index.shape[1]) * 16807
geologic_index[:, 0] = np.arange(geologic_index.shape[0]) * 48271

# calculate the erosion level for these values already
erosion_level = np.mod(geologic_index + depth, 20183)

# find the rest of the geological indices and erosion levels
for y in xrange(1, geologic_index.shape[0]):
    for x in xrange(1, geologic_index.shape[1]):
        if (x, y) != target:
            geologic_index[y][x] = erosion_level[y][x - 1] * erosion_level[y - 1][x]

        erosion_level[y][x] = (geologic_index[y][x] + depth) % 20183

# find the region types
region_types = np.mod(erosion_level, 3).astype(int)

print "PART 1:", np.sum(region_types[0:target[1] + 1, 0:target[0] + 1])

# tools allowed per region. Tools are ordered climbing gear, neither, torch
tools_by_region = [(0, 2), (0, 1), (1, 2)]
equipped = 2

# find an initial guess (upper bound) for the minimum time needed by going in a straight line down, and then a straight
# line right
best_time = 0

# first go down, then sideways
for c in xrange(2):
    for coord in xrange(1, target[1 - c]):
        # check if we can move
        if equipped in tools_by_region[region_types[(target[0], coord) if c else (coord, 0)]]:
            best_time += 1
        else:
            # change tools otherwise
            best_time += 8
            for tool in tools_by_region[region_types[(target[0], coord) if c else (coord, 0)]]:
                if tool in tools_by_region[region_types[(target[0], coord - 1) if c else (coord - 1, 0)]]:
                    equipped = tool
                    break

# time per tool. We start of at (0, 0) with the torch, so the time here is 0
# all other spots get initialized with the best time we found earlier.
time_with_tool = [best_time*np.ones(region_types.shape).astype(int) for t in xrange(3)]
time_with_tool[2][(0, 0)] = 0

# list of points we need to "flow outward" from still
to_do = []


def find_route(start=(0, 0), eq=2):
    global to_do
    nd_srt = False

    # get the time at the starting point, add one to find the time at the next point
    time = time_with_tool[eq][start] + 1

    # if the time + manhattan distance is more than the best time so far, we can stop, as it would be impossible to
    # reach the goal in a time lower than the best time so far in that case
    if time + abs(start[1] - target[0]) + abs(start[0] - target[1]) > time_with_tool[2][target[::-1]]:
        return

    # flow outward in all directions
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_pos = (start[0] + dy, start[1] + dx)
        # we cannot go below 0 (wrapping would mess things up)
        if new_pos[0] < 0 or new_pos[1] < 0:
            continue

        # stop if we reached the target, (x, y) needs to be reversed
        elif new_pos == target[::-1]:
            if eq == 2:
                if time < time_with_tool[2][new_pos]:
                    time_with_tool[2][new_pos] = time
            else:
                # add 7 if we need to swap tools
                if time + 7 < time_with_tool[2][new_pos]:
                    time_with_tool[2][new_pos] = time + 7

        else:
            try:
                # find the tools allowed in the next region
                new_t_a = tools_by_region[region_types[new_pos]]
                # initial value for the new data of the point flowed towards (contains starting point and tool)
                next_data = {}

                # find out if we need to swap tools
                if eq in new_t_a:
                    # check if this is a new lowest value reached at this point
                    if time < time_with_tool[eq][new_pos]:
                        time_with_tool[eq][new_pos] = time
                        next_data = {"start": new_pos, "eq": eq}
                else:
                    # otherwise, swap tools and do the same
                    for t in tools_by_region[region_types[start]]:
                        if t in new_t_a and time + 7 < time_with_tool[t][new_pos]:
                            time_with_tool[t][new_pos] = time + 7
                            next_data = {"start": new_pos, "eq": t}
                            break

                # check if we are not already checking this point
                if next_data and next_data not in to_do:
                    to_do.append(next_data)

                    if time < time_with_tool[to_do[0]["eq"]][to_do[0]["start"]]:
                        nd_srt = True

            except IndexError:
                pass

    return nd_srt


find_route()
while to_do:
    # we only want to sort if we added a point with a starting value lower than the one we otherwise would do
    # this is not guaranteed to be the best way of handling this, as adding a value of 1 to [0, 2, 3] first and then
    # 2 would not trigger a sort, while that would be desired
    if find_route(**to_do.pop(0)):
        to_do.sort(key=lambda data: time_with_tool[data["eq"]][data["start"]])

print "PART 2:", time_with_tool[2][target[::-1]]
print tim.time() - t0
