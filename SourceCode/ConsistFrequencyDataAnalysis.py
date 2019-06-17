import pandas as pd
import matplotlib.pyplot as plt
import os
import pylab as pl
import numpy as np
from scipy import stats,optimize
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.optimize import curve_fit
from scipy import log
import matplotlib.pyplot as plt
from collections import Counter
from pandas import Series

def createAllCertainFormatFileList(filePath,fileFormat):
	filenameList=[os.path.join(filePath,relativeFilename) for relativeFilename in os.listdir(filePath)
		if os.path.isfile(os.path.join(filePath,relativeFilename))
		if os.path.splitext(relativeFilename)[1] in fileFormat]
	return filenameList

def calculateFirstIntentionMatchFinalIntention(intentionList):
    firstGoal=calculateFirstIntention(intentionList)
    finalGoal=calculateFirstIntention(list(reversed(intentionList)))
    firstIntention="consist"if firstGoal==finalGoal else "inconsist"
    return firstIntention

def calculateFirstIntention(intentionList):
    try:
        target1Goal=intentionList.index(1)
    except ValueError as e:
        target1Goal=999
    try:
        target2Goal=intentionList.index(2)
    except ValueError as e:
        target2Goal=999
    if target1Goal<target2Goal:
        firstGoal=1
    elif target2Goal<target1Goal:
        firstGoal=2
    else:
        firstGoal=0
    return firstGoal

if __name__=="__main__":
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
    fileFormat = '.csv'
    resultsFilenameList = createAllCertainFormatFileList(resultsPath, fileFormat)
    resultsDataFrameList = [pd.read_csv(file) for file in resultsFilenameList]
    specialTrialIndex=9
    trialNumber=10
    resultsDataFrame = pd.concat(resultsDataFrameList,sort=False)
    specialTrialResultsDataFrame =resultsDataFrame.iloc[list(range(specialTrialIndex,len(resultsDataFrame),trialNumber))]
    print(specialTrialResultsDataFrame,resultsDataFrame)
    goal = [eval(specialTrialResultsDataFrame.iat[i, 12]) for i in range(len(specialTrialResultsDataFrame)) ]
    firstGoalConsistFinalGoal=[calculateFirstIntentionMatchFinalIntention(supriseTrialGoal)  for supriseTrialGoal in goal]
    consistAndInconsistCount = dict(Counter(firstGoalConsistFinalGoal) )
    print(consistAndInconsistCount)
    names=['consist','inconsist']
    if "consist" not in consistAndInconsistCount.keys():
        consistAndInconsistCount["consist"]=0
    if "inconsist" not in consistAndInconsistCount.keys():
        consistAndInconsistCount["inconsist"]=0
    frequency=(np.array([consistAndInconsistCount['consist'],consistAndInconsistCount['inconsist']])/len(goal))
    plt.bar([0,0.3],frequency,width=0.1)
    plt.xticks([0,0.3], names)
    plt.xlabel('Consist And Inconsist')
    plt.ylabel('frequency')
    plt.title('firstIntentionPredictFinalGoal')
    plt.show()