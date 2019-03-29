import create_wav
import sys

print(sys.argv)
print(str(sys.argv[1]))
name = str(sys.argv[1])
# name = args[1]


# print(sys.argv)
# name = 'colin'

samples = 4

recordings = []


# create_wav.recordFile('hello')

# name = 'colin'

for j in range(samples):

    recordings.append(str(name + str(j)))


for i in recordings:
    print(type(i))
    create_wav.recordFile(i)