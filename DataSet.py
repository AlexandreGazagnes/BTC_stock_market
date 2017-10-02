# -*- coding: utf-8 -*-

###########################
###########################

# DataSet.py 

###########################
###########################


#########################
# 	SUMMARY
#########################


#########################
# 	IMPORT
#########################

from StockData import *
from StockResume import *
from FolderManager import * 


#########################
# 	VAR & CONST
#########################

DEFAULT_FILE_LIST = ['AC.csv', 'ACA.csv']
""", 'AI.csv', 'AIR.csv', 'ATO.csv', 'BN.csv', 
'BNP.csv', 'CA.csv', 'CAP.csv', 'CS.csv', 'DG.csv', 'EI.csv', 'EN.csv', 'ENGI.csv', 
'FP.csv', 'FR.csv', 'FTI.csv', 'GLE.csv', 'KER.csv', 'LHN.csv', 'LR.csv', 'MC.csv', 
'ML.csv', 'MT.csv', 'OR.csv', 'ORA.csv', 'PUB.csv', 'RI.csv', 'RNO.csv', 'SAF.csv',
'SAN.csv', 'SGO.csv', 'SOLB.csv', 'STM.csv', 'SU.csv', 'SW.csv', 'UG.csv', 'UL.csv',
'VIE.csv', 'VIV.csv']
"""

DEFAULT_REP = "/home/alex/stock_exchange_project/v1.1.1/Quotes/CAC40"


#########################
# 	CLASSES
#########################

class DataSet(): 
	"""
	blabla
	"""

	def __init__(self, file_list=DEFAULT_FILE_LIST, rep=DEFAULT_REP) : 
		"""
		blabla
		"""

		dataset = list()

		#creating the dataset of Data objects
		for fi in file_list : 
			dataset.append(StockData(fi, rep))

		for i, _ in enumerate(dataset) :
			dataset[i].upgrade()

		self.object_list = dataset
		self.size = len(self.object_list)
		
		self.add_mean()


	def resume_stock(self):
		"""
		blabla
		"""

		for i, _ in enumerate(self.object_list) :
			self.object_list[i] = StockResume(self.object_list[i])


	def add_mean(self) : 
		"""
		blabla
		"""

		# KPI_
		self.KPI = {elem : 0 for elem in self.object_list[0].KPI.keys()}
		for elem in self.KPI.keys() : 
			for i,j in enumerate(self.object_list) : self.KPI[elem] += j.KPI[elem]
		for elem in self.KPI.keys() : self.KPI[elem] = round(self.KPI[elem] / self.size, DECIMAL_LEVEL)

		# price Volatility
		self.price_volatility = {elem : 0 for elem in self.object_list[0].price_volatility.keys()}
		for elem in self.price_volatility.keys() : 
			for i,j in enumerate(self.object_list) : self.price_volatility[elem] += j.price_volatility[elem]
		for elem in self.price_volatility.keys() : self.price_volatility[elem] = round(self.price_volatility[elem] /self.size, DECIMAL_LEVEL)

		# volume Volatility
		self.volume_volatility = {elem : 0 for elem in self.object_list[0].volume_volatility.keys()}
		for elem in self.volume_volatility.keys() : 
			for i,j in enumerate(self.object_list) : self.volume_volatility[elem] += j.volume_volatility[elem]
		for elem in self.volume_volatility.keys() : self.volume_volatility[elem] = round(self.volume_volatility[elem] /self.size, DECIMAL_LEVEL)



	def __repr__(self) : 
		"""
		blabla
		"""

		string = "objet : {}, \nsize : {}, \nKPI : {}, \nvolatility : {} ".format(
			self.name, self.size, self.KPI, self.volatility)
		return string


#########################
# 	FUNCTIONS
#########################


#########################
# 	MAIN
#########################


if __name__ == '__main__':
    
    dataset = DataSet()
    dataset.resume_stock()

    datasource = FolderManager()
    dataset2 = DataSet(file_list=datasource.source_files, rep=datasource.source_folder)
