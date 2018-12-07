precursors = {}
steps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
workers = {}

# initialize workers
for i in xrange(5):
    # "." is passive
    workers[i] = "."

# initialize precursors
for i in xrange(len(steps)):
    # step ==> [precursors, time left]
    precursors[steps[i]] = [[], 61 + i]

# add precursors and sort them
with open("input.txt", "r") as f:
    for line in f.readlines():
        precursor = line.split(" ")[1]
        step = line.split(" ")[-3]

        precursors[step][0].append(precursor)
        precursors[step][0].sort()

# report for testing
for step in steps:
    print step, precursors[step]

# list of completed steps
completed = ""
# t = -1 because the 'first' step is intialization
t = -1

while len(completed) < len(steps):

    print t, [workers[i] for i in xrange(len(workers))]

    # check if workers are done
    for worker in workers:

        if workers[worker] != ".":

            if precursors[workers[worker]][1] == 0:
                completed += workers[worker]

                # complete the task if they are done
                for l in steps:
                    if workers[worker] in precursors[l][0]:
                        precursors[l][0].remove(workers[worker])

                workers[worker] = "."

            else:
                # otherwise, the time left is one less
                precursors[workers[worker]][1] -= 1

    # any second a step is completed, a new one may be taken immediately
    # when a new step is started, the time left is decreased by 1 second in the same step
    for i in xrange(len(steps)):

        # only add steps that are not done already, can be performed and are not being worked on yet
        if precursors[steps[i]][1] > 0 and not precursors[steps[i]][0] and steps[i] not in workers.values():

            for worker in workers:
                # only non-idle workers may take on a step
                if workers[worker] == ".":
                    workers[worker] = steps[i]
                    precursors[steps[i]][1] -= 1
                    break

    # increment the time
    t += 1

print completed, t
