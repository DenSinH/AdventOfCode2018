precursors = {}
steps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# initialize precursors
for step in steps:
    precursors[step] = []

# add and sort precursors
with open("input.txt", "r") as f:
    for line in f.readlines():
        precursor = line.split(" ")[1]
        step = line.split(" ")[-3]

        precursors[step].append(precursor)
        precursors[step].sort()

# report for testing
for step in steps:
    print step, precursors[step]

# order of completion
order = ""

# try to complete each step in alphabetical order, until all of them are done
while len(steps) > 0:

    for i in xrange(len(steps)):

        if not precursors[steps[i]]:

            order += steps[i]

            for s in steps:

                try:
                    precursors[s].remove(steps[i])
                except ValueError:
                    pass

            steps = steps[:i] + steps[i + 1:]
            break

print order
