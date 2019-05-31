import pygame as pg
import os
import pandas as pd
import collections as co
import numpy as np
import pickle
from Visualization import DrawBackground, DrawNewState, DrawImage,DrawText
from Controller import HumanController,ModelController
import UpdateWorld
from Writer import WriteDataFrameToCSV
from Trial import Trial
from itertools import combinations, permutations

class Experiment():
    def __init__(self, trial,designValues,updateWorld):
        self.trial = trial
        self.designValues=designValues
        self.updateWorld=updateWorld

    def __call__(self):
        for designValue in self.designValues:
            playerGrid,bean1Grid, bean2Grid,bottom,height,direction = self.updateWorld(designValue)
            print(playerGrid,bean1Grid, bean2Grid,bottom,height,direction)
            self.trial(bean1Grid, bean2Grid, playerGrid,designValue)


def main():
    dimension =15
    condition=list(permutations([1, 2, 0], 3))
    condition.append((1, 1, 1))
    designValues=range(100)
    fileName=input("Please enter fileName:")
    positionPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'+fileName+'.csv'
    updateWorld = UpdateWorld.UpdateWorld(positionPath)
    pg.init()
    screenWidth = 600
    screenHeight = 600
    screen = pg.display.set_mode((screenWidth, screenHeight))
    leaveEdgeSpace = 2
    lineWidth = 1
    backgroundColor = [205, 255, 204]
    lineColor = [0, 0, 0]
    targetColor = [255, 50, 50]
    playerColor = [50, 50, 255]
    targetRadius = 10
    playerRadius = 10
    textColorTuple = (255, 50, 50)
    drawBackground = DrawBackground(screen, dimension, leaveEdgeSpace, backgroundColor, lineColor, lineWidth,
                                    textColorTuple)
    drawText=DrawText(screen,drawBackground)
    drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
    humanController = HumanController(dimension,drawNewState)
    # policy = pickle.load(open("SingleWolfTwoSheepsGrid15.pkl","rb"))
    # modelController = ModelController(policy, dimension, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
    trial = Trial(humanController, drawNewState,drawText)
    experiment = Experiment(trial,designValues,updateWorld)
    experiment()



if __name__ == "__main__":
    main()
