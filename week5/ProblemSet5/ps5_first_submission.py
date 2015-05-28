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

    def __str__(self):
        return str(self.nodes)

def DFSShortest(graph, start, end, path = [], shortest = None):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    print 'Current dfs path:', printPath(path)
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            if shortest == None or len(path)<len(shortest):
                newPath = DFSShortest(graph,node,end,path,shortest)
                if newPath != None:
                    shortest = newPath
    return shortest

def originalDFS(graph, start, end, maxTotalDist, maxDistOutdoors, path, shortest = None):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    if start == end:
        return path
    else:
        for edge in graph.edgesFrom(start):
            current_path = copy.deepcopy(path)
            if edge.getDestination() not in current_path.getNodes(): #avoid cycles
                if edge.getOutdoorDistance() <= maxDistOutdoors - current_path.getOutdoorDistance():
                    if edge.getTotalDistance() <= maxTotalDist - current_path.getTotalDistance():
                        if shortest == None or edge.getTotalDistance() + current_path.getTotalDistance() < shortest.getTotalDistance():
                            current_path.addEdge(edge)
                            new_path = originalDFS(graph,edge.getDestination(), end, maxTotalDist, maxDistOutdoors, current_path, shortest)
                            if new_path != None:
                                shortest = new_path
    return shortest

def bruteDFS(graph, start, end, path, possiblePaths):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    if start == end:
        possiblePaths.append(path)
        return
    else:
        for edge in graph.edgesFrom(start):
            print "looking at :",edge
            current_path = copy.deepcopy(path)
            if edge.getDestination() not in current_path.getNodes(): #avoid cycles
                current_path.addEdge(edge)
                bruteDFS(graph,edge.getDestination(), end, current_path, possiblePaths)

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
    possiblePaths = []
    print "in brute"
    bruteDFS(digraph,Node(start),Node(end),Path(Node(start)),possiblePaths)
    possiblePaths = [path for path in possiblePaths if path.getTotalDistance()<= maxTotalDist and path.getOutdoorDistance() <= maxDistOutdoors]
    if len(possiblePaths) < 1:
        raise ValueError
    else:
        shortest = None
        for path in possiblePaths:
            if shortest == None or path.getTotalDistance() < shortest.getTotalDistance():
                shortest = path
    return [str(node) for node in shortest.getNodes()]



#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    min_path = originalDFS(digraph, Node(start),Node(end),maxTotalDist, maxDistOutdoors,Path(Node(start)))
    # if min_path == None:
    #     raise ValueError
    # else:
    #     return [str(node) for node in min_path.getNodes()]
    
my_map = load_map("map2.txt")
print directedDFS(my_map,"1","3",18,18)
print "expected [1,4,3]"
print directedDFS(my_map,"1","3",15,0)
print "expected ValueError"

# # Uncomment below when ready to test
# #### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     # Test cases
#     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     # print 'nodes', mitMap.nodes
#     # print 'edges', mitMap.edges
#     print mitMap


#     LARGE_DIST = 1000000

#     # Test case 1
#     print "---------------"
#     print "Test case 1:"
#     print "Find the shortest-path from Building 32 to 56"
#     expectedPath1 = ['32', '56']
#     brutePath1 = bruteForceSearch(mitMap, '32', '56', 100, 100) #LARGE_DIST, LARGE_DIST)
#     print "done with brute and got: ",brutePath1
#     dfsPath1 = directedDFS(mitMap, '32', '56', 100, 100) #LARGE_DIST, LARGE_DIST)
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
