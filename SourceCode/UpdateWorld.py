import numpy as np
from numpy import random
import copy
import xlrd
import random
from math import floor
import os
import pandas as pd

class UpdateWorld():
    def __init__(self,filePath):
        self.positionFile = pd.read_csv(filePath)

    def __call__(self,designValue):
        pacmanPosition = [self.positionFile.iat[designValue, 1],self.positionFile.iat[designValue, 2]]
        bean1Position=[self.positionFile.iat[designValue, 3],self.positionFile.iat[designValue, 4]]
        bean2Position=[self.positionFile.iat[designValue, 5],self.positionFile.iat[designValue, 6]]
        bottom=self.positionFile.iat[designValue, 7]
        height=self.positionFile.iat[designValue, 8]
        direction=self.positionFile.iat[designValue, 9]
        return pacmanPosition,bean1Position,bean2Position,bottom,height,direction

def main():
    pass



if __name__=="__main__":
    main()
