import numpy as np
import pygame as pg
import random
import Visualization


def inferGoal(trajectory, aimedGrid, targetGridA, targetGridB):
	pacmanBean1AimedDisplacement = np.linalg.norm(np.array(targetGridA) - np.array(aimedGrid), ord=1)
	pacmanBean2AimedDisplacement =  np.linalg.norm(np.array(targetGridB) - np.array(aimedGrid), ord=1)
	pacmanBean1LastStepDisplacement =  np.linalg.norm(np.array(targetGridA) - np.array(trajectory[-1]), ord=1)
	pacmanBean2LastStepDisplacement =  np.linalg.norm(np.array(targetGridB) - np.array(trajectory[-1]), ord=1)
	# print(pacmanBean1AimedDisplacement,pacmanBean2AimedDisplacement,pacmanBean1LastStepDisplacement,pacmanBean2LastStepDisplacement)
	# print(trajectory,aimedGrid)
	bean1Goal = pacmanBean1LastStepDisplacement - pacmanBean1AimedDisplacement
	bean2Goal = pacmanBean2LastStepDisplacement - pacmanBean2AimedDisplacement
	if bean1Goal > bean2Goal:
		goal = 1
	elif bean1Goal < bean2Goal:
		goal = 2
	else:
		goal = 0
	return goal

def countCertainNumberInList(listToManipulate, certainNumber):
	count = 0
	indexList=[]
	for number in listToManipulate:
		if certainNumber == number:
			count = count + 1
			indexList.append(certainNumber)
	return count,indexList



class HumanController():
	def __init__(self,gridSize,drawNewState):
		self.actionDict={pg.K_UP:[0,-1], pg.K_DOWN:[0,1], pg.K_LEFT:[-1,0], pg.K_RIGHT:[1,0]}
		self.gridSize=gridSize
		self.drawNewState=drawNewState



	def addNoise(self,targetGridA,targetGridB,playerGrid,trajectory,event,goalList, \
							   noiseStep,firstIntentionFlag,firstIntentionMidlineFlag,stepCount,designValues):
		aimedAction=self.actionDict[event.key]
		goal=0
		if designValues!="special" :
			if stepCount in noiseStep :
				while True:
					actionSpace=self.actionDict.copy()
					actionSpace.pop(event.key)
					actionList = [str(action) for action in actionSpace.values()]
					actionStr=np.random.choice(actionList)
					realAction=eval(actionStr)
					if np.all(np.add(playerGrid, realAction) >= 0) and \
							np.all(np.add(playerGrid, realAction) < self.gridSize):
						break
			else:
				realAction=self.actionDict[event.key]
		else:
			aimedGrid=np.add(playerGrid,aimedAction)
			goal=inferGoal(trajectory, aimedGrid, targetGridA, targetGridB)
			goalList.append(goal)
			if goal != 0 and not firstIntentionFlag and not firstIntentionMidlineFlag:
				noiseStep.append(stepCount)
				goalList.append(goal)
				firstIntentionFlag=True
				allPosiibileplayerGrid = [np.add(playerGrid, action) for action in self.actionDict.values()]
				if goal == 1 :
					allPossibleDistance=[[np.linalg.norm(np.array(targetGridB) - np.array(possibleGrid), ord=1),possibleGrid] for possibleGrid in allPosiibileplayerGrid]
				else :
					allPossibleDistance=[[np.linalg.norm(np.array(targetGridA) - np.array(possibleGrid), ord=1),possibleGrid] for possibleGrid in allPosiibileplayerGrid]
				orderedAllPossibleDistanceAndGrid = sorted(allPossibleDistance, key=lambda x: x[0])
				orderedAllPossibleDistance = [distance[0] for distance in orderedAllPossibleDistanceAndGrid]
				count, indexList = countCertainNumberInList(orderedAllPossibleDistance,
																 orderedAllPossibleDistance[0])
				minIndex = int(count - 1)
				realAction =list( np.array(orderedAllPossibleDistanceAndGrid[random.randint(0, minIndex)][1])-np.array(playerGrid))
				if np.linalg.norm(np.array(targetGridB) - np.array(playerGrid), ord=1)==np.linalg.norm(np.array(targetGridA) - np.array(playerGrid), ord=1):
					firstIntentionMidlineFlag=True
			else:
				realAction=self.actionDict[event.key]
		return realAction,aimedAction,goalList,firstIntentionFlag,firstIntentionMidlineFlag,noiseStep

	def __call__(self,targetGridA,targetGridB,playerGrid,playerTrajectory,noiseStep,stepCount,\
				 firstIntentionFlag,firstIntentionMidlineFlag,goalList,designValues):
		pause=True
		self.drawNewState(targetGridA,targetGridB,playerGrid)
		realAction=[0,0]
		aimedAction=[0,0]
		while pause:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN:
					if event.key in self.actionDict.keys() and \
							np.all(np.add(playerGrid, self.actionDict[event.key]) >= 0) and \
							np.all(np.add(playerGrid, self.actionDict[event.key]) < self.gridSize) :
						stepCount=stepCount+1
						realAction, aimedAction, goalList, firstIntentionFlag, firstIntentionMidlineFlag,noiseStep=\
							self.addNoise(targetGridA, targetGridB,playerGrid,  playerTrajectory,event,goalList, \
														noiseStep,firstIntentionFlag, firstIntentionMidlineFlag, stepCount,designValues)
						pause=False
			playerGrid=np.add(playerGrid, realAction)
			self.drawNewState(targetGridA, targetGridB, playerGrid)
		return playerGrid,realAction, aimedAction, goalList,firstIntentionFlag, firstIntentionMidlineFlag,stepCount,noiseStep



