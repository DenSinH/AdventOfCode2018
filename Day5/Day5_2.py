import numpy as np

# get input
with open("input.txt", "r") as f:
    polymer = f.readline().strip("\n")

# alphabet to digitize the polymer
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
cut_lengths = {}


for letter in xrange(26):
    # digitized polymer
    d_polymer = np.array([alphabet.index(l) for l in polymer])

    # strip of letter and capital letter
    d_polymer = d_polymer[d_polymer != letter]
    d_polymer = d_polymer[d_polymer != letter + 26]

    # initial cutting array
    cut = np.array([True])

    while np.any(cut):

        # as long as we cut, we need to try to cut again
        # check if the digit on the right is "inverted" of the one on a position
        right_inverted = np.abs(np.roll(d_polymer, -1) - d_polymer) == 26
        # the one on the last position can never be inverted of the digit to the right of it (there is none)
        right_inverted[-1] = False

        # inverted on the left is inverted on the right rolled over by one
        left_inverted = np.roll(right_inverted, 1)
        # the digit in the first place can never be inverted of the one to the left of it (there is none)
        left_inverted[0] = False

        # problems occur with triplets, so we need to check for those
        # check for equality two to the left
        left2_equals = np.roll(d_polymer, 2) == d_polymer
        # same reasoning as before
        left2_equals[:2] = np.array([False, False])

        # cut if:
        #    left is equal or right is inverted
        #    BUT: not if the left is inverted, and two to the left is equal (preference for cutting on the left side of
        #                                                                    triplets)
        cut = np.logical_and(np.logical_or(right_inverted, left_inverted), np.logical_not(np.logical_and(left2_equals, left_inverted)))

        d_polymer = d_polymer[np.logical_not(cut)]

    cut_lengths[alphabet[letter]] = d_polymer.size

    # report
    print "".join([alphabet[i] for i in d_polymer])
    print alphabet[letter], d_polymer.size


for letter in xrange(26):
    print alphabet[letter], cut_lengths[alphabet[letter]]
