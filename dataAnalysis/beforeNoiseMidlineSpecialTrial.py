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


def calculateFirstIntentionStep(intentionList):
    goal1Step = float('inf')
    goal2Step = float('inf')
    if 1 in intentionList:
        goal1Step = intentionList.index(1)
    if 2 in intentionList:
        goal2Step = intentionList.index(2)
    firstIntentionStep = min(goal1Step, goal2Step)
    if goal1Step < goal2Step:
        firstIntention = 1
    elif goal2Step < goal1Step:
        firstIntention = 2
    else:
        firstIntention = 0
    return firstIntentionStep + 1


if __name__ == "__main__":
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/maxModelNoNoise'
    fileFormat = '.csv'
    resultsFilenameList = createAllCertainFormatFileList(resultsPath, fileFormat)
    resultsDataFrameList = [pd.read_csv(file) for file in resultsFilenameList]
    specialTrialIndex = 9
    resultsDataFrame = pd.concat(resultsDataFrameList, sort=False)
    everyExperimentTrialNumber = 10
    specialTrialResultsDataFrame = resultsDataFrame.iloc[list(range(specialTrialIndex, resultsDataFrame.shape[0], everyExperimentTrialNumber))]
    specialTrialNumber = specialTrialResultsDataFrame.shape[0]
    participantsTypeList = ['machine' if 'machine' in name else 'Human' for name in specialTrialResultsDataFrame['name']]
    specialTrialResultsDataFrame['participantsType'] = participantsTypeList
    specialTrialResultsDataFrame['goal'] = specialTrialResultsDataFrame['goal']
    avoidCommitmentRatioList = list()
    for i in range(specialTrialNumber):
        bean1Grid = [specialTrialResultsDataFrame.iat[i, 2], specialTrialResultsDataFrame.iat[i, 3]]
        bean2Grid = [specialTrialResultsDataFrame.iat[i, 4], specialTrialResultsDataFrame.iat[i, 5]]
        playerGrid = [specialTrialResultsDataFrame.iat[i, 5], specialTrialResultsDataFrame.iat[i, 7]]
        # trajectory的第n个点是被噪声影响的点，index的n-1点被噪声影响，index的n-2点产生噪声
        noiseList = eval(specialTrialResultsDataFrame.iat[i, 11])
        actionList = eval(specialTrialResultsDataFrame.iat[i, 10])
        trajectory = eval(specialTrialResultsDataFrame.iat[i, 9])
        goal = eval(resultsDataFrame.iat[i, 12])

        # firstIntentionStep = calculateFirstIntentionStep(goal)
        # avoidCommitmentRatioList.append(firstIntentionStep / len(trajectory))

        midline = calculateMidlineRatioBeforeAwayByNoise(trajectory, bean1Grid, bean2Grid, noiseList, actionList)
        avoidCommitmentRatioList.append(len(midline) / len(trajectory))
    averageAvoidCommitmentRatio = np.mean(np.array(avoidCommitmentRatioList))
    stdAvoidCommitmentRatio = np.std(np.array(avoidCommitmentRatioList)) / np.sqrt(specialTrialNumber - 1)
    print(averageAvoidCommitmentRatio)
    print(stdAvoidCommitmentRatio)
