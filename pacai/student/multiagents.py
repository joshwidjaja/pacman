import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance
from pacai.core.directions import Directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        newPosition = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()

        if successorGameState.isWin():
            return float("inf")  # pursue win state

        # do NOT stop
        if action == Directions.STOP:
            return -float("inf")

        for ghost in successorGameState.getGhostPositions():
            # abandon route if ghost is too close
            if distance.manhattan(newPosition, ghost) < 2:
                return -float("inf")

        # uses closest distance to food and its reciprocal
        closestFoodDistance = float("inf")
        for food in newFood:
            foodDistance = distance.manhattan(newPosition, food)
            if foodDistance <= closestFoodDistance:
                closestFoodDistance = foodDistance

        foodDistanceScore = 1.0 / closestFoodDistance if closestFoodDistance > 0 else float("inf")
        return successorGameState.getScore() + foodDistanceScore

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        # final action from pacman max
        score, action = self.minimax(state, 0, self.getTreeDepth())
        return action

    def minimax(self, state, agent, depth):
        # return raw score at terminal state or max depth
        if depth == 0 or state.isLose() or state.isWin():
            return self.getEvaluationFunction()(state), Directions.STOP
        elif agent == 0:  # pacman
            return self.maxValue(state, depth)
        else:
            return self.minValue(state, agent, depth)

    # for pacman
    def maxValue(self, state, depth):
        actions = state.getLegalActions(0)
        max_score = -float("inf")
        max_action = Directions.STOP

        for action in actions:
            # Don't consider stopping in the search
            if action == Directions.STOP:
                continue
            successor = state.generateSuccessor(0, action)
            # gets minimax from next ghost
            action_score, new_action = self.minimax(successor, 1, depth)
            if action_score > max_score:
                max_score = action_score
                max_action = action
        return max_score, max_action

    # for ghosts
    def minValue(self, state, agent, depth):
        actions = state.getLegalActions(agent)
        min_score = float("inf")
        min_action = Directions.STOP

        # move back to pacman if at the last ghost
        if agent == state.getNumAgents() - 1:
            new_agent = 0
            new_depth = depth - 1
        else:
            new_agent = agent + 1
            new_depth = depth

        for action in actions:
            if action == Directions.STOP:
                continue
            successor = state.generateSuccessor(agent, action)
            # gets minimax from pacman/next ghost
            action_score, new_action = self.minimax(successor, new_agent, new_depth)
            if action_score < min_score:
                min_score = action_score
                min_action = action
        return min_score, min_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        alpha = -float("inf")
        beta = float("inf")
        score, action = self.alphaBeta(state, 0, self.getTreeDepth(), alpha, beta)
        return action
    
    def alphaBeta(self, state, agent, depth, alpha, beta):
        if depth == 0 or state.isLose() or state.isWin():
            return self.getEvaluationFunction()(state), Directions.STOP
        elif agent == 0:
            return self.alphaValue(state, depth, alpha, beta)
        else:
            return self.betaValue(state, agent, depth, alpha, beta)
        
    def alphaValue(self, state, depth, alpha, beta):
        actions = state.getLegalActions(0)
        max_score = -float("inf")
        max_action = Directions.STOP

        for action in actions:
            # Don't consider stopping in the search
            if action == Directions.STOP:
                continue
            successor = state.generateSuccessor(0, action)
            action_score, new_action = self.alphaBeta(successor, 1, depth, alpha, beta)
            if action_score > max_score:
                max_score = action_score
                max_action = action

            # prune if max exceeds beta
            if max_score > beta:
                return max_score, max_action

            # update alpha
            if max_score > alpha:
                alpha = max_score

        return max_score, max_action

    def betaValue(self, state, agent, depth, alpha, beta):
        actions = state.getLegalActions(agent)
        min_score = float("inf")
        min_action = Directions.STOP

        # move back to pacman if at the last ghost
        if agent == state.getNumAgents() - 1:
            new_agent = 0
            new_depth = depth - 1
        else:
            new_agent = agent + 1
            new_depth = depth

        for action in actions:
            if action == Directions.STOP:
                continue
            successor = state.generateSuccessor(agent, action)
            action_score, new_action = self.alphaBeta(successor, new_agent, new_depth, alpha, beta)
            if action_score < min_score:
                min_score = action_score
                min_action = action

            # prune if min is below alpha
            if min_score < alpha:
                return min_score, min_action
            
            # update beta
            if min_score < beta:
                beta = min_score
        return min_score, min_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        score, action = self.expectimax(state, 0, self.getTreeDepth())
        return action
    
    def expectimax(self, state, agent, depth):
        if depth == 0 or state.isLose() or state.isWin():
            return self.getEvaluationFunction()(state), Directions.STOP
        elif agent == 0:
            return self.maxValue(state, depth)
        else:
            return self.expectedValue(state, agent, depth)
        
    def maxValue(self, state, depth):
        actions = state.getLegalActions(0)
        max_score = -float("inf")
        max_action = Directions.STOP

        for action in actions:
            # Don't consider stopping in the search
            if action == Directions.STOP:
                continue
            successor = state.generateSuccessor(0, action)
            action_score, new_action = self.expectimax(successor, 1, depth)
            if action_score > max_score:
                max_score = action_score
                max_action = action
        return max_score, max_action

    def expectedValue(self, state, agent, depth):
        actions = state.getLegalActions(agent)
        expected_score = 0
        expected_action = Directions.STOP
        probability = 1.0 / len(actions)

        if agent == state.getNumAgents() - 1:
            new_agent = 0
            new_depth = depth - 1
        else:
            new_agent = agent + 1
            new_depth = depth

        for action in actions:
            if action == Directions.STOP:
                continue

            successor = state.generateSuccessor(agent, action)
            action_score, new_action = self.expectimax(successor, new_agent, new_depth)

            expected_score += probability * action_score
        return expected_score, expected_action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    # Don't lose, simple as
    if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return -float("inf")
    
    score = currentGameState.getScore()
    
    pos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()

    # avoid ghosts (only if they aren't scared)
    brave_ghosts = []
    for ghost in ghosts:
        if ghost.getScaredTimer() <= 0:
            brave_ghosts.append(ghost)

    for ghost in brave_ghosts:
        # abandon route if ghost is too close
        if distance.manhattan(pos, ghost.getPosition()) < 2:
            return -float("inf")
    # get food
    food_list = currentGameState.getFood().asList()
    food_left = len(food_list)

    food_distances = []
    for food in food_list:
        food_distances.append(distance.manhattan(pos, food))

    closest_food_distance = min(food_distances)
    # get capsules
    capsules_left = len(currentGameState.getCapsules())
    output = score - (2 * closest_food_distance) - (4 * food_left) - (16 * capsules_left)
    return output

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
