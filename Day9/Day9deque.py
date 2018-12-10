from collections import deque
import time

"""
This solution used deque's, which I hadn't heard of before, but were a perfect fit for this problem
"""

# read input
with open("input.txt", "r") as f:
    line = f.read().split(" ")
    no_elves = int(line[0])
    highest_marble = int(line[-2])  # add * 100 for part 2

# initial values
scores = [0] * no_elves
elf = 0

marble = 1
marbles = deque([0])

# index of current
current = 1

t = time.time()

while marble <= highest_marble:

    # report progress
    if marble % 100000 == 0:
        print marble

    # algorithm provided for the game
    if marble % 23 == 0:
        marbles.rotate(-7)
        scores[elf] += marble + marbles.pop()
    else:
        marbles.rotate(2)
        marbles.append(marble)

    marble += 1
    elf = (elf + 1) % len(scores)

print max(scores)
print time.time() - t
