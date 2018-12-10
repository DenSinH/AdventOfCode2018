import time

"""
This is the naive solution for the problem. I hadn't heard of deque's before, and after finally looking on the 
Reddit to see what other people did, I implemented this in my proper solution
"""

# read the input
with open("input.txt", "r") as f:
    line = f.read().split(" ")
    no_elves = int(line[0])
    highest_marble = int(line[-2])  # add * 100 for part 2

# initial values
scores = [0] * no_elves
elf = 0

marble = 1
marbles = [0]

# index of current
current = 1

t = time.time()

while marble <= highest_marble:
    # report progress
    if marble % 10000 == 0:
        print marble

    # algorithm provided for the game
    if marble % 23 == 0:
        current = (current - 7) % len(marbles)
        scores[elf] += marble + marbles.pop(current)

    else:
        current = (current + 2) % len(marbles)
        marbles.insert(current, marble)

    marble += 1
    elf = (elf + 1) % len(scores)

print max(scores)
print time.time() - t
