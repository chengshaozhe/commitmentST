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
    def __init__(self, trial, writer, experimentValues,  updateWorld, drawImage, resultsPath, \
                 minDistanceBetweenGrids):
        self.trial = trial
        self.writer = writer
        self.experimentValues = experimentValues
        self.updateWorld = updateWorld
        self.drawImage = drawImage
        self.resultsPath = resultsPath
        self.minDistanceBetweenGrids = minDistanceBetweenGrids

    def __call__(self,designValues):
        for designValue in designValues:
            playerGrid,bean1Grid, bean2Grid,bottom,height,direction = self.updateWorld()
            print(playerGrid,bean1Grid, bean2Grid,bottom,height,direction)
            results = self.trial(bean1Grid, bean2Grid, playerGrid,designValue)
            results["bottom"]=bottom
            results["height"]=height
            results["direction"]=direction
            response = self.experimentValues.copy()
            response.update(results)
            responseDF = pd.DataFrame(response, index=[designValue])
            self.writer(responseDF)


def main():
    dimension =15
    minDistanceBetweenGrids = 5
    blockNumber = 3
    condition=list(permutations([1, 2, 0], 3))
    condition.append((1, 1, 1))
    designValues=UpdateWorld.createDesignValue(condition,blockNumber)
    designValues.append('special')
    picturePath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Pictures/'
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
    bottom=[4,6,8]
    height=[6,7,8]
    direction=[0,90,180,270]
    updateWorld = UpdateWorld.UpdateWorld(bottom,height,direction,dimension)
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
    experimentValues = co.OrderedDict()
    experimentValues["name"] = input("Please enter your name:").capitalize()
    writerPath = resultsPath + experimentValues["name"] + '.csv'
    writer = WriteDataFrameToCSV(writerPath)
    introductionImage = pg.image.load(picturePath + 'introduction.png')
    finishImage = pg.image.load(picturePath + 'finish.png')
    introductionImage=pg.transform.scale(introductionImage, (screenWidth,screenHeight))
    finishImage=pg.transform.scale(finishImage, (int(screenWidth*2/3),int(screenHeight/4)))
    drawBackground = DrawBackground(screen, dimension, leaveEdgeSpace, backgroundColor, lineColor, lineWidth,
                                    textColorTuple)
    drawText=DrawText(screen,drawBackground)
    drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
    drawImage = DrawImage(screen)
    humanController = HumanController(dimension,drawNewState)
    # policy = pickle.load(open("SingleWolfTwoSheepsGrid15.pkl","rb"))
    # modelController = ModelController(policy, dimension, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
    trial = Trial(humanController, drawNewState,drawText)
    experiment = Experiment(trial, writer, experimentValues, updateWorld, drawImage, resultsPath,
                             minDistanceBetweenGrids)
    drawImage(introductionImage)
    experiment(designValues)
    drawImage(finishImage)



if __name__ == "__main__":
    main()
