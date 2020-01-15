import pandas as pd
import os
import glob
DIRNAME = os.path.dirname(__file__)
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from scipy.stats import ttest_ind
from collections import Counter
from dataAnalysis import *


if __name__ == '__main__':
    resultsPath = os.path.join(os.path.join(DIRNAME, '..'), 'results')
    statsList = []
    stdList = []
<<<<<<< HEAD
    participants = ['human','softmaxBeta1','softmaxBeta2.5','max']
=======
    participants = ['human', 'maxModel']
>>>>>>> 12aa17872c23798b4d816a7688f003cd50aa8693
    for participant in participants:
        dataPath = os.path.join(resultsPath, participant)
        df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(dataPath, '*.csv'))), sort=False)
        statDF = pd.DataFrame()

        # df.to_csv("all.csv")
        # print(df.head(6))

        df['avoidCommitmentZone'] = df.apply(lambda x: calculateAvoidCommitmnetZone([x['playerGridX'], x['playerGridY']], [x['bean1GridX'], x['bean1GridY']], [x['bean2GridX'], x['bean2GridY']]), axis=1)

        df['avoidCommitmentRatio'] = df.apply(lambda x: calculateAvoidCommitmentRatio(eval(x['trajectory']), x['avoidCommitmentZone']), axis=1)
        statDF['avoidCommitmentRatio'] = df.groupby('name')["avoidCommitmentRatio"].mean()

        df['firstIntentionRatio'] = df.apply(lambda x: calculateFirstIntentionRatio(eval(x['goal'])), axis=1)
        statDF['firstIntentionRatio'] = df.groupby('name')["firstIntentionRatio"].mean()

        # df.to_csv("all.csv")
        nubOfSubj = len(df["name"].unique())
        print(nubOfSubj)
        print('avoidCommitmentRatio', np.mean(statDF['avoidCommitmentRatio']))
        print('firstIntentionRatio', np.mean(statDF['firstIntentionRatio']))

        statsList.append([np.mean(statDF['firstIntentionRatio']), np.mean(statDF['avoidCommitmentRatio'])])
        stdList.append([calculateSE(statDF['firstIntentionRatio']),calculateSE(statDF['avoidCommitmentRatio'])])

    xlabels = ['firstIntentionRatio', 'avoidCommitmentRatio']
    labels = participants
    x = np.arange(len(xlabels))
<<<<<<< HEAD
    totalWidth, n = 0.6, len(participants)
=======
    totalWidth, n = 0.6, len(xlabels)
>>>>>>> 12aa17872c23798b4d816a7688f003cd50aa8693
    width = totalWidth / n
    x = x - (totalWidth - width) / 2
    for i in range(len(statsList)):
        plt.bar(x + width * i, statsList[i],yerr =stdList[i] , width=width, label=labels[i])
    plt.xticks(x, xlabels)

    # plt.bar([0, 0.3], avoidCommitmentRatioList, width=0.1)
    # plt.xticks([0, 0.3], participants)
    # plt.ylabel('frequency')
    plt.ylim((0, 1))
    plt.legend(loc='best')
    plt.title('avoidCommitment')
    plt.show()
