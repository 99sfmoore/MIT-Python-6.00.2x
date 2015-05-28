import random
import pylab

def generateScores(numTrials):
  scores = []
  for i in range(numTrials):
    test1 = random.randint(50,80)
    test2 = random.randint(60,90)
    test3 = random.randint(55,95)
    score = test1*0.25 + test2*0.25 + test3*0.5
    scores.append(score)
  return scores

def plotQuizzes():
  scores = generateScores(10000)
  pylab.hist(scores, bins=7)
  pylab.xlabel("Final Score")
  pylab.ylabel("Number of Trials")
  pylab.title("Distribution of Scores")
  pylab.show()

def probTest(limit):
    prob = 1.0
    num_rolls = 0
    while prob >= limit:
      num_rolls +=1
      prob = ((5.0/6.0)**(num_rolls-1))*(1.0/6.0)
    return num_rolls  


probTest(1.0/100.0)