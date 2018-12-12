import numpy as np
import copy

# dict of notes
notes = {}

with open("input.txt", "r") as f:
    # read initial state
    line0 = f.readline().strip("\n")
    str_init = "."*5 + line0.split(" ")[2] + "."*5

    # skip empty line
    f.readline()

    # read notes
    for line in f.readlines():
        substate = np.zeros(5)
        for i in xrange(5):
            if line[i] == "#":
                substate[i] = 1.

        # store them using tostring method
        notes[substate.tostring()] = float(line[-2] == "#")

# index of pot 0
# we shift the array to save memory
zero = 5

# create initial row (1 is plant, 0 is not)
row = np.zeros(len(str_init))
for i in xrange(len(str_init)):
    if str_init[i] == "#":
        row[i] = 1

# print this row
print "00", "".join("#" if row[i] else "." for i in xrange(row.size))

# value after 20 generations and generation counting variable
after20 = 0
gen = 1

while True:
    # create new row and a copy of the old row
    new_row = np.zeros(row.size)
    old_row = copy.copy(row)

    # check if plants stay alive
    for i in xrange(2, row.size - 3):
        substate = row[i-2:i + 3]

        # necessary condition for the testinput:
        if substate.tostring() in notes:
            new_row[i] = notes[substate.tostring()]

    # store the new row
    row = copy.copy(new_row)

    # finding out where to start/stop the padding (5 0's at the start and at the end)
    nonzero = row.nonzero()[0]
    padding = np.zeros(nonzero.max() - nonzero.min() + 12)

    # shifting the coordinate of pot 0
    zero -= (nonzero.min() - 6)

    # creating the new row
    padding[6:-6 + 1] += row[nonzero.min():nonzero.max() + 1]
    row = copy.copy(padding)

    # string for comparing old and new row and reporting
    row_str = "".join("#" if row[i] else "." for i in xrange(row.size))

    print zero, str(gen + 1).zfill(2), row_str

    # don't break before gen 20, and store the value for gen 20
    # once a generation is equal to that before it (but shifted), we can stop
    if gen <= 20:
        after20 = np.sum(row*np.arange(-zero, row.size - zero))
    elif row_str == "".join("#" if old_row[i] else "." for i in xrange(old_row.size)):
        break

    gen += 1

# report values
print "After 20 generations:", after20
print "Ater 5 billion generations:", np.sum(row)*(50000000000 - gen) + np.sum(row*np.arange(-zero, row.size - zero))
