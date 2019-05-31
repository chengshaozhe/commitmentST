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


	def __call__(self):
		pause = True
		while pause:
			pg.time.wait(10)
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					pause = False
				elif event.type == pg.QUIT:
					pg.quit()
			pg.time.wait(10)



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

