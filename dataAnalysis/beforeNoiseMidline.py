import pandas as pd
import matplotlib.pyplot as plt
import os
import pylab as pl
import numpy as np
from functools import reduce
from math import ceil, floor
from collections import Counter


def createAllCertainFormatFileList(filePath, fileFormat):
    filenameList = [os.path.join(filePath, relativeFilename) for relativeFilename in os.listdir(filePath)
                    if os.path.isfile(os.path.join(filePath, relativeFilename))
                    if os.path.splitext(relativeFilename)[1] in fileFormat]
    return filenameList


# def calculateMidlineRatioBeforeAwayByNoise(trajectory,bean1Grid,bean2Grid,noise,action):
#     # trajectory的第n个点是被噪声影响的点，index的n-1点被噪声影响，index的n-2点产生噪声
#     midlineList=list()
#     for step in range(1,len(trajectory)):
#         pacmanGrid=trajectory[step]
#         midlineFlag=np.linalg.norm(np.array(pacmanGrid) - np.array(bean1Grid), ord=1)== np.linalg.norm(np.array(pacmanGrid) - np.array(bean2Grid), ord=1)
#         if midlineFlag:
#             if step+1 not in noise:
#                 midlineList.append(pacmanGrid)
#             else:
#                 realPacmanGrid=np.array(trajectory[step-1])+np.array(action[step-1])
#                 if  np.linalg.norm(np.array(realPacmanGrid) - np.array(bean1Grid), ord=1)== np.linalg.norm(np.array(realPacmanGrid) - np.array(bean2Grid), ord=1):
#                     midlineList.append(pacmanGrid)
#         else:
#             break
#     return midlineList

def calculateMidlineRatioBeforeAwayByNoise(trajectory, bean1Grid, bean2Grid, noise, action):
    # trajectory的第n个点是被噪声影响的点，index的n-1点被噪声影响，index的n-2点产生噪声
    midlineList = list()
    for step in range(1, len(trajectory)):
        pacmanGrid = trajectory[step]
        midlineFlag = np.linalg.norm(np.array(pacmanGrid) - np.array(bean1Grid), ord=1) == np.linalg.norm(np.array(pacmanGrid) - np.array(bean2Grid), ord=1)
        if midlineFlag:
            midlineList.append(pacmanGrid)
        else:
            break
    return midlineList


if __name__ == "__main__":
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/results/human'
    fileFormat = '.csv'
    resultsFilenameList = createAllCertainFormatFileList(resultsPath, fileFormat)
    resultsDataFrameList = [pd.read_csv(file) for file in resultsFilenameList]
    resultsDataFrame = pd.concat(resultsDataFrameList, sort=False)
    trialNumber = resultsDataFrame.shape[0]
    avoidCommitmentRatioList = list()
    for results in resultsDataFrameList:
        participantAvoidCommitmentRatioList = list()
        trialNumber = results.shape[0]
        for i in range(trialNumber):
            bean1Grid = [results.iat[i, 2], results.iat[i, 3]]
            bean2Grid = [results.iat[i, 4], results.iat[i, 5]]
            playerGrid = [results.iat[i, 5], results.iat[i, 7]]
            # trajectory的第n个点是被噪声影响的点，index的n-1点被噪声影响，index的n-2点产生噪声
            noiseList = eval(resultsDataFrame.iat[i, 11])
            actionList = eval(resultsDataFrame.iat[i, 10])
            trajectory = eval(resultsDataFrame.iat[i, 9])
            midline = calculateMidlineRatioBeforeAwayByNoise(trajectory, bean1Grid, bean2Grid, noiseList, actionList)
            participantAvoidCommitmentRatioList.append(len(midline) / len(trajectory))
        avoidCommitmentRatioList.append(np.array(participantAvoidCommitmentRatioList))
    averageAvoidCommitmentRatio = np.mean(np.array(avoidCommitmentRatioList[0]))
    stdAvoidCommitmentRatio = np.std(np.array(avoidCommitmentRatioList[0])) / np.sqrt(len(avoidCommitmentRatioList) - 1)
    print(averageAvoidCommitmentRatio)
    print(stdAvoidCommitmentRatio)
