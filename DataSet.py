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

DEFAULT_FILE_LIST = ['AC.csv', 'ACA.csv', 'AI.csv', 'AIR.csv', 'ATO.csv', 'BN.csv', 
'BNP.csv', 'CA.csv', 'CAP.csv', 'CS.csv', 'DG.csv', 'EI.csv', 'EN.csv', 'ENGI.csv', 
'FP.csv', 'FR.csv', 'FTI.csv', 'GLE.csv', 'KER.csv', 'LHN.csv', 'LR.csv', 'MC.csv', 
'ML.csv', 'MT.csv', 'OR.csv', 'ORA.csv', 'PUB.csv', 'RI.csv', 'RNO.csv', 'SAF.csv',
'SAN.csv', 'SGO.csv', 'SOLB.csv', 'STM.csv', 'SU.csv', 'SW.csv', 'UG.csv', 'UL.csv',
'VIE.csv', 'VIV.csv']


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
		self.mean = dict()


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

		mean_ = dict()
		
		# KPI
		mean_["KPI"] = dict()
		mean_["KPI"]["buy_begin_sell_end"] = 0
		mean_["KPI"]["global_max_possible"] = 0

		for i,j in enumerate(self.object_list) :
			mean_["KPI"]["buy_begin_sell_end"] += j.KPI["buy_begin_sell_end"]
			mean_["KPI"]["global_max_possible"] += j.KPI["global_max_possible"]

		mean_["KPI"]["buy_begin_sell_end"] = round(mean_["KPI"]["buy_begin_sell_end"] / self.size, DECIMAL_LEVEL)
		mean_["KPI"]["global_max_possible"] = round(mean_["KPI"]["global_max_possible"] / self.size, DECIMAL_LEVEL)

		self.mean["KPI"] = mean_["KPI"]	

		# price Volatility
		mean_["price_volatility"] = dict()
		mean_["price_volatility"]["log_volatility"] = 0
		mean_["price_volatility"]["5_days_volatility"] = 0
		mean_["price_volatility"]["min_max"] = 0

		for i,j in enumerate(self.object_list) :
			mean_["price_volatility"]["log_volatility"] += j.price_volatility["log_volatility"]
			mean_["price_volatility"]["5_days_volatility"] += j.price_volatility["5_days_volatility"]
			mean_["price_volatility"]["min_max"] += j.price_volatility["min_max"]

		mean_["price_volatility"]["log_volatility"] = round(mean_["price_volatility"]["log_volatility"] /self.size, DECIMAL_LEVEL)
		mean_["price_volatility"]["5_days_volatility"]  = round(mean_["price_volatility"]["5_days_volatility"] / self.size, DECIMAL_LEVEL)
		mean_["price_volatility"]["min_max"] = round(mean_["price_volatility"]["min_max"] / self.size, DECIMAL_LEVEL)

		self.mean["price_volatility"] = mean_["price_volatility"]


		# volume Volatility
		mean_["volume_volatility"] = dict()
		mean_["volume_volatility"]["log_volatility"] = 0
		mean_["volume_volatility"]["5_days_volatility"] = 0
		mean_["volume_volatility"]["min_max"] = 0

		for i,j in enumerate(self.object_list) :
			mean_["volume_volatility"]["log_volatility"] += j.volume_volatility["log_volatility"]
			mean_["volume_volatility"]["5_days_volatility"] += j.price_volatility["5_days_volatility"]
			mean_["volume_volatility"]["min_max"] += j.price_volatility["min_max"]

		mean_["volume_volatility"]["log_volatility"] = round(mean_["volume_volatility"]["log_volatility"] /self.size, DECIMAL_LEVEL)
		mean_["volume_volatility"]["5_days_volatility"] = round(mean_["volume_volatility"]["5_days_volatility"] / self.size, DECIMAL_LEVEL)
		mean_["volume_volatility"]["min_max"] = round(mean_["volume_volatility"]["min_max"] / self.size, DECIMAL_LEVEL)

		self.mean["volume_volatility"] = mean_["volume_volatility"]


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
    dataset.add_mean()

    datasource = FolderManager()

    dataset2 = DataSet(file_list=datasource.source_files, rep=datasource.source_folder)
    dataset2.add_mean()
