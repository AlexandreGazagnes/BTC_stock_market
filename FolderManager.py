# -*- coding: utf-8 -*-

###########################
###########################

# FolderManager.py 

###########################
###########################



#########################
# 	SUMMARY
#########################



#########################
# 	IMPORT
#########################

import os 


#########################
# 	VAR & CONST
#########################


#########################
# 	CLASSES
#########################


class FolderManager : 
	"""
	blablabla
	"""

	def __init__(self):
		"""
		blabla
		"""

		self.init_folder = os.getcwd()
		self.source_folder = str()
		self.dest_folder = str()
		self.source_files = list()
		self.dest_files = list()

		self.ask_source_folder()
		self.ask_source_files()


	def ask_source_folder(self) : 
		"""
		blabla
		"""
	
		self.source_folder = "/home/alex/stock_exchange_project/v1.1.1/Quotes/CAC40"


	def ask_source_files(self) : 
		"""
		blabla
		"""

		os.chdir(self.source_folder)
		self.source_files = os.listdir()
		self.source_files.sort()
		os.chdir(self.init_folder)


#########################
# 	FUNCTIONS
#########################





#########################
# 	MAIN
#########################


if __name__ == '__main__':
	datasource = FolderManager()
