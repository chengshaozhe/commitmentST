import numpy as np
from numpy import random
import copy
import xlrd
import random
from math import floor


class UpdateWorld():
    def __init__(self,bottom,height,direction,dimension):
        self.bottom=bottom
        self.height=height
        self.direction=direction
        self.dimension=dimension

    def __call__(self):
        bottom=random.choice(self.bottom)
        height=random.choice(self.height)
        direction=random.choice(self.direction)
        if direction==0:
            pacmanPosition=[floor(self.dimension/2),random.randint(height,self.dimension-1)]
            bean1Position=[pacmanPosition[0]-floor(bottom/2),pacmanPosition[1]-height]
            bean2Position=[pacmanPosition[0]+floor(bottom/2),pacmanPosition[1]-height]
        elif direction==180:
            pacmanPosition = [floor(self.dimension / 2),random.randint(0, self.dimension - 1-height)]
            bean1Position = [pacmanPosition[0] - floor(bottom / 2), pacmanPosition[1] + height]
            bean2Position = [pacmanPosition[0] + floor(bottom / 2), pacmanPosition[1] + height]
        elif direction==90:
            pacmanPosition = [random.randint(0, self.dimension - 1-height),floor(self.dimension / 2)]
            bean1Position = [pacmanPosition[0] + height,pacmanPosition[1]- floor(bottom / 2) ]
            bean2Position = [pacmanPosition[0] + height,pacmanPosition[1]+ floor(bottom / 2)]
        else:
            pacmanPosition = [random.randint(height,self.dimension-1),floor(self.dimension / 2)]
            bean1Position = [pacmanPosition[0] - height, pacmanPosition[1] - floor(bottom / 2)]
            bean2Position = [pacmanPosition[0] - height, pacmanPosition[1] + floor(bottom / 2)]
        return pacmanPosition,bean1Position,bean2Position,bottom,height,direction


def createDesignValue(condition,blockNumber):
    designValuesIndex=random.sample(list(range(len(condition))),blockNumber)
    designValues=np.array(condition)[designValuesIndex].flatten().tolist()
    return designValues

def main():
    pass

if __name__=="__main__":
    main()
