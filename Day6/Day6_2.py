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
total_d = np.zeros(point_ds[0].shape)

for i in xrange(len(point_ds)):
    total_d += point_ds[i]

points_included = np.zeros(total_d.shape)

included_mask = total_d <= 10000
points_included[included_mask] = 1.

print np.count_nonzero(points_included), "points included"

plt.figure()

cmap = cm.get_cmap("binary", 2)

res_decrease = 1  # 1 is no decrease
plt.pcolormesh(x_coords[::res_decrease], y_coords[::res_decrease], points_included[::res_decrease], cmap=cmap,
               vmin=0., vmax=1.)

plt.scatter(points[:, 0], points[:, 1], color="r", s=1., marker="s")

plt.show()
