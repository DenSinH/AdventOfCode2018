inp = 880751
inp_lst = [int(d) for d in str(inp)]  # input converted to a list

# initial values
scores = [3, 7]
elve1 = 0
elve2 = 1

# looking if we need to do part 2 still
part_2 = True

while len(scores) < inp + 10 or part_2:  # keep going until both part 1 and 2 finish

    # it is kind of random when it will or will not print, as the length sometimes increases by 2
    if not len(scores) % 100000:
        print len(scores) / 1000000., "Million recipies"

    # algorithm for finding the new recipies and current recipies
    new_score = scores[elve1] + scores[elve2]
    if new_score >= 10:
        scores.append(new_score // 10)

    scores.append(new_score % 10)

    elve1 = (elve1 + scores[elve1] + 1) % len(scores)
    elve2 = (elve2 + scores[elve2] + 1) % len(scores)

    # if we need to do part 2 still and it is possible that the input string was found, we check for it
    if part_2 and len(scores) > len(inp_lst):
        # we only need to check the last len(inp_lst) (or 1 before), as all of the possible places before that
        # we have checked before, and we might have added 2 recipies, so we do need to check these 2
        if scores[-len(inp_lst) - 1:-1] == inp_lst:
            # in this case, we need to report 1 recipe less (which is weird to me, as both of them were made at the
            # same time...)
            print "PART 2:", len(scores) - len(inp_lst) - 1
            part_2 = False
        elif scores[-len(inp_lst):] == inp_lst:
            print "PART 2:", len(scores) - len(inp_lst)
            part_2 = False

# report part 1 too
print "PART 1:", scores[inp:inp + 10]
