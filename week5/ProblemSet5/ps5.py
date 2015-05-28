# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
import copy
# This imports everything from `graph.py` as if it was defined in this file!
from better_graph import * 
import pdb
#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print "Loading map from file..."
    g = WeightedDigraph()
    f = open(mapFilename)
    for line in f:
        n1, n2, total, outdoor = [int(x) for x in line.split()]
        node1 = Node(n1)
        node2 = Node(n2)
        try:
            g.addNode(node1)
        except (ValueError):
            pass
        try:
            g.addNode(node2)
        except (ValueError):
            pass
        g.addEdge(WeightedEdge(node1,node2,total,outdoor))
    return g



#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#
class Path(object):
    def __init__(self,start):
        self.nodes = [start]
        self.outdoorDistance = 0
        self.totalDistance = 0

    def getNodes(self):
        return self.nodes

    def getOutdoorDistance(self):
        return self.outdoorDistance

    def getTotalDistance(self):
        return self.totalDistance

    def addEdge(self,edge):
        self.nodes.append(edge.getDestination())
        self.outdoorDistance += edge.getOutdoorDistance()
        self.totalDistance += edge.getTotalDistance()
        print "added Edge"
        print self.nodes

    def __str__(self):
        return str(self.nodes)

def DFS(graph, start, end, maxTotalDist, maxDistOutdoors, path, meets_criteria = []):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    print "This is meets_criteria"
    print meets_criteria
    print "start is",start
    print "end is",end
    print "maxTotalDist is ",maxTotalDist
    print "maxDistOutdoors is ",maxDistOutdoors
    if start == end:
        print path.getNodes()
        meets_criteria.append(path)
        print "adding a path"
        print "current size of meets_criteria is ",len(meets_criteria)
    else:
        print "from node ",start," I'm going to look at ", graph.edgesFrom(start)
        print "at top of for edge in graph loop, path is ",path.getNodes()
        print "locking that as current_path"
        # current_path = copy.deepcopy(path)
        for edge in graph.edgesFrom(start):
            print "edge is ",edge
            print "setting path to older current_path"
            current_path = copy.deepcopy(path)
            print "current path is ",current_path.getNodes()
            print "copying path"
            if edge.getDestination() not in current_path.getNodes(): #avoid cycles
                print "dest is not in path"
                if edge.getOutdoorDistance() <= maxDistOutdoors - current_path.getOutdoorDistance():
                    print "outdoor distance okay"
                    if edge.getTotalDistance() <= maxTotalDist - current_path.getTotalDistance():
                        print "total distance okay"
                        print "path was ",current_path.getNodes()
                        current_path.addEdge(edge)
                        print "adding edge"
                        print "path is ",current_path.getNodes()
                        meets_criteria += DFS(graph,edge.getDestination(), end, maxTotalDist, maxDistOutdoors, current_path, meets_criteria)
    # pdb.set_trace()
    print "from start node of ",start," meets_criteria is ",meets_criteria," and I'm returning"
    return meets_criteria

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    possiblePaths = DFS(digraph,Node(start),Node(end),maxTotalDist,maxDistOutdoors,Path(Node(start)))
    print "number of paths is: ",len(possiblePaths)
    for path in possiblePaths:
        print path
    if len(possiblePaths) < 1:
        raise ValueError
    else:
        shortest = None
        for path in possiblePaths:
            if shortest == None or path.getTotalDistance() < shortest.getTotalDistance():
                shortest = path
    return [str(node) for node in shortest.getNodes()]

my_graph = load_map("mit_map.txt")
print isinstance(my_graph, Digraph)   
print isinstance(my_graph, WeightedDigraph)
print bruteForceSearch(my_graph,57,76,120,60)


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     Test cases
#     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     print 'nodes', mitMap.nodes
#     print 'edges', mitMap.edges


#     LARGE_DIST = 1000000

#     Test case 1
#     print "---------------"
#     print "Test case 1:"
#     print "Find the shortest-path from Building 32 to 56"
#     expectedPath1 = ['32', '56']
#     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath1
#     print "Brute-force: ", brutePath1
#     print "DFS: ", dfsPath1
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
#     print "---------------"
#     print "Test case 2:"
#     print "Find the shortest-path from Building 32 to 56 without going outdoors"
#     expectedPath2 = ['32', '36', '26', '16', '56']
#     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
#     print "Expected: ", expectedPath2
#     print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr
