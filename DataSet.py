# -*- coding: utf-8 -*-

###########################
###########################

# DataSet.py 

###########################
###########################


#########################
# 	IMPORT
#########################


from StockData import *
from StockResume import * 


#########################
# 	CLASSES
#########################


class DataSet(): 
	"""
	blabla
	"""

	def __init__(self, file_list) : 
		"""
		blabla
		"""

		dataset = list()

		#creating the dataset of Data objects
		for fi in file_list : 
			dataset.append(Data(fi))

		for i, _ in enumerate(dataset) :
			dataset[i].extract_file()
			dataset[i].manage_raw_data()
			dataset[i].add_MMA30_MMA50()
			dataset[i].add_price_MMA30()
			dataset[i].add_KPI()
			dataset[i].add_volatility()
			dataset[i].reduce_data()

		self.object_list = dataset
		self.size = len(self.object_list)


	def add_summary(self): 
		self.summary = Data(file="Mean", source="None")
		self.summary.reduce_data()

		for obj in self.object_list : 
			for i,j in obj.KPI.items() : 
				if i in list(self.summary.KPI.keys()) : self.summary.KPI[i] +=j
				else : self.summary.KPI[i] = j
              
		for i, j in self.summary.KPI.items(): 
			self.summary.KPI[i] = round(j/self.size, DECIMAL_LEVEL)
               

		for obj in self.object_list : 
			for i,j in obj.volatility.items() : 
				if i in list(self.summary.volatility.keys()) : self.summary.volatility[i] +=j
				else : self.summary.volatility[i] = j

		for i, j in self.summary.volatility.items(): 
			self.summary.volatility[i] = round(j/self.size ,DECIMAL_LEVEL)

		self.summary.name = "Mean"


	def __repr__(self) : 
		"""
		blabla
		"""

		string = "objet : {}, \nsize : {}, \nKPI : {}, \nvolatility : {} ".format(
			self.name, self.size, self.KPI, self.volatility)
		return string


	def __str__(self) : 
		"""
		blabla
		"""

		string = "objet : {}, \nsize : {}, \nKPI : {}, \nvolatility : {} \n".format(
			self.name, self.size, self.KPI, self.volatility)
		return string



#########################
# 	MAIN
#########################



if __name__ == '__main__':

  pass
