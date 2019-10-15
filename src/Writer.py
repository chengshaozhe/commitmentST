import pandas as pd 
import os 

class WriteDataFrameToCSV():
	def __init__(self,saveResultFile):
		self.saveResultFile=saveResultFile
	def __call__(self,responseDF):
		if not os.path.isfile(self.saveResultFile):
			responseDF.to_csv(self.saveResultFile, header=list(responseDF.columns))
		else:
			responseDF.to_csv(self.saveResultFile, mode='a', header=False)