class ModelController():
	def __init__(self,policy,gridSize,stopwatchEvent,stopwatchUnit,drawNewState,finishTime):
		self.policy=policy
		self.gridSize=gridSize
		self.stopwatchEvent=stopwatchEvent
		self.stopwatchUnit=stopwatchUnit
		self.stopwatch=0
		self.drawNewState=drawNewState
		self.finishTime=finishTime
	def __call__(self,targetGridA,targetGridB,playerGrid,currentScore,currentStopwatch):
		pause=True
		newStopwatch = currentStopwatch
		remainningTime=max(0,self.finishTime-currentStopwatch)
		self.drawNewState(targetGridA,targetGridB,playerGrid,remainningTime,currentScore)
		while pause:
			targetStates = (tuple(targetGridA),tuple(targetGridB))
			if targetStates not in self.policy.keys():
				targetStates = (tuple(targetGridB),tuple(targetGridA))
			policyForCurrentStateDict=self.policy[targetStates][tuple(playerGrid)]
			actionMaxList = [action for action in policyForCurrentStateDict.keys() if policyForCurrentStateDict[action]==np.max(list(policyForCurrentStateDict.values()))]
			action = random.choice(actionMaxList)
			playerNextPosition=np.add(playerGrid,action)
			if np.any(playerNextPosition<0) or np.any(playerNextPosition>=self.gridSize):
				playerNextPosition=playerGrid
			pause=False
			for event in pg.event.get():
				if event.type == self.stopwatchEvent:
					newStopwatch=newStopwatch+self.stopwatchUnit
					remainningTime=max(0,self.finishTime - newStopwatch)
			self.drawNewState(targetGridA,targetGridB,playerNextPosition,remainningTime,currentScore)
			pg.display.flip()
		return playerNextPosition,action,newStopwatch

if __name__=="__main__":
	pg.init()
	screenWidth=720
	screenHeight=720
	screen=pg.display.set_mode((screenWidth,screenHeight))
	gridSize=20
	leaveEdgeSpace=2
	lineWidth=2
	backgroundColor=[188,188,0]
	lineColor=[255,255,255]
	targetColor=[255,50,50]
	playerColor=[50,50,255]
	targetRadius=10
	playerRadius=10
	targetGridA=[5,5]
	targetGridB=[15,5]
	playerGrid=[10,15]
	currentScore=5
	textColorTuple=(255,50,50)
	stopwatchEvent = pg.USEREVENT + 1
	stopwatchUnit=10
	pg.time.set_timer(stopwatchEvent, stopwatchUnit)
	finishTime=90000
	currentStopwatch=32000

	drawBackground=Visualization.DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState=Visualization.DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)

	getHumanAction = HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
	import pickle
	policy=pickle.load(open("SingleWolfTwoSheepsGrid15.pkl","rb"))
	getModelAction = ModelController(policy, gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)

	# [playerNextPosition,action,newStopwatch]=getHumanAction(targetGridA, targetGridB, playerGrid, currentScore, currentStopwatch)
	[playerNextPosition,action,newStopwatch]=getModelAction(targetGridA, targetGridB, playerGrid, currentScore, currentStopwatch)
	print(playerNextPosition,action,newStopwatch)

	pg.quit()

