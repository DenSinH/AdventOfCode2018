import ast


class Registers(object):

    def __init__(self, vals):
        """
        :param vals: list[int, int, int, int]
        """
        self.vals = vals

    """
    All operations that can be performed on the registers 
    :param: inp: list[int, int, int]
    """
    def addi(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] + inp[1]

    def addr(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] + self.vals[inp[1]]

    def muli(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] * inp[1]

    def mulr(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] * self.vals[inp[1]]

    def bani(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] & inp[1]

    def banr(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] & self.vals[inp[1]]

    def bori(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] | inp[1]

    def borr(self, inp):
        self.vals[inp[-1]] = self.vals[inp[0]] | self.vals[inp[1]]

    def setr(self, inp):
        self.vals[inp[-1]] = int(self.vals[inp[0]])

    def seti(self, inp):
        self.vals[inp[-1]] = inp[0]

    def gtir(self, inp):
        self.vals[inp[-1]] = int(inp[0] > self.vals[inp[1]])

    def gtri(self, inp):
        self.vals[inp[-1]] = int(self.vals[inp[0]] > inp[1])

    def gtrr(self, inp):
        self.vals[inp[-1]] = int(self.vals[inp[0]] > self.vals[inp[1]])

    def eqir(self, inp):
        self.vals[inp[-1]] = int(inp[0] == self.vals[inp[1]])

    def eqri(self, inp):
        self.vals[inp[-1]] = int(self.vals[inp[0]] == inp[1])

    def eqrr(self, inp):
        self.vals[inp[-1]] = int(self.vals[inp[0]] == self.vals[inp[1]])


# samples for part 1
samples = []
with open("input.txt", "r") as f:
    lines = f.readlines()

# storing the line that the test program starts at
test_prog_start = 0

# the samples come in blocks of 4 lines
for i in xrange(len(lines) // 4 + 1):
    sample = []
    # the samples start with "Before", so we can stop looking for samples once this word is not the first word
    if lines[4*i][:6] == "Before":
        # store the information as sample = [before, operation, after]
        sample.append(ast.literal_eval(lines[4*i].split(":")[1].strip()))
        sample.append([int(n) for n in lines[4*i + 1].split(" ")])
        sample.append(ast.literal_eval(lines[4*i + 2].split(":")[1].strip()))
        samples.append(sample)
    else:
        test_prog_start = 4 * i
        break


# read the test program
program = []
for line in lines[test_prog_start:]:
    if line != "\n":
        program.append([int(n) for n in line.split(" ")])


# we are looking for samples that can be multi-interpretable (more than 3 operations apply)
multi_samples = 0

# a register we perform the operations on
registers = Registers([0, 0, 0, 0])

# dict that stores the possible operations per op-code
op_codes = {}

# dict that stores the operation that actually belongs to the op-codes
final_codes = {}

# list of operations in string format
ops = "addr addi mulr muli banr bani borr bori " \
      "eqir eqri eqrr setr seti gtir gtri gtrr".split(" ")

for i in xrange(16):
    op_codes[i] = list(ops)
    final_codes[i] = ""

# go over the samples
for i in range(len(samples)):
    # amount of operations that work for the sample we are looking at
    poss_ops = 0
    sample = samples[i]

    for op in ops:

        try:
            # initialize the registers in the "Before"-state
            registers.vals = list(sample[0])
            # run the operation
            getattr(registers, op)(sample[1][1:])

            # if the output is equal to the "After"-state, we found a possible operation that works for this sample
            if registers.vals == sample[2]:
                poss_ops += 1
            else:
                # otherwise, we can remove this operation from the possible operations for the op code in sample[1]
                try:
                    op_codes[sample[1][0]].remove(op)
                except ValueError:
                    pass

        # since the values in the "Before" state might be larger than 3, an IndexError might occur
        except IndexError:
            pass

    if poss_ops >= 3:
        multi_samples += 1

# find the operations that belong to the operation codes
# we do this by continuously looking at the possible operations for some op-code, and if there is only one possiblity,
# then this must be the operation that belongs to the op-code. It is then not possible for any other op-code
# to code for this operation
while "" in final_codes.values():
    for op_code in final_codes:
        if len(op_codes[op_code]) == 1:

            final_codes[op_code] = op_codes[op_code][0]
            for op_c in final_codes:
                if op_c != op_code and final_codes[op_code] in op_codes[op_c]:
                    op_codes[op_c].remove(final_codes[op_code])


# running the test program we found on the initial state for the registers
registers.vals = [0, 0, 0, 0]
for code in program:
    getattr(registers, final_codes[code[0]])(code[1:])

print "PART 1:", multi_samples
print "PART 2:", registers.vals
