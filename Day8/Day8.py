with open("input.txt", "r") as f:
    test_input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    data = [int(n) for n in f.read().split(" ")]


class Node(object):

    def __init__(self, no_subnodes, no_metadata):

        # number of nodes and metadata
        # the nodes and metadata will be added externally
        self.no_subnodes = no_subnodes
        self.no_metadata = no_metadata

        self.subnodes = []
        self.metadata = []

    def total_metadata(self):
        # finding the sum of the metadata
        return sum(self.metadata) + sum([subnode.total_metadata() for subnode in self.subnodes])

    def value(self):
        # algorithm for the value of a node as described in the exercise
        if self.no_subnodes == 0:
            return sum(self.metadata)

        val = 0
        for i in self.metadata:
            if i <= self.no_subnodes:
                val += self.subnodes[i - 1].value()
        return val

    def __str__(self):
        # representation for checking if the tree is correct
        res = str(self.metadata) + "\n"
        for subnode in self.subnodes:
            for line in str(subnode).split("\n"):
                res += "    " + line + "\n"

        # removing the last newline character
        return res[:-1]

    def __repr__(self):
        return self.__str__()


def build_tree(dat):

    # the root node that will be returned
    root = Node(dat[0], dat[1])
    dat = dat[2:]

    for i in xrange(root.no_subnodes):
        # add subnodes and make data shorter
        subnode, dat = build_tree(dat)
        root.subnodes.append(subnode)

    for j in xrange(root.no_metadata):
        # add metadata
        root.metadata.append(dat[j])

    # return the root node and the leftover data
    return root, dat[root.no_metadata:]


tree, data_left = build_tree(data)
"""If there is data left, something went wrong"""
assert not data_left

# report
print str(tree)
print tree.total_metadata()
print tree.value()
