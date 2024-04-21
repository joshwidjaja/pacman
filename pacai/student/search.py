"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.queue import Queue
from pacai.util.stack import Stack
from pacai.util.priorityQueue import PriorityQueue
from pacai.core.search.heuristic import euclidean

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    initial_node = (problem.startingState(), "Stop", 0)
    node = initial_node
    frontier = Stack()
    frontier.push(node)
    reached = {problem.startingState(): node}
    parents = {node: None}

    while not frontier.isEmpty():
        node = frontier.pop()
        state, action, cost = node
        if problem.isGoal(state):
            output = [action]
            current = node
            while parents[current] is not None:
                state, action, cost = current
                output.insert(0, action)
                current = parents[current]
            output.pop(-1)
            return output

        for child in problem.successorStates(state):
            s, a, c = child

            if s in reached:
                x, y, old_cost = reached[s]
            if s not in reached:
                reached[s] = child
                frontier.push(child)
                parents[child] = node
    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    initial_node = (problem.startingState(), "Stop", 0)
    node = initial_node
    frontier = Queue()
    frontier.push(node)
    reached = {problem.startingState(): node}
    parents = {node: None}

    while not frontier.isEmpty():
        node = frontier.pop()
        state, action, cost = node
        if problem.isGoal(state):
            output = [action]
            current = node
            while parents[current] is not None:
                state, action, cost = current
                output.insert(0, action)
                current = parents[current]
            output.pop(-1)
            return output

        for child in problem.successorStates(state):
            s, a, c = child

            if s in reached:
                x, y, old_cost = reached[s]
            if s not in reached or c < old_cost:
                reached[s] = child
                frontier.push(child)
                parents[child] = node
    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    initial_node = (problem.startingState(), "Stop", 0)
    node = initial_node
    frontier = PriorityQueue()
    frontier.push(node, 0)
    reached = {problem.startingState(): node}
    parents = {node: None}

    while not frontier.isEmpty():
        node = frontier.pop()
        state, action, cost = node
        if problem.isGoal(state):
            output = [action]
            current = node
            while parents[current] is not None:
                state, action, cost = current
                output.insert(0, action)
                current = parents[current]
            output.pop(-1)
            return output

        for child in problem.successorStates(state):
            s, a, c = child

            if s in reached:
                x, y, old_cost = reached[s]
            if s not in reached or c < old_cost:
                reached[s] = child
                frontier.push(child, c)
                parents[child] = node
    return None

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    if type(problem.startingState()[0]) is tuple:
        initial_cost = euclidean(problem.startingState()[0], problem)
    else:
        initial_cost = euclidean(problem.startingState(), problem)
    initial_node = (problem.startingState(), "Stop", initial_cost)
    node = initial_node
    frontier = PriorityQueue()
    frontier.push(node, initial_cost)
    reached = {problem.startingState(): node}
    parents = {node: None}

    while not frontier.isEmpty():
        node = frontier.pop()
        state, action, cost = node
        if problem.isGoal(state):
            output = [action]
            current = node
            while parents[current] is not None:
                state, action, cost = current
                output.insert(0, action)
                current = parents[current]
            output.pop(-1)
            return output

        for child in problem.successorStates(state):
            s, a, c = child

            if s in reached:
                x, y, old_cost = reached[s]
            if s not in reached or c < old_cost:
                reached[s] = child
                if type(s[0]) is tuple:
                    m = euclidean(s[0], problem)
                else:
                    m = euclidean(s, problem)
                frontier.push(child, c + m)
                parents[child] = node
    return None
