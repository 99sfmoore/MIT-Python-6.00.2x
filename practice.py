import random 

def trial():
    balls = ["r","r","r","g","g","g"]
    firstBall = None
    for j in range(3):
        i = random.randrange(len(balls))
        firstBall = firstBall or balls[i]
        if balls.pop(i) != firstBall:
            return False
    return True

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    count = 0
    for i in range(numTrials):
        if trial():
            count += 1
    return float(count)/numTrials
        
                
                

