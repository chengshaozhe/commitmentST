import numpy as np
import pygame as pg
import random
import Visualization



def countCertainNumberInList(listToManipulate, certainNumber):
    count = 0
    indexList = list()
    for i in range(len(listToManipulate)):
        if certainNumber == listToManipulate[i]:
            count = count + 1
            indexList.append(i)

    return count, indexList


class NormalNoise():
    def __init__(self,controller):
        self.actionSpace=controller.actionSpace
        self.gridSize=controller.gridSize


    def __call__(self, playerGrid,action,trajectory,noiseStep, stepCount):
        if stepCount in noiseStep:
            while True:
                actionSpace = self.actionSpace.copy()
                actionSpace.remove(action)
                actionList = [str(action) for action in actionSpace]
                actionStr = np.random.choice(actionList)
                realAction = eval(actionStr)
                if np.all(np.add(playerGrid, realAction) >= 0) and \
                        np.all(np.add(playerGrid, realAction) < self.gridSize):
                    break
        else:
            realAction = action
        realPlayerGrid =tuple(np.add(playerGrid, realAction))
        return realPlayerGrid,realAction

class AwayFromTheGoalNoise():
    def __init__(self,controller):
        self.actionSpace=controller.actionSpace
        self.gridSize=controller.gridSize

    def __call__(self,  playerGrid,targetGridA, targetGridB,action,goal, firstIntentionFlag,firstIntentionMidlineFlag,noiseStep,stepCount):
        if goal != 0 and not firstIntentionFlag and not firstIntentionMidlineFlag:
            noiseStep.append(stepCount)
            firstIntentionFlag = True
            allPosiibileplayerGrid = [np.add(playerGrid, action) for action in self.actionSpace]
            if goal == 1:
                allPossibleDistance = [
                    [np.linalg.norm(np.array(targetGridB) - np.array(possibleGrid), ord=1), possibleGrid] for
                    possibleGrid in allPosiibileplayerGrid]
            else:
                allPossibleDistance = [
                    [np.linalg.norm(np.array(targetGridA) - np.array(possibleGrid), ord=1), possibleGrid] for
                    possibleGrid in allPosiibileplayerGrid]
            orderedAllPossibleDistanceAndGrid = sorted(allPossibleDistance, key=lambda x: x[0])
            orderedAllPossibleDistance = [distance[0] for distance in orderedAllPossibleDistanceAndGrid]
            count, indexList = countCertainNumberInList(orderedAllPossibleDistance,
                                                        orderedAllPossibleDistance[0])
            minIndex = int(count - 1)
            realAction = list(
                np.array(orderedAllPossibleDistanceAndGrid[random.randint(0, minIndex)][1]) - np.array(playerGrid))
            if np.linalg.norm(np.array(targetGridB) - np.array(playerGrid), ord=1) == np.linalg.norm(
                    np.array(targetGridA) - np.array(playerGrid), ord=1):
                firstIntentionMidlineFlag = True
        else:
            realAction=action
        realPlayerGrid =  tuple(np.add(playerGrid, realAction))
        return realPlayerGrid,firstIntentionFlag, firstIntentionMidlineFlag, noiseStep


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
                    if event.key in self.actionDict.keys() and \
                            np.all(np.add(playerGrid, self.actionDict[event.key]) >= 0) and \
                            np.all(np.add(playerGrid, self.actionDict[event.key]) < self.gridSize):
                        action=self.actionDict[event.key]
                        aimePlayerGrid = tuple(np.add(playerGrid, action))
                        pause=False
        return aimePlayerGrid,action


class ModelControllerSoftmax():
    def __init__(self, policy, gridSize):
        self.policy = policy
        self.gridSize = gridSize
        self.actionSpace = [(0, -1),  (0, 1),  (-1, 0), (1, 0)]


    def __call__(self, playerGrid,targetGrid1,targetGrid2):
        action=(0,0)
        pause=True
        try:
            policyOneStep=self.policy[(playerGrid,(targetGrid1,targetGrid2))]
        except KeyError as e:
            policyOneStep=self.policy[(playerGrid,(targetGrid2,targetGrid1))]
        probability = [policyOneStep[self.actionSpace[i]] for i in range(len(policyOneStep))]
        actionSpaceStr=[str(action)  for action in self.actionSpace]
        while pause:
            action = np.random.choice(actionSpaceStr, 1, p=probability).tolist()
            action=eval(action[0])
            if np.all(np.add(playerGrid, action) >= 0) and \
                    np.all(np.add(playerGrid, action) < self.gridSize):
                aimePlayerGrid = tuple(np.add(playerGrid, action))
                pause=False
            else:
                aimePlayerGrid=playerGrid
        return aimePlayerGrid, action

class ModelControllerMax():
    def __init__(self, policy, gridSize):
        self.policy = policy
        self.gridSize = gridSize
        self.actionSpace = [(0, -1),  (0, 1),  (-1, 0), (1, 0)]


    def __call__(self, playerGrid,targetGrid1,targetGrid2):
        action=(0,0)
        pause=True
        try:
            policyOneStep=self.policy[(playerGrid,(targetGrid1,targetGrid2))]
        except KeyError as e:
            policyOneStep=self.policy[(playerGrid,(targetGrid2,targetGrid1))]
        probability = [policyOneStep[self.actionSpace[i]] for i in range(len(policyOneStep))]
        actionSpaceStr=np.array([str(action)  for action in self.actionSpace])
        while pause:
            numberOfMaxProbability, indexOfMaxProbability = countCertainNumberInList(probability, max(probability))
            action = np.random.choice(actionSpaceStr[indexOfMaxProbability].tolist(), 1)
            action=eval(action[0])
            if np.all(np.add(playerGrid, action) >= 0) and \
                    np.all(np.add(playerGrid, action) < self.gridSize):
                aimePlayerGrid = tuple(np.add(playerGrid, action))
                pause=False
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

