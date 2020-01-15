import pandas as pd
import os
import glob
DIRNAME = os.path.dirname(__file__)
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from scipy.stats import ttest_ind
from dataAnalysis import *

if __name__ == '__main__':
    resultsPath = os.path.join(os.path.join(DIRNAME, '..'), 'results')
    statsList = []
<<<<<<< HEAD
    stdList = []
    # participants = ['human', 'softmaxBeta2.5', 'goalModelWithPrior5softmaxBeta2.5', 'goalModelWithPriorThreshsoftmaxBeta2.5']
    participants = ['human', 'softmaxBeta2.5', 'commitBeta0.01', 'commitBeta0.03', 'commitBeta0.05', 'commitBeta0.07']
=======
    stdList= []
    participants = ['human', 'maxModel']
>>>>>>> 12aa17872c23798b4d816a7688f003cd50aa8693
    for participant in participants:
        dataPath = os.path.join(resultsPath, participant)
        df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(dataPath, '*.csv'))), sort=False)
        # df.to_csv("all.csv")

        # print(df.head(6))
        nubOfSubj = len(df["name"].unique())
        statDF = pd.DataFrame()
        print('participant', participant, nubOfSubj)

        df["firstIntentionConsistFinalGoal"] = df.apply(lambda x: calculateFirstIntentionConsistency(eval(x['goal'])), axis=1)
        dfNormailTrail = df[df['noiseNumber'] != 'special']
        dfSpecialTrail = df[df['noiseNumber'] == 'special']

        statDF['firstIntentionConsistFinalGoalNormal'] = dfNormailTrail.groupby('name')["firstIntentionConsistFinalGoal"].mean()
        statDF['firstIntentionConsistFinalGoalSpecail'] = dfSpecialTrail.groupby('name')["firstIntentionConsistFinalGoal"].mean()

       # statDF.to_csv("statDF.csv")
        print('firstIntentionConsistFinalGoalNormal', np.mean(statDF['firstIntentionConsistFinalGoalNormal']))
        print('firstIntentionConsistFinalGoalSpecail', np.mean(statDF['firstIntentionConsistFinalGoalSpecail']))
        print('')

        statsList.append([np.mean(statDF['firstIntentionConsistFinalGoalNormal']), np.mean(statDF['firstIntentionConsistFinalGoalSpecail'])])
<<<<<<< HEAD
        stdList.append([calculateSE(statDF['firstIntentionConsistFinalGoalNormal']), calculateSE(statDF['firstIntentionConsistFinalGoalSpecail'])])
=======
        stdList.append([calculateSE(statDF['firstIntentionConsistFinalGoalNormal']),calculateSE(statDF['firstIntentionConsistFinalGoalSpecail'])])
>>>>>>> 12aa17872c23798b4d816a7688f003cd50aa8693

    xlabels = ['normalTrial', 'specialTrail']
    lables = participants
    x = np.arange(len(xlabels))
<<<<<<< HEAD
    totalWidth, n = 0.6, len(participants)
    width = totalWidth / n
    x = x - (totalWidth - width) / 2
    for i in range(len(statsList)):
        plt.bar(x + width * i, statsList[i], yerr=stdList[i], width=width, label=lables[i])
=======
    totalWidth, n = 0.6, len(xlabels)
    width = totalWidth / n
    x = x - (totalWidth - width) / 2
    for i in range(len(statsList)):
        plt.bar(x + width * i, statsList[i],yerr=stdList[i], width=width, label=lables[i])
>>>>>>> 12aa17872c23798b4d816a7688f003cd50aa8693
    plt.xticks(x, xlabels)

    plt.ylim((0, 1))
    plt.legend(loc='best')
    plt.title('commit to goal ratio')
    plt.show()
