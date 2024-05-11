from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.
        states = self.mdp.getStates()
        for i in range(self.iters):
            new_values = self.values.copy()
            for state in states:
                # drop terminal states
                if self.mdp.isTerminal(state):
                    continue
                action = self.getPolicy(state)
                q_value = self.getQValue(state, action)
                new_values[state] = q_value
            self.values = new_values

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)
    
    def getQValue(self, state, action):
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        sum = 0

        for next_state, prob in transitions:
            reward = self.mdp.getReward(state, action, next_state)
            # q-value formula
            sum += prob * (reward + (self.discountRate * self.getValue(next_state)))
        return sum
    
    def getAction(self, state):
        return self.getPolicy(state)
    
    def getPolicy(self, state):
        """
        Returns the best action according to computed values.
        """
        # drop terminal states
        if self.mdp.isTerminal(state):
            return None
        
        actions = self.mdp.getPossibleActions(state)
        action_values = {}

        for action in actions:
            action_values[action] = self.getQValue(state, action)

        best_action = max(action_values, key=action_values.get)

        return best_action
