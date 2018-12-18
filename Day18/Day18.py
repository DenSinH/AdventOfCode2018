import numpy as np
import copy
import time

# keeping track of runtime
t0 = time.time()

# create initial state
state = []

with open("input.txt", "r") as f:
    for line in f.readlines():
        state.append([{".": 0, "|": 1, "#": 2}[char] for char in line.strip("\n")])

state = np.array(state)


def next_state(old):
    # number of things of a certain type, 0: ., 1: |, 2: #
    # this is in the form of an array the shape of old
    no_by_typ = []

    for typ in xrange(3):
        # find the positions with this value in the old state
        old_by_type = np.zeros(old.shape)
        old_by_type[old == typ] = 1

        # pad this state with zeros to roll it without carryover
        padded_old_by_typ = np.pad(old_by_type, ((1, 1), (1, 1)), mode="constant")
        # keeping track of count
        count = np.zeros(padded_old_by_typ.shape)

        # roll in all directions
        for iroll in [-1, 0, 1]:
            for jroll in [-1, 0, 1]:
                count += np.roll(np.roll(padded_old_by_typ, iroll, axis=0), jroll, axis=1)

        # we must subtract the initial count, as (0, 0) is also rolled
        # we remove the padding
        no_by_typ.append((count - padded_old_by_typ)[1:-1, 1:-1])

    # find the new state
    new = np.zeros(old.shape)

    # conditions for the evolution
    new[np.logical_and(old == 0, no_by_typ[1] >= 3)] = 1
    new[old == 1] = 1
    new[np.logical_and(old == 1, no_by_typ[2] >= 3)] = 2
    new[np.logical_and(old == 2, np.logical_and(no_by_typ[1] >= 1, no_by_typ[2] >= 1))] = 2

    return new


# function to print out a given state st
def print_state(st):
    for i in xrange(st.shape[0]):
        print "".join([".|#"[int(k)] for k in st[i]])


# keeping track of old states and resource numbers
prev_states = {}
resources = []
t = 0

# initial values for trees and lumberyards
trees = np.count_nonzero(state == 1)
lumb = np.count_nonzero(state == 2)


# keep going until we have already had this state
while state.tostring() not in prev_states:
    # record the old state
    prev_states[state.tostring()] = t
    resources.append(trees*lumb)

    # create a new state
    state = copy.copy(next_state(state))

    # increase time, and refresh resources
    t += 1

    trees = np.count_nonzero(state == 1)
    lumb = np.count_nonzero(state == 2)


# report part 1
print "PART 1:", resources[10]

# find the start of the periodic movement (first time encountering the last state we calculated) and its period
start_period = prev_states[state.tostring()]
period = t - start_period

# find how much time is left until 1000000000, and find the phase of the periodic movement at that time
time_left = 1000000000 - start_period
phase = time_left % period

# report the resource number of this time (equal to the first time we encountered that state)
print "PART 2:", resources[start_period + phase]
print "runtime", time.time() - t0
