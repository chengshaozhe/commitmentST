import pandas as pd
import os
import glob
DIRNAME = os.path.dirname(__file__)
import matplotlib.pyplot as plt
# matplotlib.style.use('ggplot')
import numpy as np
from scipy.stats import ttest_ind


def calculateFirstIntentionMatchFinalIntention(intentionList):
    intentionList = eval(intentionList)
    firstGoal = calculateFirstIntention(intentionList)
    finalGoal = calculateFirstIntention(list(reversed(intentionList)))
    firstIntention = 1 if firstGoal == finalGoal else 0
    return firstIntention


def calculateFirstIntention(intentionList):
    try:
        target1Goal = intentionList.index(1)
    except ValueError as e:
        target1Goal = 999
    try:
        target2Goal = intentionList.index(2)
    except ValueError as e:
        target2Goal = 999
    if target1Goal < target2Goal:
        firstGoal = 1
    elif target2Goal < target1Goal:
        firstGoal = 2
    else:
        firstGoal = 0
    return firstGoal


if __name__ == '__main__':
    dataPath = os.path.join(os.path.join(DIRNAME, '..'), 'results/maxModel')
    df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(dataPath, '*.csv'))), sort=False)
    # df.to_csv("all.csv")

    # print(df.head(6))
    nubOfSubj = len(df["name"].unique())
    statDF = pd.DataFrame()
    print(nubOfSubj)

    df["firstIntentionConsistFinalGoal"] = df.apply(lambda x: calculateFirstIntentionMatchFinalIntention(x['goal']), axis=1)
    dfNormailTrail = df[df['noiseNumber'] != 'special']
    dfSpecialTrail = df[df['noiseNumber'] == 'special']
    df.to_csv("statDF.csv")
    statDF['firstIntentionConsistFinalGoalNormal'] = dfNormailTrail.groupby('name')["firstIntentionConsistFinalGoal"].mean()
    statDF['firstIntentionConsistFinalGoalSpecail'] = dfSpecialTrail.groupby('name')["firstIntentionConsistFinalGoal"].mean()
    print('normal mean', np.mean(statDF['firstIntentionConsistFinalGoalNormal']))
    print('special mean', np.mean(statDF['firstIntentionConsistFinalGoalSpecail']))

    consistNormal = np.mean(statDF['firstIntentionConsistFinalGoalNormal'])
    consistSpecial = np.mean(statDF['firstIntentionConsistFinalGoalSpecail'])

    frequency = [consistSpecial, 1 - consistSpecial]
    names = ['consist', 'inconsist']
    plt.bar([0, 0.3], frequency, width=0.1)
    plt.xticks([0, 0.3], names)
    plt.xlabel('Consist And Inconsist')
    plt.ylabel('frequency')
    plt.ylim((0, 1))
    plt.title('firstIntentionPredictFinalGoal NormalTrial')
    plt.show()
