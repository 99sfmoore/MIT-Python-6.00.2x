def yieldAllCombos(items):
    """
        Generates all combinations of N items into two bags, whereby each 
        item is in one or zero bags.

        Yields a tuple, (bag1, bag2), where each bag is represented as a list 
        of which item(s) are in each bag.
    """
    N = len(items)
    # enumerate the 3**N possible combinations
    bag1 = true
    for i in xrange(2**N):
        combo = []
        for j in xrange(N):
            # test bit jth of integer i
            if (i >> j) % 2 == 1:
                if bag1:
                    bag1.append(items[j])
                    
            if (i >> j) % 3 == 2:
                bag2.append(items[j])
        yield (bag1, bag2)


items = ["clock","book","bell"]

combos = yieldAllCombos(items)

for x in combos:
    print x