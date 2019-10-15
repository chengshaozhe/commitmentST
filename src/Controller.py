import numpy as np
import pygame as pg
import random
import Visualization



def inferGoal(originGrid, aimGrid, targetGridA, targetGridB):
    pacmanBean1aimDisplacement = np.linalg.norm(np.array(targetGridA) - np.array(aimGrid), ord=1)
    pacmanBean2aimDisplacement = np.linalg.norm(np.array(targetGridB) - np.array(aimGrid), ord=1)
    pacmanBean1LastStepDisplacement = np.linalg.norm(np.array(targetGridA) - np.array(originGrid), ord=1)
    pacmanBean2LastStepDisplacement = np.linalg.norm(np.array(targetGridB) - np.array(originGrid), ord=1)
    bean1Goal = pacmanBean1LastStepDisplacement - pacmanBean1aimDisplacement
    bean2Goal = pacmanBean2LastStepDisplacement - pacmanBean2aimDisplacement
    if bean1Goal > bean2Goal:
        goal = 1
    elif bean1Goal < bean2Goal:
        goal = 2
    else:
        goal = 0
    return goal

def countCertainNumberInList(listToManipulate, certainNumber):
    count = 0
    indexList = list()
    for i in range(len(listToManipulate)):
        if certainNumber == listToManipulate[i]:
            count = count + 1
            indexList.append(i)

    return count, indexList

def calculateSoftmaxProbability(probabilityList,beita):
	newProbabilityList=list(np.divide(np.exp(np.multiply(beita,probabilityList)),np.sum(np.exp(np.multiply(beita,probabilityList)))))
	return newProbabilityList

class NormalNoise():
    def __init__(self,controller):
        self.actionSpace=controller.actionSpace
        self.gridSize=controller.gridSize


    def __call__(self, playerGrid,action,trajectory,noiseStep, stepCount):
        if stepCount in noiseStep:
            actionSpace = self.actionSpace.copy()
            actionSpace.remove(action)
            actionList = [str(action) for action in actionSpace]
            actionStr = np.random.choice(actionList)
            realAction = eval(actionStr)
        else:
            realAction = action
        realPlayerGrid =tuple(np.add(playerGrid, realAction))
        return realPlayerGrid,realAction

def selectActionMinDistanceFromTarget(goal,playerGrid,bean1Grid,bean2Grid,actionSpace):
    allPosiibilePlayerGrid = [np.add(playerGrid, action) for action in actionSpace]
    allActionGoal = [inferGoal(playerGrid, possibleGrid, bean1Grid, bean2Grid) for possibleGrid in
                     allPosiibilePlayerGrid]
    if goal == 1:
        realActionIndex = allActionGoal.index(2)
    else:
        realActionIndex = allActionGoal.index(1)
    realAction = actionSpace[realActionIndex]
    return realAction


class AwayFromTheGoalNoise():
    def __init__(self,controller):
        self.actionSpace=controller.actionSpace
        self.gridSize=controller.gridSize

    def __call__(self,  playerGrid,bean1Grid, bean2Grid,action,goal, firstIntentionFlag,noiseStep,stepCount):
        if goal != 0 and not firstIntentionFlag :
            noiseStep.append(stepCount)
            firstIntentionFlag = True
            realAction=selectActionMinDistanceFromTarget(goal,playerGrid,bean1Grid,bean2Grid,self.actionSpace)
        else:
            realAction=action
        realPlayerGrid =  tuple(np.add(playerGrid, realAction))
        return realPlayerGrid,firstIntentionFlag, noiseStep


class HumanController():
    def __init__(self, gridSize):
        self.actionDict = {pg.K_UP: (0, -1), pg.K_DOWN: (0, 1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}
        self.actionSpace = [(0, -1),  (0, 1),  (-1, 0), (1, 0)]
        self.gridSize = gridSize


    def __call__(self, playerGrid,targetGrid1,targetGrid2):
        action = [0, 0]
        pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key in self.actionDict.keys():
                        action=self.actionDict[event.key]
                        aimePlayerGrid = tuple(np.add(playerGrid, action))
                        pause=False
        return aimePlayerGrid,action

class CheckBoundary():
    def __init__(self, xBoundary, yBoundary):
        self.xMin, self.xMax = xBoundary
        self.yMin, self.yMax = yBoundary

    def __call__(self, position):
        adjustedX, adjustedY = position
        if position[0] >= self.xMax:
            adjustedX = self.xMax
        if position[0] <= self.xMin:
            adjustedX =  self.xMin
        if position[1] >= self.yMax:
            adjustedY =  self.yMax
        if position[1] <= self.yMin:
            adjustedY = self.yMin
        checkedPosition =(adjustedX, adjustedY)
        return checkedPosition


class ModelController():
    def __init__(self, policy, gridSize,softmaxBeta):
        self.policy = policy
        self.gridSize = gridSize
        self.actionSpace = [(0, -1),  (0, 1),  (-1, 0), (1, 0)]
        self. softmaxBeta=softmaxBeta


    def __call__(self, playerGrid,targetGrid1,targetGrid2):
        try:
            policyForCurrentStateDict = self.policy[(playerGrid, (targetGrid1, targetGrid2))]
        except KeyError as e:
            policyForCurrentStateDict = self.policy[(playerGrid, (targetGrid2, targetGrid1))]
        if self.softmaxBeta < 0:
            actionMaxList = [action for action in policyForCurrentStateDict.keys() if
                             policyForCurrentStateDict[action] == np.max(list(policyForCurrentStateDict.values()))]
            action = random.choice(actionMaxList)
        else:
            actionProbability = np.divide(list(policyForCurrentStateDict.values()),
                                          np.sum(list(policyForCurrentStateDict.values())))
            softmaxProbabilityList = calculateSoftmaxProbability(          list(actionProbability), self.softmaxBeta)
            action = list(policyForCurrentStateDict.keys())[
                list(np.random.multinomial(1, softmaxProbabilityList)).index(1)]
        aimePlayerGrid = tuple(np.add(playerGrid, action))
        pg.time.delay(0)
        return aimePlayerGrid, action

if __name__ == "__main__":
    pg.init()
    screenWidth = 720
    screenHeight = 720
    screen = pg.display.set_mode((screenWidth, screenHeight))
    gridSize = 20
    leaveEdgeSpace = 2
    lineWidth = 2
    backgroundColor = [188, 188, 0]
    lineColor = [255, 255, 255]
    targetColor = [255, 50, 50]
    playerColor = [50, 50, 255]
    targetRadius = 10
    playerRadius = 10
    targetGridA = [5, 5]
    targetGridB = [15, 5]
    playerGrid = [10, 15]
    currentScore = 5
    textColorTuple = (255, 50, 50)
    stopwatchEvent = pg.USEREVENT + 1
    stopwatchUnit = 10
    pg.time.set_timer(stopwatchEvent, stopwatchUnit)
    finishTime = 90000
    currentStopwatch = 32000

    drawBackground = Visualization.DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor,
                                                  lineWidth, textColorTuple)
    drawNewState = Visualization.DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius,
                                              playerRadius)

    getHumanAction = HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
    import pickle

    policy = pickle.load(open("SingleWolfTwoSheepsGrid15.pkl", "rb"))
    getModelAction = ModelController(policy, gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)

    # [playerNextPosition,action,newStopwatch]=getHumanAction(targetGridA, targetGridB, playerGrid, currentScore, currentStopwatch)
    [playerNextPosition, action, newStopwatch] = getModelAction(targetGridA, targetGridB, playerGrid, currentScore,
                                                                currentStopwatch)
    print(playerNextPosition, action, newStopwatch)

    pg.quit()

