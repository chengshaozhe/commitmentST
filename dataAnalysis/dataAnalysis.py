import numpy as np

def calculateSE(data):
    standardError = np.std(data) / np.sqrt(len(data) - 1)
    return standardError

def calculateGridDis(grid1, grid2):
    gridDis = np.linalg.norm(np.array(grid1) - np.array(grid2), ord=1)
    return gridDis


def creatRect(coor1, coor2):
    vector = np.array(list(zip(coor1, coor2)))
    vector.sort(axis=1)
    rect = [(i, j) for i in range(vector[0][0], vector[0][1] + 1) for j in range(vector[1][0], vector[1][1] + 1)]
    return rect


def calculateAvoidCommitmnetZone(playerGrid, target1, target2):
    dis1 = calculateGridDis(playerGrid, target1)
    dis2 = calculateGridDis(playerGrid, target2)
    if dis1 == dis2:
        rect1 = creatRect(playerGrid, target1)
        rect2 = creatRect(playerGrid, target2)
        avoidCommitmentZone = list(set(rect1).intersection(set(rect2)))
        avoidCommitmentZone.remove(tuple(playerGrid))
    else:
        avoidCommitmentZone = []
    return avoidCommitmentZone


def calculateAvoidCommitmentRatio(trajectory, zone):
    avoidCommitmentSteps = 0
    for step in trajectory:
        if tuple(step) in zone:
            avoidCommitmentSteps += 1
    avoidCommitmentRatio = avoidCommitmentSteps / (len(trajectory) - 1)
    return avoidCommitmentRatio


def calculateFirstOutZoneRatio(trajectory, zone):
    avoidCommitmentPath = list()
    for point in trajectory:
        if tuple(point) not in zone and len(avoidCommitmentPath) != 0:
            break
        if tuple(point) in zone:
            avoidCommitmentPath.append(point)
    avoidCommitmentRatio = len(avoidCommitmentPath) / (len(trajectory) - 1)
    return avoidCommitmentRatio


def calculateFirstIntentionStep(goalList):
    goal1Step = goal2Step = len(goalList)
    if 1 in goalList:
        goal1Step = goalList.index(1) + 1
    if 2 in goalList:
        goal2Step = goalList.index(2) + 1
    firstIntentionStep = min(goal1Step, goal2Step)
    return firstIntentionStep


def calculateFirstIntentionRatio(goalList):
    firstIntentionStep = calculateFirstIntentionStep(goalList)
    firstIntentionRatio = firstIntentionStep / len(goalList)
    return firstIntentionRatio


def calculateFirstIntention(goalList):
    try:
        target1Goal = goalList.index(1)
    except ValueError as e:
        target1Goal = 999
    try:
        target2Goal = goalList.index(2)
    except ValueError as e:
        target2Goal = 999
    if target1Goal < target2Goal:
        firstGoal = 1
    elif target2Goal < target1Goal:
        firstGoal = 2
    else:
        firstGoal = 0
    return firstGoal


def calculateFirstIntentionConsistency(goalList):
    firstGoal = calculateFirstIntention(goalList)
    finalGoal = calculateFirstIntention(list(reversed(goalList)))
    firstIntention = 1 if firstGoal == finalGoal else 0
    return firstIntention
