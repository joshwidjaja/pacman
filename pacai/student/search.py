"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.queue import Queue
from pacai.util.stack import Stack
from pacai.util.priorityQueue import PriorityQueue

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
    node_queue = Stack()
    start_node = problem.startingState()
    visited = [start_node]
    node_queue.push((start_node, []))

    while not node_queue.isEmpty():
        current_node, path = node_queue.pop()

        if problem.isGoal(current_node):
            return path
        
        for child in problem.successorStates(current_node):
            successor, action, cost = child

            if successor not in visited:
                visited.append(successor)
                node_queue.push((successor, path + [action]))

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    node_queue = Queue()
    start_node = problem.startingState()
    visited = [start_node]
    node_queue.push((start_node, []))

    while not node_queue.isEmpty():
        current_node, path = node_queue.pop()

        if problem.isGoal(current_node):
            return path
        
        for child in problem.successorStates(current_node):
            successor, action, cost = child

            if successor not in visited:
                visited.append(successor)
                node_queue.push((successor, path + [action]))
    
    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    node_queue = PriorityQueue()
    start_node = problem.startingState()
    visited = [start_node]
    node_queue.push((start_node, []), 0)

    while not node_queue.isEmpty():
        current_node, path = node_queue.pop()

        if problem.isGoal(current_node):
            return path
        
        for child in problem.successorStates(current_node):
            successor, action, cost = child

            if successor not in visited:
                visited.append(successor)
                new_cost = problem.actionsCost(path + [action])
                node_queue.push((successor, path + [action]), new_cost)
    
    return []

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    # Assistance from Tutor Chloe Wong
    node_queue = PriorityQueue()
    start_node = problem.startingState()
    visited = [start_node]
    node_queue.push((start_node, []), 0)

    while not node_queue.isEmpty():
        current_node, path = node_queue.pop()

        if problem.isGoal(current_node):
            return path
        
        for child in problem.successorStates(current_node):
            successor, action, cost = child

            if successor not in visited:
                visited.append(successor)
                new_cost = problem.actionsCost(path + [action]) + heuristic(successor, problem)
                node_queue.push((successor, path + [action]), new_cost)

    return []