def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """
    if not L:
        return float('NaN')
    sum = 0
    for str in L:
       sum += len(str)
    mean = float(sum) / len(L)
    sum_of_var = 0
    for str in L:
        sum_of_var += (len(str) - mean)**2
    variance = sum_of_var/len(L)
    return variance**0.5

# using list comprehensions
def stdDevOfLengths2(L):
    n = float(len(L))
    if (n == 0):
        return float('NaN')
    lengths    = [len(s) for s in L]
    mean       = sum(lengths) / n
    squaredDev = [(l-mean)**2 for l in lengths]
    variance   = sum(squaredDev) / n    
    return variance**(.5)

def coeffofVariation(L):
    n = float(len(L))
    if (n == 0):
        return float('NaN')
    # lengths    = [len(s) for s in L]
    mean       = sum(L) / n
    squaredDev = [(el-mean)**2 for el in L]
    variance   = sum(squaredDev) / n    
    stdDev =  variance**(.5)
    return stdDev / mean


# print stdDevOfLengths(['a', 'z', 'p'])
# print stdDevOfLengths(['apples', 'oranges', 'kiwis', 'pineapples'])
# print coeffofVariation([10, 4, 12, 15, 20, 5])
# string = "hello iou"
# vowels = ['a','e','i','o','u']
# print sum(string.count(c) for c in vowels)
# tiles = [[[False] for h in range(3)] for w in range(5)]
# print tiles
# tiles[2][1] = True
# tiles[0][1] = True
# tiles[4][0] = True
# print tiles
print float(99)/100
print float(20)/100