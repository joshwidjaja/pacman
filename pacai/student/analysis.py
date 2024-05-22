"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    Reduced noise to prevent excessive deviation
    """

    answerDiscount = 0.9
    answerNoise = 0.01

    return answerDiscount, answerNoise

def question3a():
    """
    low living reward encourages an early exit
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = -4.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    reducing the discount makes taking a longer route also favorable
    """

    answerDiscount = 0.2
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    living reward is harsher than 3d, but less harsh than 3a
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    No changes necessary, path preferred by default
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    made the reward positive to disincentivize the actual goals
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 10

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    """

    # answerEpsilon = 0.3
    # answerLearningRate = 0.5

    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
