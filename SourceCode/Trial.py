import numpy as np
import pygame as pg
from pygame import time
import collections as co
import pickle
from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController,ModelController
import UpdateWorld
import random


# def extractNoRepeatingElements(list, number):
#     while True:
#         point = np.random.choice(list, number).tolist()
#         if set(point) == number:
#             break
#     return point

def extractNoRepeatingElements(list, number):
    point =random.sample(list, number)
    print(point)
    return point

class Trial():
    def __init__(self,humanController,drawNewState,drawText):
        self.humanController=humanController
        self.drawNewState=drawNewState
        self.drawText=drawText

    def checkTerminationOfTrial(self,bean1Grid, bean2Grid, humanGrid):
        if np.linalg.norm(np.array(humanGrid) - np.array(bean1Grid), ord=1)==0 or \
                np.linalg.norm(np.array(humanGrid) - np.array(bean2Grid), ord=1) == 0 :
            pause=False
        else:
            pause=True
        return pause

    def __call__(self,bean1Grid,bean2Grid,playerGrid,designValues):
        pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT])
        self.drawNewState(bean1Grid, bean2Grid, playerGrid)
        self.humanController()




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

