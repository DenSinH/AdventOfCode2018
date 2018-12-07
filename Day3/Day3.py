import numpy as np

cloth = np.zeros((10, 10))

with open("input.txt", "r") as f:

    for line in f.readlines():
        l = line.split(" ")
        # [:-1] for the :  and the \n

        x, y = (int(i) for i in l[2][:-1].split(","))
        w, h = (int(i) for i in l[3][:-1].split("x"))

        # for easier comparison, the cloth will always be square
        max_coords = max(x + w, y + h)
        if cloth.size < max_coords**2:
            new_cloth = np.zeros((max_coords, max_coords))
            new_cloth[0:cloth.shape[0], 0:cloth.shape[1]] += cloth
            cloth = np.array(new_cloth)

        cloth[x:x + w, y:y + h] += np.ones((w, h))

print cloth.shape
print cloth[cloth >= 2].size

with open("input.txt", "r") as f:

    for line in f.readlines():
        l = line.split(" ")
        # [:-1] for the :  and the \n

        x, y = (int(i) for i in l[2][:-1].split(","))
        w, h = (int(i) for i in l[3][:-1].split("x"))

        if np.all(cloth[x: x + w, y:y + h] == np.ones((w, h))):
            print line
