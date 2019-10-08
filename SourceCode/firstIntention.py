import pandas as pd
import matplotlib.pyplot as plt
import os
import pylab as pl
import numpy as np
from numpy import log

def createAllCertainFormatFileList(filePath,fileFormat):
	filenameList=[os.path.join(filePath,relativeFilename) for relativeFilename in os.listdir(filePath)
		if os.path.isfile(os.path.join(filePath,relativeFilename))
		if os.path.splitext(relativeFilename)[1] in fileFormat]
	return filenameList

def cleanDataFrame(rawDataFrame):
	cleanConditionDataFrame=rawDataFrame[rawDataFrame.condition != "None"]
	cleanBeanEatenDataFrame=cleanConditionDataFrame[cleanConditionDataFrame.beanEaten!=0]
	return cleanBeanEatenDataFrame

def calculateFirstIntentionStep(data):
    goal1Step=float('inf')
    goal2Step=float('inf')
    intentionList=eval(data)
    if 1 in intentionList:
        goal1Step=intentionList.index(1)
    if 2 in intentionList:
        goal2Step=intentionList.index(2)
    firstIntentionStep=min(goal1Step,goal2Step)
    if goal1Step<goal2Step:
        firstIntention=1
    elif goal2Step<goal1Step:
        firstIntention=2
    else:
        firstIntention=0
    return firstIntentionStep+1

if __name__=="__main__":
    resultsPath = os.path.abspath(os.path.join(os.getcwd(),os.pardir )) + '/Results/'
    fileFormat = '.csv'
    resultsFilenameList = createAllCertainFormatFileList(resultsPath, fileFormat)
    resultsDataFrameList = [pd.read_csv(file) for file in resultsFilenameList]
    # resultsDataFrame = pd.concat(resultsDataFrameList,sort=False)
    # trialNumber=resultsDataFrame.shape[0]
    # goal= [resultsDataFrame.iat[i, 12] for i in range(trialNumber) ]
    # firstIntentionStep=[calculateFirstIntentionStep(goalList) for goalList in goal if calculateFirstIntentionStep(goalList)!=float('inf')]
    # averageFirstIntentionStep = np.mean(np.array(firstIntentionStep))
    # print(averageFirstIntentionStep)
    specialTrialIndex = 9
    trialNumber = 10
    resultsDataFrame = pd.concat(resultsDataFrameList, sort=False)
    specialTrialResultsDataFrame = resultsDataFrame.iloc[
        list(range(specialTrialIndex, len(resultsDataFrame), trialNumber))]
    goal = [specialTrialResultsDataFrame.iat[i, 12] for i in range(len(specialTrialResultsDataFrame))]
    firstIntentionStep = [calculateFirstIntentionStep(goalList) for goalList in goal if
                          calculateFirstIntentionStep(goalList) != float('inf')]
    averageFirstIntentionStep = np.mean(np.array(firstIntentionStep))
    std=np.std(np.array(firstIntentionStep))*np.sqrt(10)/np.sqrt(9)

    n_groups = 2

    meansBeforeAwayMidlineByNoise = [0.3756378817393345, 0.439613179]
    stdBeforeAwayMidlineByNoise = [0.268591239, 0.187222041]

    meansAfterAwayMidlineByNoise = [0.044776057, 0.016285403]
    stdAfterAwayMidlineByNoise = [0.112354063, 0.0704330924060792]

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, meansBeforeAwayMidlineByNoise, bar_width,
                    alpha=opacity, color='b',
                    yerr=stdBeforeAwayMidlineByNoise, error_kw=error_config,
                    label='beforeAwayMidlineByNoise')

    rects2 = ax.bar(index + bar_width, meansAfterAwayMidlineByNoise, bar_width,
                    alpha=opacity, color='r',
                    yerr=stdAfterAwayMidlineByNoise, error_kw=error_config,
                    label='afterAwayMidlineByNoise')

    ax.set_xlabel('participants')
    ax.set_ylabel('ratio')
    ax.set_title('midline states')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('human', 'model'))
    ax.legend()
    plt.ylim(0, 1)

    fig.tight_layout()
    plt.show()







