import numpy as np


class Registers(object):

    def __init__(self, vals, ip):
        """
        :param vals: list[int, int, int, int]
        """
        self.ip = ip
        self.vals = np.array(vals)

    """
    All operations that can be performed on the registers 
    :param: inp: list[int, int, int]
    """
    def point(self):
        return self.vals[self.ip]

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


program = []
with open("input.txt", "r") as f:
    ip = int(f.readline()[-2:])
    lines = f.readlines()
    for line in lines:
        # (code, [regs]) for all commands
        program.append((line.split(" ")[0], np.array([int(n) for n in line.split(" ")[1:]])))


# a register we perform the operations on
registers = Registers([0, 0, 0, 0, 0, 0], ip)

# run the operation
while True:
    # run the operation in the program
    getattr(registers, program[registers.point()][0])(program[registers.point()][1])
    if registers.point() + 1 < len(program):
        registers.vals[registers.ip] += 1
    else:
        # breaking condition for the program
        break

print registers.vals
