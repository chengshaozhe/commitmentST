import numpy as np
import pygame as pg
from pygame import time
import collections as co
import pickle
from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController,ModelControllerSoftmax
import UpdateWorld
import random


def inferGoal(trajectory, aimGrid, targetGridA, targetGridB):
    pacmanBean1aimDisplacement = np.linalg.norm(np.array(targetGridA) - np.array(aimGrid), ord=1)
    pacmanBean2aimDisplacement = np.linalg.norm(np.array(targetGridB) - np.array(aimGrid), ord=1)
    pacmanBean1LastStepDisplacement = np.linalg.norm(np.array(targetGridA) - np.array(trajectory[-1]), ord=1)
    pacmanBean2LastStepDisplacement = np.linalg.norm(np.array(targetGridB) - np.array(trajectory[-1]), ord=1)
    bean1Goal = pacmanBean1LastStepDisplacement - pacmanBean1aimDisplacement
    bean2Goal = pacmanBean2LastStepDisplacement - pacmanBean2aimDisplacement
    if bean1Goal > bean2Goal:
        goal = 1
    elif bean1Goal < bean2Goal:
        goal = 2
    else:
        goal = 0
    return goal

def extractNoRepeatingElements(list, number):
    point =random.sample(list, number)
    return point

class NormalTrial():
    def __init__(self,controller,drawNewState,drawText,normalNoise):
        self.controller=controller
        self.drawNewState=drawNewState
        self.drawText=drawText
        self.normalNoise=normalNoise

    def checkTerminationOfTrial(self,bean1Grid, bean2Grid, humanGrid):
        if np.linalg.norm(np.array(humanGrid) - np.array(bean1Grid), ord=1)==0 or \
                np.linalg.norm(np.array(humanGrid) - np.array(bean2Grid), ord=1) == 0 :
            pause=False
        else:
            pause=True
        return pause

    def __call__(self,bean1Grid,bean2Grid,playerGrid,designValues):
        initialPlayerGrid=playerGrid
        initialTime = time.get_ticks()
        reactionTime=list()
        trajectory=[initialPlayerGrid]
        results=co.OrderedDict()
        aimActionList=list()
        totalStep=int(np.linalg.norm(np.array(playerGrid) - np.array(bean1Grid), ord=1))
        noiseStep = random.sample(list(range(1, totalStep + 1)), designValues)
        stepCount=0
        goalList=list()
        self.drawText("+",[0,0,0],[7,7])
        pg.time.wait(1300)
        self.drawNewState(bean1Grid,bean2Grid,initialPlayerGrid)
        pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT])
        aimPlayerGrid,aimAction =self.controller(initialPlayerGrid,bean1Grid,bean2Grid)
        goal = inferGoal(trajectory, aimPlayerGrid, bean1Grid, bean2Grid)
        goalList.append(goal)
        stepCount=stepCount+1
        realPlayerGrid,aimAction=self.normalNoise( trajectory[-1],aimAction,trajectory,noiseStep, stepCount)
        self.drawNewState(bean1Grid,bean2Grid,realPlayerGrid)
        reactionTime.append(time.get_ticks() - initialTime)
        trajectory.append(list(realPlayerGrid))
        aimActionList.append(aimAction)
        pause = self.checkTerminationOfTrial(bean1Grid, bean2Grid, realPlayerGrid)
        while pause:
            aimPlayerGrid, aimAction = self.controller(realPlayerGrid, bean1Grid, bean2Grid)
            goal = inferGoal(trajectory, aimPlayerGrid, bean1Grid, bean2Grid)
            goalList.append(goal)
            stepCount = stepCount + 1
            realPlayerGrid,aimAction = self.normalNoise(trajectory[-1], aimAction, trajectory, noiseStep, stepCount)
            self.drawNewState(bean1Grid, bean2Grid, realPlayerGrid)
            # pg.time.delay(1000)
            reactionTime.append(time.get_ticks() - initialTime)
            trajectory.append(list(realPlayerGrid))
            aimActionList.append(aimAction)
            pause = self.checkTerminationOfTrial(bean1Grid, bean2Grid, realPlayerGrid)
        pg.time.wait(500)
        pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])
        results["bean1GridX"] = bean1Grid[0]
        results["bean1GridY"] = bean1Grid[1]
        results["bean2GridX"] = bean2Grid[0]
        results["bean2GridY"] = bean2Grid[1]
        results["playerGridX"] = initialPlayerGrid[0]
        results["playerGridY"] = initialPlayerGrid[1]
        results["reactionTime"]=str(reactionTime)
        results["trajectory"]=str(trajectory)
        results["aimAction"]=str(aimActionList)
        results["noisePoint"]=str(noiseStep)
        results["goal"]=str(goalList)
        return results

