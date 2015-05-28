my_collection = []

def my_function(x, prev_x):
  if x == 1:
    print "about to return the list"
    return prev_x
  else:
    print "nope,",x," != 1",(x)
    prev_x.append(x)
    my_function(x-1,prev_x)

my_function(5,my_collection)
print my_collection
