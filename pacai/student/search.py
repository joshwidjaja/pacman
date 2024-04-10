"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

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
    frontier = [node]
    reached = {problem.startingState(): node}
    parents = {node: None}

    while len(frontier) != 0:
        node = frontier.pop(0)
        state, action, cost = node
        if problem.isGoal(state):
            output = [action]
            current = node
            while parents[current] is not None:
                state, action, cost = current
                output.insert(0, action)
                current = parents[current]
            return output

        for child in problem.successorStates(state):
            s, a, c = child

            if s in reached:
                x, y, old_cost = reached[s]
            if s not in reached or c < old_cost:
                reached[s] = child
                frontier.append(child)
                parents[child] = node
    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    initial_node = (problem.startingState(), "Stop", 0)
    node = initial_node
    frontier = [node]
    reached = {problem.startingState(): node}
    parents = {node: None}

    while len(frontier) != 0:
        node = frontier.pop(-1)
        state, action, cost = node
        if problem.isGoal(state):
            output = [action]
            current = node
            while parents[current] is not None:
                state, action, cost = current
                output.insert(0, action)
                current = parents[current]
            return output

        for child in problem.successorStates(state):
            s, a, c = child

            if s in reached:
                x, y, old_cost = reached[s]
            if s not in reached or c < old_cost:
                reached[s] = child
                frontier.append(child)
                parents[child] = node
    return None

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