class SpecialTrial():
    def __init__(self,controller,drawNewState,drawText,awayFromTheGoalNoise):
        self.controller = controller
        self.drawNewState = drawNewState
        self.drawText = drawText
        self.awayFromTheGoalNoise=awayFromTheGoalNoise

    def checkTerminationOfTrial(self,bean1Grid, bean2Grid, humanGrid):
        if np.linalg.norm(np.array(humanGrid) - np.array(bean1Grid), ord=1)==0 or \
                np.linalg.norm(np.array(humanGrid) - np.array(bean2Grid), ord=1) == 0 :
            pause=False
        else:
            pause=True
        return pause

    def __call__(self,bean1Grid,bean2Grid,playerGrid,designValues):
        initialPlayerGrid = playerGrid
        initialTime = time.get_ticks()
        reactionTime = list()
        trajectory = [initialPlayerGrid]
        results = co.OrderedDict()
        aimActionList = list()
        firstIntentionFlag=False
        firstIntentionMidlineFlag=False
        totalStep = int(np.linalg.norm(np.array(playerGrid) - np.array(bean1Grid), ord=1))
        noiseStep = list()
        stepCount = 0
        goalList = list()
        self.drawText("+", [0, 0, 0], [7, 7])
        pg.time.wait(1300)
        self.drawNewState(bean1Grid,bean2Grid,initialPlayerGrid)
        pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
        aimPlayerGrid, aimAction = self.controller(initialPlayerGrid,bean1Grid,bean2Grid)
        goal = inferGoal(trajectory, aimPlayerGrid, bean1Grid, bean2Grid)
        goalList.append(goal)
        stepCount=stepCount+1
        realPlayerGrid,firstIntentionFlag, firstIntentionMidlineFlag, noiseStep = self.awayFromTheGoalNoise(trajectory[-1],
                                                bean1Grid,bean2Grid,aimAction,goal, firstIntentionFlag,
                                              firstIntentionMidlineFlag,noiseStep, stepCount)

        self.drawNewState(bean1Grid,bean2Grid,realPlayerGrid)
        reactionTime.append(time.get_ticks() - initialTime)
        trajectory.append(list(realPlayerGrid))
        aimActionList.append(aimAction)
        pause = self.checkTerminationOfTrial(bean1Grid, bean2Grid, realPlayerGrid)
        while pause:
            aimPlayerGrid, aimAction = self.controller(realPlayerGrid, bean1Grid, bean2Grid)
            goal = inferGoal(trajectory, aimPlayerGrid, bean1Grid, bean2Grid)
            goalList.append(goal)
            stepCount = stepCount + 1
            realPlayerGrid, firstIntentionFlag, firstIntentionMidlineFlag, noiseStep = self.awayFromTheGoalNoise(
                trajectory[-1], bean1Grid, bean2Grid, aimAction, goal, firstIntentionFlag,
                firstIntentionMidlineFlag, noiseStep, stepCount)
            self.drawNewState(bean1Grid, bean2Grid, realPlayerGrid)
            reactionTime.append(time.get_ticks() - initialTime)
            trajectory.append(list(realPlayerGrid))
            aimActionList.append(aimAction)
            pause = self.checkTerminationOfTrial(bean1Grid, bean2Grid, realPlayerGrid)
        pg.time.wait(500)
        pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])
        results["bean1GridX"] = bean1Grid[0]
        results["bean1GridY"] = bean1Grid[1]
        results["bean2GridX"] = bean2Grid[0]
        results["bean2GridY"] = bean2Grid[1]
        results["playerGridX"] = initialPlayerGrid[0]
        results["playerGridY"] = initialPlayerGrid[1]
        results["reactionTime"] = str(reactionTime)
        results["trajectory"] = str(trajectory)
        results["aimAction"] = str(aimActionList)
        results["noisePoint"] = str(noiseStep)
        results["goal"] = str(goalList)
        return results




def main():
    dimension = 21
    bounds = [0, 0, dimension - 1, dimension - 1]
    minDistanceBetweenGrids = 5
    condition = [-5, -3, -1, 0, 1, 3, 5]
    initialWorld = UpdateWorld.InitialWorld(bounds)
    pg.init()
    screenWidth = 720
    screenHeight = 720
    screen = pg.display.set_mode((screenWidth, screenHeight))
    gridSize = 21
    leaveEdgeSpace = 2
    lineWidth = 1
    backgroundColor = [205, 255, 204]
    lineColor = [0, 0, 0]
    targetColor = [255, 50, 50]
    playerColor = [50, 50, 255]
    targetRadius = 10
    playerRadius = 10
    stopwatchUnit=10
    textColorTuple=(255,50,50)
    stopwatchEvent = pg.USEREVENT + 1
    pg.time.set_timer(stopwatchEvent, stopwatchUnit)
    pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, stopwatchEvent])
    finishTime=90000
    currentStopwatch=32888
    score=0
    drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
    drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
    humanController=HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
    policy=pickle.load(open("SingleWolfTwoSheepsGrid15.pkl","rb"))
    modelController=ModelController(policy, gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
    trial=Trial(modelController, drawNewState, stopwatchEvent, finishTime)
    bean1Grid,bean2Grid,playerGrid=initialWorld(minDistanceBetweenGrids)
    bean1Grid=(3,13)
    bean2Grid=(5,0)
    playerGrid=(0,8)
    results=trial(bean1Grid, bean2Grid, playerGrid, score, currentStopwatch)


if __name__=="__main__":
    main()

