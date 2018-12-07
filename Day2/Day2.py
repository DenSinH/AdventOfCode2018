with open("input.txt", "r") as f:
    lines = list(f.readlines())

two_letters = []
three_letters = []

two_unique = []
three_unique = []

for line in lines:
    let_count = {}
    for letter in line:
        if letter in let_count:
            let_count[letter] += 1
        else:
            let_count[letter] = 1

    if 2 in let_count.values():
        two_letters.append(line.strip("\n"))
        two_unique.append(line.strip("\n"))
    elif 3 in let_count.values():
        three_unique.append(line.strip("\n"))

    if 3 in let_count.values():
        three_letters.append(line.strip("\n"))

print two_letters
print three_letters

print len(two_letters)*len(three_letters)

unique = two_unique + three_unique

for i in range(len(unique)):
    for j in range(i, len(unique)):
        if [unique[i][l] == unique[j][l] for l in range(len(unique[0]))].count(False) == 1:
            print unique[i], unique[j]
            print "".join([unique[i][l] if unique[i][l] == unique[j][l] else "" for l in range(len(unique[0]))])

