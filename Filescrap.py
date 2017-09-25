# -*- coding: utf-8 -*-

###########################
###########################

# Filescrap.py 

###########################
###########################



#########################
# 	SUMMARY
#########################



#########################
# 	IMPORT
#########################



#########################
# 	VAR & CONST
#########################



#########################
# 	CLASSES
#########################

class DataSetManager : 

	def __init__(self, file_list)

		dataset = list()

		#creating the dataset of Data objects
		for fi in file_list : 
			data_set.append(Data(fi))

		for i in range(len(data_set)) :
			data_set[i].extract_file()
			data_set[i].manage_raw_data()
			data_set[i].add_MMA30_MMA50()
			data_set[i].add_price_MMA30()
			data_set[i].add_KPI()
			data_set[i].add_volatility()

		self.dataset = dataset

		datasummary = list()

		for i in range(len(self.dataset)): 
			

		self.name = data.name
		self.size = data.size
		self.KPI = data.KPI
		self.volatility = data.volatility

	def function():
		passdef


#########################
# 	FUNCTIONS
#########################


def ask_folder() : 
	"""
	blabla
	"""
	
	return "/home/alex/stock_exchange_project/v1.1.0/Quotes/CAC40/"


def ask_files(folder) : 
	"""
	blabla
	"""

	os.chdir(folder)
	files = os.listdir()

	return files





#########################
# 	MAIN
#########################


folder = ask_folder()

file_list = ask_file(folder)

dataset = DataSetManager(file_list)

data_set_selected = list()

for i in data_set : 
	data_set_selected.(DataSummary(i))

del data_set
