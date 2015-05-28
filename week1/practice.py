import pylab
import numpy as np

# pylab.figure(1)
# pylab.plot([1,2,3,4],[3,5,2,7])
# pylab.show()

def parse_temps(filename):
  inFile = open(filename)
  mins = []
  maxs = []
  for line in inFile:
    fields = line.split(' ')
    if len(fields) < 3 or not fields[0].isdigit():
      continue
    else:
      mins.append(int(fields[2]))
      maxs.append(int(fields[1]))
  return (mins, maxs)



def plot_diff(lowtemps, hightemps):
  difftemps = []
  # index = 0
  # for temp in hightemps:
  #   difftemps.append(temp - lowtemps[index])
  #   index +=1
  difftemps = list(np.array(hightemps) - np.array(lowtemps))
  pylab.figure(1)
  pylab.plot(difftemps)
  pylab.show()

# mins, maxs = parse_temps('temps.txt')
# plot_diff(mins, maxs)

import random

# for i in range(100):
#   print i
#   print random.randrange(0,100,2)


# mylist = []

# for i in xrange(random.randint(1, 10)):
#     random.seed(0)
#     if random.randint(1, 10) > 3:
#         number = random.randint(1, 10)
#         mylist.append(number)
# print mylist

import string

def loadWords2():
  try:
    inFile = open("mywords.txt", 'r', 0)
  except IOError as e:
    print "The wordlist doesn't exist; using some fruits for now"
    return ['apple', 'orange', 'pear', 'lime', 'lemon', 'grape', 'pineapple']
  line = inFile.readline()
  wordlist = string.split(line,",")
  print "  ", len(wordlist), "words loaded."
  return wordlist


mylist = loadWords2()
print mylist




