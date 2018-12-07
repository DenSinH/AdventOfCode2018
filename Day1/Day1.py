frequency = 0

with open("input.txt", "r") as f:
    lines = list(f.readlines())

for l in lines:
    line = l.strip("\n")
    frequency += int(line)

print frequency

frequency = 0
seen_frequencies = {}
i = 0

while True:
    line = lines[i].strip("\n")
    frequency += int(line)
    if frequency in seen_frequencies:
        break
    seen_frequencies[frequency] = 1.

    i = (i + 1) % len(lines)

print frequency
