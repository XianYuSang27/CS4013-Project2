# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Get the current score
        score = successorGameState.getScore()

        # Calculate the distance to the nearest food using Manhattan distance
        foodList = newFood.asList()
        if len(foodList) > 0:
            foodDistance = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            # If there's no food left, give a high score
            return float("inf")

        # Calculate the distance to the nearest scared ghost using Manhattan distance
        scaredGhosts = [ghostState for ghostState, scaredTime in zip(newGhostStates, newScaredTimes) if scaredTime > 0]
        if scaredGhosts:
            scaredGhostDistance = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in scaredGhosts])
        else:
            # If no ghost is scared, consider the closest ghost
            scaredGhostDistance = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        # Calculate the score based on the distance to food and distance to scared ghost
        score += 20 / (foodDistance + 1) - 5 / (scaredGhostDistance + 1)

        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        #Gets action for max agent
        def max_value(state, depth):
            #Check if terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None
            v = float("-inf")
            best_action = None
            #Finds best action for max agent
            for action in state.getLegalActions(self.index):
                #Gets successor for action
                successor = state.generateSuccessor(self.index, action)
                #Gets score for next depth (min agent)
                score, _ = min_value(successor, depth, 1)
                #Determines best action depending on score
                if score > v:
                    v = score
                    best_action = action
            return v, best_action

        #Gets action for min agent
        def min_value(state, depth, agent_index):
            #Check if terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None
            v = float("inf")
            best_action = None
            #Finds best action for min agent
            for action in state.getLegalActions(agent_index):
                #Gets successor for action
                successor = state.generateSuccessor(agent_index, action)
                #Gets score of successor
                if agent_index == state.getNumAgents() - 1:
                    #If last min agent, get score for max agent
                    score, _ = max_value(successor, depth + 1)
                else:
                    #Gets score for next depth (min agent)
                    score, _ = min_value(successor, depth, agent_index + 1)
                #Determines best action depending on score
                if score < v:
                    v = score
                    best_action = action
            return v, best_action
        
        #Returns best actions for agents
        _, best_action = max_value(gameState, 0)
        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def max_value(state, depth, alpha, beta):
            #Check if terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None
            v = float("-inf")
            best_action = None
            #Finds best action for max agent
            for action in state.getLegalActions(self.index):
                #Gets successor for action
                successor = state.generateSuccessor(self.index, action)
                #Gets score for next depth (min agent)
                score, _ = min_value(successor, depth, 1, alpha, beta)
                #Determines best action depending on score
                if score > v:
                    v = score
                    best_action = action
                #Stops search if current value is greater than beta
                if v > beta:
                    return v, best_action
                #Updates 
                alpha = max(alpha, v)
            return v, best_action
            
        def min_value(state, depth, agent_index, alpha, beta):
            #Check if terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None
            v = float("inf")
            best_action = None
            #Finds best action for min agent
            for action in state.getLegalActions(agent_index):
                #Gets successor for action
                successor = state.generateSuccessor(agent_index, action)
                #Gets score of successor
                if agent_index == state.getNumAgents() - 1:
                    #If last min agent, get score for max agent
                    score, _ = max_value(successor, depth + 1, alpha, beta)
                else:
                    #Gets score for next depth (min agent)
                    score, _ = min_value(successor, depth, agent_index + 1, alpha, beta)
                #Determines best action depending on score
                if score < v:
                    v = score
                    best_action = action
                #Stops search if current value is less than alpha
                if v < alpha:
                    return v, best_action
                beta = min(beta, v)    
            return v, best_action
        
        #Returns actions
        _, best_action = max_value(gameState, 0, float("-inf"), float("inf"))
        return best_action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
