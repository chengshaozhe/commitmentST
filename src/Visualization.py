import pygame as pg
import numpy as np
import os


class DrawBackground():
	def __init__(self,screen,gridSize,leaveEdgeSpace,backgroundColor,lineColor,lineWidth,textColorTuple):
		self.screen=screen
		self.gridSize=gridSize
		self.leaveEdgeSpace=leaveEdgeSpace
		self.widthLineStepSpace=np.int(screen.get_width()/(gridSize+2*self.leaveEdgeSpace))
		self.heightLineStepSpace=np.int(screen.get_height()/(gridSize+2*self.leaveEdgeSpace))
		self.backgroundColor=backgroundColor
		self.lineColor=lineColor
		self.lineWidth=lineWidth
		self.textColorTuple=textColorTuple
	def __call__(self):
		self.screen.fill((0,0,0))
		pg.draw.rect(self.screen,self.backgroundColor,pg.Rect(np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace),
			np.int(self.gridSize*self.widthLineStepSpace),np.int(self.gridSize*self.heightLineStepSpace)))
		for i in range(self.gridSize+1):
			pg.draw.line(self.screen, self.lineColor, [np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace)],
				[np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((self.gridSize+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
			pg.draw.line(self.screen, self.lineColor, [np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)],
				[np.int((self.gridSize+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
		return

class DrawNewState():
	def __init__(self,screen,drawBackground,targetColor,playerColor,targetRadius,playerRadius):
		self.screen=screen
		self.drawBackground=drawBackground
		self.targetColor=targetColor
		self.playerColor=playerColor
		self.targetRadius=targetRadius
		self.playerRadius=playerRadius
		self.leaveEdgeSpace=drawBackground.leaveEdgeSpace
		self.widthLineStepSpace=drawBackground.widthLineStepSpace
		self.heightLineStepSpace=drawBackground.heightLineStepSpace

	def __call__(self,targetPositionA,targetPositionB,playerPosition):
		self.drawBackground()
		pg.draw.rect(self.screen, self.targetColor, [np.int((targetPositionA[0]+self.leaveEdgeSpace+0.2)*self.widthLineStepSpace),
			np.int((targetPositionA[1]+self.leaveEdgeSpace+0.2)*self.heightLineStepSpace),self.targetRadius*2,self.targetRadius*2])
		pg.draw.rect(self.screen, self.targetColor, [np.int((targetPositionB[0]+self.leaveEdgeSpace+0.2)*self.widthLineStepSpace),
			np.int((targetPositionB[1]+self.leaveEdgeSpace+0.2)*self.heightLineStepSpace),self.targetRadius*2,self.targetRadius*2])
		pg.draw.circle(self.screen, self.playerColor, [np.int((playerPosition[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((playerPosition[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)],self.playerRadius)
		# pg.draw.circle(self.screen, self.playerColor,
		# 			   [np.int(playerPosition[0] ),
		# 				np.int(playerPosition[1])],self.playerRadius)
		pg.display.flip()
		return

class DrawImage():
	def __init__(self,screen):
		self.screen=screen
		self.screenCenter=(self.screen.get_width()/2,self.screen.get_height()/2)

	def __call__(self,image):
		imageRect=image.get_rect()
		imageRect.center=self.screenCenter
		pause=True
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT])
		self.screen.fill((0, 0, 0))
		self.screen.blit(image, imageRect)
		pg.display.flip()
		while pause:
			pg.time.wait(10)
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					pause = False
				elif event.type == pg.QUIT:
					pg.quit()
			pg.time.wait(10)
		pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP,pg.QUIT])


class DrawText():
	def __init__(self,screen,drawBackground):
		self.screen=screen
		self.screenCenter=(self.screen.get_width()/2,self.screen.get_height()/2)
		self.drawBackground=drawBackground
		self.leaveEdgeSpace = drawBackground.leaveEdgeSpace
		self.widthLineStepSpace = drawBackground.widthLineStepSpace
		self.heightLineStepSpace = drawBackground.heightLineStepSpace

	def __call__(self,text,textColorTuple,textPositionTuple):
		self.drawBackground()
		font = pg.font.Font(None, 50)
		textObj = font.render(text, 1, textColorTuple)
		self.screen.blit(textObj, [np.int((textPositionTuple[0]+self.leaveEdgeSpace+0.2)*self.widthLineStepSpace),
			np.int((textPositionTuple[1]+self.leaveEdgeSpace-0.1)*self.heightLineStepSpace)])
		pg.display.flip()
		return


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
	targetPositionA=[5,5]
	targetPositionB=[15,5]
	playerPosition=[10,15]
	picturePath=os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/Pictures/'
	restImage=pg.image.load(picturePath+'rest.png')
	currentTime=138456
	currentScore=5
	textColorTuple=(255,50,50)
	drawBackground=DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState=DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	drawImage=DrawImage(screen)
	drawBackground(currentTime, currentScore)
	pg.time.wait(5000)
	pg.quit()


