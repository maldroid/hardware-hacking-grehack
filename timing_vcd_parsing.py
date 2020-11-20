from __future__ import print_function
import sys

f = open(sys.argv[1])
last = False
timestamp = 0
timestamps = {}
byte = 0

for line in f:
    if line[0] == '$':                               # skip the preamble
        continue
    elif line[0] == '#':                             # it's a timestamp
        prev_timestamp = timestamp
        timestamp = int(line[1:])
    elif line[0] == '0' and line[1] == '"' and last: # it's the character we're interested in
        if (timestamp - prev_timestamp) > 100000:    # skip if the time difference is too high
            print('Skipping...')
            last = False
            continue
        timestamps.setdefault(byte, []).append(timestamp - prev_timestamp)  # keep the differences in a per byte dictionary
        if len(timestamps[byte]) == 100:                                    # change the current byte if it has been tested 100 times
            byte += 1
        last = False
    elif line[0] == '1' and line[1] == '!':          # we will be interested in the next character
            last = True

for byte in timestamps:                              # calculate the time difference average
    timestamps[byte] = 1.0 * sum(timestamps[byte]) / len(timestamps[byte])

ordered_keys = sorted(timestamps, key = timestamps.get)   # print the sorted data
for byte in ordered_keys:
    print("{} {} {}".format(timestamps[byte], byte, chr(byte)))

