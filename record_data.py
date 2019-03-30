import create_wav
import sys

name = str(sys.argv[1])

samples = 4

recordings = []

for j in range(samples):

    recordings.append(str(name + str(j)))

for i in recordings:
    print(type(i))
    create_wav.recordFile(i)