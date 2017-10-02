# -*- coding: utf-8 -*-

##########################
##########################

# Broker.py 

##########################
##########################


#########################
# 	SUMMARY
#########################


#########################
# 	IMPORT
#########################


#########################
# 	VAR & CONST
#########################

KRAKEN_FEES = round(0.16/100, DECIMAL_LEVEL)
FORTUNEO_FEES = round(0.2/100, DECIMAL_LEVEL)
ING_FEES = round(0.26/100, DECIMAL_LEVEL) #ideal = ordre de 5_999€ -> 0.13%


#########################
# 	CLASSES
#########################


class Broker : 
	"""
	blabla
	"""

	def __init__(self, filelist, source_rep, strategy, fees) : 
		"""
		blabla
		"""

		self.filelist = filelist
		self.source_rep = source_rep
		self.strategy = strategy
		self.fees = fees
		self.buy_condition, self.buy_value, self.sell_condition self.sell_value = \
			strategy[0], strategy[1],strategy[3],strategy[4]
		self.capital = 100
		self.volume = 0


		for stock in self.filelist : 
			self.trade(stock)

		self.add_KPI()



	def trade(stock) : 
		"""
		blabla
		"""

		for info in stock.val_data.values() : 
			if info == buy_condition : 
				for i, val in enumerate(stock.val_data[info]) :
					if val ==  self.buy_value : 
						self.buy(stock.val_data["Price"])
					if val == self.buy_value : 
						self.sell(stock.val_data["Price"])


	def buy(self, price) :
		"""
		blabla
		"""

		self.volume = self.capital / price
		fees = self.volume * price * self.fees
		self.capital -= fees
		self.volume = self.capital / price
		self.capital = 0


	def sell(self, price) :
		"""
		blabla
		"""

		self.capital = self.volume * price
		self.capital -= self.volume * price * self.fees
		self.volume = 0 


	def add_KPI(self):
		"""
		blabla
		"""

		if self.capital > 100 : 
			self.KPI = round(1 + ((self.capital-100) /100),DECIMAL_LEVEL)
		else : self.KPI = round(1 - ((100-self.capital)/100),DECIMAL_LEVEL)



#########################
# 	FUNCTIONS
#########################


#########################
# 	MAIN
#########################

datasource = FolderManager()

buy_begin_sell_end = ("Date",start_date,"Date",end_date)

Alex = Broker(filelist=['AC.csv', 'ACA.csv'], source_rep=datasource.source_folder,
	strategy=buy_begin_sell_end,fees=FORTUNEO_FEES )
