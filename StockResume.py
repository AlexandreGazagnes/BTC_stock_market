# -*- coding: utf-8 -*-

##########################
##########################

# StockResume.py 

##########################
##########################


#########################
# 	IMPORT
#########################

from StockData import *


#########################
# 	CLASSES
#########################

		
class StockResume: 

	def __init__(self, data): 

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
# 	MAIN
#########################

if __name__ == '__main__':

	data = StockData(file=DEFAULT_FILENAME)
	data.upgrade()
	data2 = StockResume(data)
