import numpy as np

with open("input.txt", "r") as f:

    lines = sorted(list(f.readlines()))

sleep_times = {}
id_ = ""
sleep_start = 0

for line in lines:

    if "Guard" in line:
        sleep_start = 0

        id_ = line.split(" ")[3]
        if id_ not in sleep_times:
            sleep_times[id_] = np.zeros(60)

    elif "falls" in line:
        sleep_start = int(line.split(":")[1][:2])
    elif "wakes" in line:
        sleep_end = int(line.split(":")[1][:2])

        sleep_times[id_][sleep_start:sleep_end] += np.ones(sleep_end - sleep_start)

most_asleep = sorted(sleep_times.keys(), key=lambda id_: np.sum(sleep_times[id_]))[-1]
print most_asleep, sleep_times[most_asleep], sleep_times[most_asleep].argmax()

most_frequent_minute = sorted(sleep_times.keys(), key=lambda id_: sleep_times[id_].max())[-1]
print most_frequent_minute, sleep_times[most_frequent_minute], sleep_times[most_frequent_minute].argmax()
