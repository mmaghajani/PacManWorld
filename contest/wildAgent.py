from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveReflexAgent', second='DefensiveReflexAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
    def getSuccessor(self, gameState, action):
      #TODO
        return 0


class OffensiveReflexAgent(ReflexCaptureAgent):

    def getFeatures(self, gameState, action):

        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        features['successorScore'] = self.getScore(successor)

        foodList = self.getFood(successor).asList()
        if len(foodList) > 0:
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        myPos = successor.getAgentState(self.index).getPosition()
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        inRange = filter(lambda x: not x.isPacman and x.getPosition() != None, enemies)
        if len(inRange) > 0:
            positions = [agent.getPosition() for agent in inRange]
            closest = min(positions, key=lambda x: self.getMazeDistance(myPos, x))
            closestDist = self.getMazeDistance(myPos, closest)
            if closestDist <= 5:
                features['distanceToGhost'] = closestDist

        features['isPacman'] = 1 if successor.getAgentState(self.index).isPacman else 0

        return features

    def getWeights(self, gameState, action):
        if self.inactiveTime > 80:
            return {'successorScore': 200, 'distanceToFood': -5, 'distanceToGhost': 2, 'isPacman': 1000}
        successor = self.getSuccessor(gameState, action)
        myPos = successor.getAgentState(self.index).getPosition()
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        inRange = filter(lambda x: not x.isPacman and x.getPosition() != None, enemies)
        if len(inRange) > 0:
            positions = [agent.getPosition() for agent in inRange]
            closestPos = min(positions, key=lambda x: self.getMazeDistance(myPos, x))
            closestDist = self.getMazeDistance(myPos, closestPos)
            closest_enemies = filter(lambda x: x[0] == closestPos, zip(positions, inRange))
            for agent in closest_enemies:
                if agent[1].scaredTimer > 0:
                    return {'successorScore': 200, 'distanceToFood': -5, 'distanceToGhost': 0, 'isPacman': 0}
        return {'successorScore': 200, 'distanceToFood': -5, 'distanceToGhost': 2, 'isPacman': 0}

    def __init__(self, index):
        CaptureAgent.__init__(self, index)

        self.numEnemyFood = "+inf"
        self.inactiveTime = 0


class DefensiveReflexAgent(ReflexCaptureAgent):
    class DefensiveReflexAgent(ReflexCaptureAgent):

        def __init__(self, index):
            CaptureAgent.__init__(self, index)
            self.target = None
            self.lastObservedFood = None
            # This variable will store our patrol points and
            # the agent probability to select a point as target.
            self.patrolDict = {}

        def distFoodToPatrol(self, gameState):
            food = self.getFoodYouAreDefending(gameState).asList()
            total = 0
            for position in self.noWallSpots:
                closestFoodDist = "+inf"
                for foodPos in food:
                    dist = self.getMazeDistance(position, foodPos)
                    if dist < closestFoodDist:
                        closestFoodDist = dist
                # We can't divide by 0!
                if closestFoodDist == 0:
                    closestFoodDist = 1
                self.patrolDict[position] = 1.0 / float(closestFoodDist)
                total += self.patrolDict[position]
            if total == 0:
                total = 1
            for x in self.patrolDict.keys():
                self.patrolDict[x] = float(self.patrolDict[x]) / float(total)