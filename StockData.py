	# -*- coding: utf-8 -*-

###########################
###########################

# StockData.py 

###########################
###########################

#########################
# 	SUMMARY
#########################

#########################
# 	IMPORT
#########################

import os
from collections import OrderedDict
from math import sqrt, log


#########################
# 	VAR & CONSTANTS
#########################

DEFAULT_FILENAME = "test.csv" #/home/alex/stock_exchange_project/v1.1.0/Quotes/CAC40.csv" " #"cours_BTC_DOL_01.01.17_13.09.17.csv"
DECIMAL_LEVEL = 4
SEP = ";"
NB_LOCAL_MIN_MAX = 10


#########################
#	CLASSES
#########################

class StockData :
	"""
	class StockData, form a basic file, it represents and manage the stock data
	"""

	def __init__(self, file="test.csv", directory=os.getcwd(), source="abcbourse", 
		file_format="csv"): 
		"""
		init method
		"""

		self.init_directory = os.getcwd()
		self.source_directory = os.getcwd()
		if directory != os.getcwd() : self.source_directory = directory
		self.file = file
		self.file_format = file_format
		
		self.name = str()
		self.source = source
		self.size = 0
		self.start_date = str()
		self.end_date = str()
		self.periodicity = str()

		# --> Manage number days between start and end. 
		# if number/days / self.size = 1.0 => days
		
		self.raw_data = list()
		self.val_data = OrderedDict()

		self.KPI = dict()

		self.price_volatility = dict()
		self.volume_volatility = dict()


	def extract_file(self):
		"""
		extract data from an text file, merge integers and decimals
		val_data if needed and convert basics datas in good type (int for ex)
		create size.data, name and raw data attributes
		"""

		# file manager
		os.chdir(self.source_directory)
		fichier = open(self.file, "r")
		raw_data = fichier.readlines()
		fichier.close()

		# source manager
		if self.source == "abcbourse" : 
			for i,_ in enumerate(raw_data):
				raw_data[i] = raw_data[i].replace("\n","")
				raw_data[i] = raw_data[i].replace(";",",")
				raw_data[i] = raw_data[i].split(",")

			self.size = len(raw_data)
			self.name = raw_data[0][0]

			for i in range(self.size):

				for j in range(2, len(raw_data[i])-2,2): 
					raw_data[i][j] = int(raw_data[i][j]) + (int(raw_data[i][j+1])/100)
				for j in [9,7,5,3,0]: 
					del raw_data[i][j]
				raw_data[i].insert(0, i+1)

			for i in range(self.size): 
				raw_data[i][len(raw_data[i])-1] = int(raw_data[i][len(raw_data[i])-1]) +1

		# implement this later
		elif self.source == "yahoo_finance": 
			raise ValueError
		elif self.source == "Google_finance": 
			raise ValueError
		else : 
			raise ValueError

		self.raw_data = raw_data


	def find_name(self) : 
		"""
		implement later
		"""

		url_google = str("http://www.google.fr/search?q=" + str(self.name))
		web_page = urllib.request.urlopen(url_google)
		html = str(web_page.read())
		start, stop = "Cotation action", "|"
		nb_start, nb_stop = html.find(start), html.find(stop)
		self.name = html[nb_start + len(start) : nb_stop]	


	def manage_raw_data(self):
		"""
		manage raw datas creating an orderdict name val_data, an attribute, with 
		initials datas : Id Date Opening...
		"""

		# creates empty elements of orderdict val_data
		self.val_data["Id"], self.val_data["Date"], self.val_data["Opening"] = list(),list(),list()
		self.val_data["Min"], self.val_data["Max"] = list(),list()
		self.val_data["Price"], self.val_data["Volume"] = list(),list()

		# transfer basics datas from raw_data to val_data orderdict
		titles = ["Id", "Date", "Opening", "Min", "Max", "Price", "Volume"]
		for j, k in enumerate(titles): 
			for i in range(self.size): 
				self.val_data[k].append(self.raw_data[i][j])

		self.start_date = str(self.val_data["Date"][0])
		self.end_date = self.val_data["Date"][self.size-1]


	def add_MMAs(self, MMA1=30, MMA2=50): # what about a dcit (mma1,mma2, mma3...)
		"""
		based intials data in val_data orderdict, create technical idndicarors based on 
		moving mean : MMA30, MMA50, MMA30 VS MMA50, delta_MMA30_MMA50, and MMA30 X MMA50
		"""

		# creates empty elements of orderdict val_data
		str_MMA1 = "MMA" + str(MMA1)
		str_MMA2 = "MMA" + str(MMA2)
		self.val_data[str_MMA1], self.val_data[str_MMA2] = list(), list()

		str_MMA1_vs_MMA2 = str_MMA1 + "_vs_" + str_MMA2
		str_delta_MMA1_MMA2 = "delta_" + str_MMA1 + "_" + str_MMA2
		str_MMA1_X_MMA2 = str_MMA1 + "_X_" + str_MMA2
		self.val_data[str_MMA1_vs_MMA2], self.val_data[str_delta_MMA1_MMA2] = list(), list()
		self.val_data[str_MMA1_X_MMA2] = list()

		# add MMA1 and MMA2		
		for (mma,str_mma) in [(MMA1, str_MMA1), (MMA2, str_MMA2) ] :
			for i in range(self.size): 
				if i<mma-1 : 
					self.val_data[str_mma].append(0)
				elif i >=mma-1 : 
					sub_sum = [self.val_data["Price"][i] for i in range(i, i-mma, -1)]
					self.val_data[str_mma].append(round(sum(sub_sum)/mma,DECIMAL_LEVEL))

		# add MMA1 vs MMA2
		for i in range(self.size): 
			if self.val_data[str_MMA1][i] > self.val_data[str_MMA2][i] and self.val_data[str_MMA1][i] and self.val_data[str_MMA2][i] : 
				self.val_data[str_MMA1_vs_MMA2].append("+")
			elif self.val_data[str_MMA1][i] < self.val_data[str_MMA2][i] and self.val_data[str_MMA1][i] and self.val_data[str_MMA2][i] : 
				self.val_data[str_MMA1_vs_MMA2].append("-")
			elif self.val_data[str_MMA1][i] == self.val_data[str_MMA2][i] and self.val_data[str_MMA1][i] and self.val_data[str_MMA2][i]:
				self.val_data[str_MMA1_vs_MMA2].append("=")
			elif not (self.val_data[str_MMA1][i] and self.val_data[str_MMA2][i]) :
				self.val_data[str_MMA1_vs_MMA2].append("")
			else : 
				raise ValueError

		# add delta MMA1 MMA2
		for i in range(self.size):
			if i < 50 : 
				self.val_data[str_delta_MMA1_MMA2].append(0)
			else:
				self.val_data[str_delta_MMA1_MMA2].append(abs(round(
					(self.val_data[str_MMA1][i] - self.val_data[str_MMA2][i]) / 
					self.val_data[str_MMA2][i],DECIMAL_LEVEL)))

		# add MMA1 X MMA2
		for i in range(self.size): 
			if self.val_data[str_MMA1_vs_MMA2][i] and \
			self.val_data[str_MMA1_vs_MMA2][i] != self.val_data[str_MMA1_vs_MMA2][i-1]:
				self.val_data[str_MMA1_X_MMA2].append(True)
			else : 
				self.val_data[str_MMA1_X_MMA2].append("")


	def add_price_MMA(self, MMA=30):
		"""
		based intials data in val_data orderdict, create technical idndicarors based on 
		moving mean vs price : price VS MMA300, delta_price_MMA30, and price X MMA30
		"""
		"""
		# creates empty elements of orderdict val_data
		str_MMA = "MMA" + str(MMA)

		assert str_MMA in self.val_data.keys()

		str_price_vs_MMA = "price_vs_" + str_MMA
		str_delta_price_MMA = "delta_price_" + str_MMA
		str_price_X_MMA = "str_price_X_" + str_MMA
		self.val_data[str_price_vs_MMA], self.val_data[str_delta_price_MMA], \
		self.val_data[str_price_X_MMA]  = list(), list(), list()

		# add price vs MMA
		for i in range(self.size): 
			if self.val_data["Price"][i] > self.val_data[str_MMA][i] and self.val_data[str_MMA][i] : 
				self.val_data[str_price_vs_MMA].append("+")
			elif self.val_data["Price"][i] < self.val_data[str_MMA][i] and self.val_data[str_MMA][i] : 
				self.val_data[str_price_vs_MMA].append("-")
			elif self.val_data["Price"][i] == self.val_data[str_MMA][i] and self.val_data[str_MMA][i]:
				self.val_data[str_price_vs_MMA].append("=")
			elif not (self.val_data[str_MMA][i]) :
				self.val_data[str_price_vs_MMA].append("")
			else : 
				raise ValueError

		# add delta price MMA
		for i in range(self.size):
			if i<30 : 
				self.val_data[str_delta_price_MMA].append(0)
			else:
				self.val_data[str_delta_price_MMA].append(abs(round(
				(self.val_data["Price"][i] - self.val_data[str_MMA][i]) / self.val_data[str_MMA][i],DECIMAL_LEVEL)))

		# add price X MMA
		self.val_data[str_price_X_MMA].append("") # --> ????
		for i in range(1, self.size): 
			if self.val_data[str_price_X_MMA][i] and \
			self.val_data[str_price_X_MMA][i] != self.val_data[str_price_X_MMA][i-1]:
				self.val_data[str_price_X_MMA].append(True)
			else : 
				self.val_data[str_price_X_MMA].append("")
		"""


	def add_KPI(self):
		"""
		self.KPI is an order dict, each elem of this dict is also a dic with the keys value, buy and sell
		"""

		# dumb indicator : buy the first day, sell the last one
		self.KPI["buy_begin_sell_end"] = round( 1 + ((self.val_data["Price"][self.size - 1] - self.val_data["Price"][0]) / self.val_data["Price"][0]), DECIMAL_LEVEL)
		
		#looks for the smalest global Price and the highest (but after the lower one)
		id_global_min, val_global_min = 0, self.val_data["Price"][0]
		for i,j in enumerate(self.val_data["Price"]) :
			if j < val_global_min : 
				id_global_min, val_global_min = i, j

		id_global_max, val_global_max = 0, self.val_data["Price"][0]
		for i,j in enumerate(self.val_data["Price"]) :
			if j > val_global_max and i > id_global_min : 
				id_global_max, val_global_max = i, j

		self.KPI["global_max_possible"] = round(1 + ((val_global_max - val_global_min) / val_global_min), DECIMAL_LEVEL)

		# buy and sells for NB_LOCAL_MIN_MAX local min/max
		#cf v1.1.0


	def add_price_volatility(self, nb_log_volatility=252):
		"""
		blabla
		"""

		min_ = min(self.val_data["Price"])
		max_ = max(self.val_data["Price"])

		self.price_volatility["min_max"] = round((min_ - max_) / (max_ if min_ > max_ else min_), DECIMAL_LEVEL)
		self.price_volatility["log_volatility"] = round(sqrt((nb_log_volatility/self.size) * (sum([log(self.val_data["Price"][i]/self.val_data["Price"][i-1]) for i in range(1, self.size)]))**2),DECIMAL_LEVEL)
		self.price_volatility["5_days_volatility"] = round(sqrt((1/(self.size/5)) * (sum([log(self.val_data["Price"][i]/self.val_data["Price"][i-1]) for i in range(1, self.size,5)]))**2),DECIMAL_LEVEL)


	def add_volume_volatility(self, nb_log_volatility=252):
		"""
		blabla
		"""

		min_ = min(self.val_data["Volume"])
		max_ = max(self.val_data["Volume"])

		self.volume_volatility["min_max"] = round((min_ - max_) / (max_ if min_ > max_ else min_ ), DECIMAL_LEVEL)
		self.volume_volatility["log_volatility"] = round(sqrt((nb_log_volatility/self.size) * (sum([log(self.val_data["Volume"][i]/self.val_data["Volume"][i-1]) for i in range(1, self.size)]))**2),DECIMAL_LEVEL)
		self.volume_volatility["5_days_volatility"] = round(sqrt((1/(self.size/5)) * (sum([log(self.val_data["Volume"][i]/self.val_data["Volume"][i-1]) for i in range(1, self.size,5)]))**2),DECIMAL_LEVEL)


	def upgrade(self) : 
		"""
		blabla
		"""

		self.extract_file()
		self.manage_raw_data()
		self.add_MMAs()
		self.add_price_MMA()
		self.add_KPI()
		self.add_price_volatility()
		self.add_volume_volatility()


	def save_csv(self, file_name=DEFAULT_FILENAME, sep=SEP,coma_vs_point=True): 
		"""
		Save in data.val_data coverted in text in a csv readble format, covert the val_data order dict in a text, 
		with comas and return needed for CSV export
		"""

		text = str()

		# creates fist line with titles
		for i in self.val_data.keys() : 
			text+=str(str(i)+";")
		text +="\n"
	
		# creates data in str format for each line		
		for i in range(self.size):
			for j in self.val_data.keys() : 
				text+=str(str(self.val_data[j][i]) + sep)
			text+="\n"
		
		# be carefull for Excell or Odt : need a coma and no point 
		if coma_vs_point : 
			text = text.replace(".", ",")
		
		fichier = open(str("py."+ file_name), "w")
		fichier.write(text)
		fichier.close()


	def __repr__(self) : 
		"""
		Blabla
		"""
		text = str()
		for i, j in self.__dict__.items():
			text+= "{} : {}\n".format(i,j)
		
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
	data2 = StockData(file="AC.csv", directory= "/home/alex/stock_exchange_project/v1.1.1/Quotes/CAC40")
	data2.upgrade()



