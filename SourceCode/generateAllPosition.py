import numpy as np
from numpy import random
import copy
import xlrd
import random
from math import floor
from Writer import WriteDataFrameToCSV
import os
import collections as co
import pandas as pd
from math import floor


class UpdateWorld():
    def __init__(self, dimension):
        self.dimension = dimension

    def __call__(self,bottom,height,direction):
        if direction == 0:
            pacmanPosition=[[floor(self.dimension/2),y] for y in range(height,self.dimension)]
            bean1Position = [[pacman[0] - floor(bottom / 2), pacman[1] - height] for pacman in pacmanPosition]
            bean2Position = [[pacman[0] + floor(bottom / 2), pacman[1] - height] for pacman in pacmanPosition]
        elif direction == 180:
            pacmanPosition = [[floor(self.dimension / 2), y] for y in range(self.dimension-height)]
            bean1Position = [[pacman[0] - floor(bottom / 2), pacman[1] + height] for pacman in pacmanPosition]
            bean2Position = [[pacman[0] + floor(bottom / 2), pacman[1] + height] for pacman in pacmanPosition]
        elif direction == 90:
            pacmanPosition = [[x, floor(self.dimension / 2)] for x in range(self.dimension-height)]
            bean1Position = [[pacman[0] + height, pacman[1] - floor(bottom / 2)] for pacman in pacmanPosition]
            bean2Position = [[pacman[0] + height, pacman[1] + floor(bottom / 2)] for pacman in pacmanPosition]
        else:
            pacmanPosition = [[x, floor(self.dimension / 2)] for x in range(height,self.dimension)]
            bean1Position = [[pacman[0] - height, pacman[1] - floor(bottom / 2)] for pacman in pacmanPosition]
            bean2Position = [[pacman[0] - height, pacman[1] + floor(bottom / 2)] for pacman in pacmanPosition]
        return pacmanPosition, bean1Position, bean2Position, bottom, height, direction


def main():
    bottoms = [4, 6, 8]
    heights = [6, 7, 8]
    directions = [0, 90, 180, 270]
    dimension=15
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
    fileName=input("Please enter the file name:").capitalize()
    writerPath = resultsPath + fileName + '.csv'
    writer = WriteDataFrameToCSV(writerPath)
    updateWorld=UpdateWorld(dimension)
    position=co.OrderedDict()
    designValues=0
    for bottom in bottoms :
        for height in heights:
            for direction in directions:
                pacmanPosition, bean1Position, bean2Position, bottom, height, direction=updateWorld(bottom,height,direction)
                for i in range(len(pacmanPosition)):
                    designValues = designValues + 1
                    position["pacmanPositionX"]=pacmanPosition[i][0]
                    position["pacmanPositionY"]=pacmanPosition[i][1]
                    position["bean1PositionX"]=bean1Position[i][0]
                    position["bean1PositionY"]=bean1Position[i][1]
                    position["bean2PositionX"]=bean2Position[i][0]
                    position["bean2PositionY"]=bean2Position[i][1]
                    position["bottom"]=bottom
                    position["height"]=height
                    position["direction"]=direction
                    responseDF = pd.DataFrame(position,index=[designValues])
                    writer(responseDF)



if __name__ == "__main__":
    main()
