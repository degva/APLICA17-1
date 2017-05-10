# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

from collections import deque
class FIFOQueue(deque):
    def pop(self):
        return self.popleft()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def graphSearch(problem, frontier):

    initial = problem.getStartState()
    actions = []
    explored = []

    frontier.append((initial, actions))
    while frontier:
        node, actions = frontier.pop()
        explored.append(node)
        successors = problem.getSuccessors(node)
        for succ in successors:
            coordinate, direction, cost = succ
            newActions = actions + [direction]
            res_list = [x for x,_ in frontier]
            if (coordinate not in explored) and (coordinate not in res_list):
                if problem.isGoalState(coordinate):
                    return newActions
                frontier.append((coordinate, newActions))

    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return graphSearch(problem, [])

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return graphSearch(problem, FIFOQueue())

def invertMeme(memelist):
    """ This is a hardcoded meme """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    rmeme = []
    for i in memelist:
        if i == s:
            rmeme.append(n)
        elif i == w:
            rmeme.append(e)
        elif i == e:    
            rmeme.append(w)
        elif i == n:
            rmeme.append(s)
    return rmeme    


def biSearch(problem, QI, QG):
    initial = problem.getStartState()
    goal = problem.goal
    
    explored1 = []
    explored2 = []

    frontier1 = QI
    frontier2 = QG
    frontier1.append((initial,[]))
    frontier2.append((goal,[]))
    if(initial == goal):
            return []

    while True:
        node1,dir1 = frontier1.pop()
        explored1.append(node1)
        if (node1 in frontier2):
            for node, dir2 in frontier2:
                if (node1 == node):
                    ans = invertMeme(dir2)
                    ans.reverse()
                    return dir1 + ans
            
        successors = problem.getSuccessors(node1)
        for succ in successors:
            coordinate, direction, cost = succ
            newActions = dir1 + [direction]
            res_list = [x for x,_ in frontier1]
            if(coordinate not in frontier1) and (coordinate not in explored1):
                frontier1.append((coordinate,newActions))
        
        node2,dir2 = frontier2.pop()
        explored2.append(node2)
        if (node2 in frontier1):
            for node, dir1 in frontier1:
                if (node2 == node):
                    ans = invertMeme(dir2)
                    ans.reverse()
                    return  dir1 + ans


        successors = problem.getSuccessors(node2)
        for succ in successors:
            coordinate, direction, cost = succ
            newActions = dir2 + [direction]
            res_list = [x for x,_ in frontier2]
            if(coordinate not in frontier2) and (coordinate not in explored2):
                frontier2.append((coordinate,newActions))

        for cord1, dir1 in frontier1:
            for cord2, dir2 in frontier2:
                if(cord1 == cord2):
                    ans = invertMeme(dir2)
                    ans.reverse()
                    return  dir1 + ans

def bidirectionalSearch(problem):
    return biSearch(problem, FIFOQueue(), FIFOQueue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def aStarSearch(problem, heuristic=manhattanHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    closedset = []
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push( (start, []), heuristic(start, problem))

    while not frontier.isEmpty():
        node, actions = frontier.pop()

        if problem.isGoalState(node):
            return actions

        closedset.append(node)

        for coord, direction, cost in problem.getSuccessors(node):
            if not coord in closedset:
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                frontier.push( (coord, new_actions), score )

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
bir = bidirectionalSearch
