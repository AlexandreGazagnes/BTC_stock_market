# -*- coding: utf-8 -*-

##########################
##########################

# StockResume.py 

##########################
##########################

#########################
# 	SUMMARY
#########################

#########################
# 	IMPORT
#########################

from StockData import *


#########################
# 	VAR & CONST
#########################

#########################
# 	CLASSES
#########################
		
class StockResume: 

	def __init__(self, data, *keep_other_info_list):
		"""
		blabla
		""" 

		self.name = data.name
		# self.source = data.source 
		self.info = dict()
		self.info["size"]= data.size
		self.info["start_date"] = data.start_date
		self.info["end_date"] = data.end_date
		self.info["periodicity"] = data.periodicity

		self.KPI = data.KPI
		self.price_volatility = data.price_volatility
		self.volume_volatility = data.volume_volatility

		if keep_other_info_list : 
			self.val_data {str(i) : data.val_data[str(i)] for i in keep_other_info_list}


	def __repr__(self) :
		"""
		blablabla
		""" 
		text = """name : {}
info : {}
KPI : {}
price volatility : {}
volume volatility : {}""".format(
self.name, self.info, self.KPI, self.price_volatility,
self.volume_volatility)
		return text

#########################
# 	FUNCTIONS
#########################

#########################
# 	MAIN
#########################

if __name__ == '__main__':

	data = StockData(file=DEFAULT_FILENAME)
	data.upgrade()
	data2 = StockResume(data)

	data3 = StockData(file="AC.csv", directory= "/home/alex/stock_exchange_project/v1.1.1/Quotes/CAC40")
	data3.upgrade()
	data4 = StockResume(data3)
