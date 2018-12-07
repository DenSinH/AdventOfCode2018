import numpy as np
import matplotlib.pyplot as plt
from pylab import cm

# max x = 355
# max y = 349

# limits for the grid
x_min = 0
y_min = 0

x_lim = 400
y_lim = 400

# base list of x_coords and y_coords
x_coords = np.array([np.arange(x_min, x_lim) for y in xrange(y_min, y_lim)])
y_coords = np.array([y*np.ones(x_lim - x_min) for y in xrange(y_min, y_lim)])

# list for points and point distances
points = []
point_ds = []

# read input
with open("input.txt", "r") as f:
    for l in f.readlines():
        line = l.strip("\n")
        (x, y) = (int(i) for i in line.split(", "))
        points.append((x, y))

points = np.array(points)

# find the distances for each point
for point in points:
    point_ds.append(np.abs(x_coords - point[0]) + np.abs(y_coords - point[1]))

# array of shortest distances to some point
shortest_d = np.array(point_ds[0])

# formula for minimum
for i in xrange(1, len(point_ds)):
    shortest_d = (shortest_d + point_ds[i] - np.abs(shortest_d - point_ds[i])) / 2

# finding the closest indices
closest_point = np.zeros(shortest_d.shape)

for i in xrange(len(point_ds)):
    dist_equals_mask = shortest_d == point_ds[i]
    closest_point[dist_equals_mask] = i

# distances might be equal for some points, equidistant points are points where the distance to some point is minimal
# but the index in the array is not equal to this index
for i in xrange(len(point_ds)):
    dist_equals_mask = shortest_d == point_ds[i]
    closest_unequal = closest_point != i
    two_points_equal = np.logical_and(dist_equals_mask, closest_unequal)
    closest_point[two_points_equal] = -1.

# report values (and if they are in the boundary)
for i in sorted(range(len(point_ds)), key=lambda i: np.count_nonzero(closest_point == i)):
    if i in closest_point[:, 0] or i in closest_point[:, -1] or i in closest_point[0, :] or i in closest_point[-1, :]:
        print "IN BOUNDARY:",
    print i, np.count_nonzero(closest_point == i)

plt.figure()

cmap = cm.get_cmap("hsv", len(points) + 1)
cmap.set_under("k")
res_decrease = 1  # 1 is no decrease
plt.pcolormesh(x_coords[::res_decrease], y_coords[::res_decrease], closest_point[::res_decrease], cmap=cmap,
               vmin=0., vmax=len(points) - 1)

plt.colorbar()

plt.scatter(points[:, 0], points[:, 1], color="w", s=1., marker="s")

plt.show()
