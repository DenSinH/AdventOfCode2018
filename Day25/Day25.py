import numpy as np

# read the points
points = []

with open("input.txt", "r") as f:
    for line in f.readlines():
        points.append([int(n) for n in line.split(",")])

points = np.array(points)
constellations = []

# loop over the points
for point in points:
    const_i = -1

    # loop over all constellations
    i = 0
    while i < len(constellations):
        for p in constellations[i]:
            if np.sum(np.abs(point - p)) <= 3:
                # if we have not added this point to a constellation, add it to this one, and keep stored that it
                # was in this one
                if const_i < 0:
                    const_i = int(i)
                    constellations[i].append(point)
                else:
                    # if we already had found a constellation it was in, we can "connect" these constellations
                    constellations[const_i] += constellations.pop(i)

                    # constellations gets shorter, so we need to lower i, as we increase it later
                    i -= 1
                break
        i += 1

    # if no constellation was found, create a new one
    if const_i == -1:
        constellations.append([point])

print len(constellations)
