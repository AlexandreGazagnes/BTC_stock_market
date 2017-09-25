############################
############################

#  stock_exchange_v1.0.2.py 

############################
############################



#########################
# 	SUMMARY
#########################

summary = """

Description :
	Script standable rapide qui pour but de traiter les fichiers CSV générés
	par le site abcbourse dans le cadre du téléchargement de l'historique
	d'un cours de bourse.

	On peut en effet télécharger les cours de bourses sur abcbourse, mais le 
	fichier CSV rendu est assez illisible.

	Le script suivant le rend lisible : 
	Il supprime les champs inutiles, regroupe les unités et les décimales (au lieu d'avoir
	12.89 on a 12 dans une colonne et 89 dans l'autre.
	Il rajoute des indicateurs techniques comme les moyennes mobiles 30/50 jours, leurs croisements etc
	idem entre cours et MMA30

	Il crée une classe "Data" qui organise et calcule toutes ses informations
	La classe Data possedes plusieurs attributs : 
		des attributs standards : file, name, source, size
		un attribut raw_data, inutile mais conservé, qui est une liste de liste avec toutes les datas
		un attribut values qui est un dict reprenant les data spécifiques self.values["Price"], self.values["Date"] etc etc
		un attribut KPI qui est un dictionnaire de dictionnaire.
			pour chaque stratégie testée, il enregistre la performance générée ["value"], les ordres d'achats ["buy"], et de vente ["buy"] 

	Enfin le script 
	Il recompile le tout dans un nouveau fichier CSV. 
	Il enregistre le fichier en ajoutant "py." avant le nom du fichier original

Previous :	
	passage en mode classe

Next :		
	Rajouter le MACD
	Rjouter une fonction qui sur la base du code de l'action FR00001234 va récupérer le nom de laction.
	terminier les locals min/max
	passer en sous objets, pas normal d'avoir un self.KPI["strategie"]["value"]
	quid de l'utilité des OrderDict()


Version :	1.1.0

Date 	:	25/09/2017

Auteur 	: 	Alexandre GAZAGNES

"""



#########################
# 	IMPORT
#########################

import os
import collections as coll



#########################
# 	VAR & CONSTANTS
#########################

DEFAULT_FILENAME =  "test.csv" #"cours_BTC_DOL_01.01.17_13.09.17.csv"
DECIMAL_LEVEL = 4
SEP = ";"
FEES = 0
NB_LOCAL_MIN_MAX = 10


#########################
#	CLASSES
#########################

class Data(object):
	"""
	classe Data, qui sert à enregistrer et caluculer tous les indiacteurs provenant
	d'un set de donées du cours d'une valeur
	"""

	def __init__(self, file="test.csv",source="abcbourse"): 
		"""init method"""

		self.file = file
		self.name = str()
		self.source = source
		self.raw_data = list()
		self.size = 0
		self.values = coll.OrderedDict()
		self.KPI = coll.OrderedDict()


	def extract_file(self):
		"""extract data from an text file, merge integers and decimals
		values if needed and convert basics datas in good type (int for ex)
		create size.data, name and raw data attributes"""
		
		fichier = open(self.file, "r")
		raw_data = fichier.readlines()
		fichier.close()

		if self.source == "abcbourse" : 
			for i in range(len(raw_data)):
				raw_data[i] = raw_data[i].replace("\n","")
				raw_data[i] = raw_data[i].split(",")

			self.size = len(raw_data)
			self.name = raw_data[0][0]

			for i in range(self.size):

				for j in range(2, len(raw_data[i])-2,2): 
					raw_data[i][j] = int(raw_data[i][j]) + (int(raw_data[i][j+1])/100)
				for j in [9,7,5,3,0]: 
					del raw_data[i][j]
				raw_data[i].insert(0, i+1)
		else: 
			raise ValueError

		self.raw_data = raw_data


	def manage_raw_data(self):
		"""manage raw datas creating an orderdict name values, an attribute, with 
		initials datas : Id Date Opening...
		"""

		# creates empty elements of orderdict values
		self.values["Id"], self.values["Date"], self.values["Opening"] = list(),list(),list()
		self.values["Min"], self.values["Max"] = list(),list()
		self.values["Price"], self.values["Volume"] = list(),list()

		# transfer basics datas from raw_data to values orderdict
		titles = ["Id", "Date", "Opening", "Min", "Max", "Price", "Volume"]
		for j, k in enumerate(titles): 
			for i in range(self.size): 
				self.values[k].append(self.raw_data[i][j])


	def add_MMA30_MMA50(self):
		"""based intials data in values orderdict, create technical idndicarors based on 
		moving mean : MMA30, MMA50, MMA30 VS MMA50, delta_MMA30_MMA50, and MMA30 X MMA50"""

		# creates empty elements of orderdict values
		self.values["MMA30"], self.values["MMA50"] = list(), list()
		self.values["MMA30_vs_MMA50"], self.values["delta_MMA30_MMA50"] = list(), list()
		self.values["MMA30_X_MMA50"] = list()

		# add MMA_30
		for i in range(self.size): 
			if i<30-1 : 
				self.values["MMA30"].append(0)
			elif i >=30-1 : 
				sub_sum = [self.values["Price"][i] for i in range(i, i-30, -1)]
				self.values["MMA30"].append(round(sum(sub_sum)/30,DECIMAL_LEVEL))
		
		# add MMA_50 --> FACTORISATION OF CODE !!!
		for i in range(self.size): 
			if i<50-1 : 
				self.values["MMA50"].append(0)
			elif i >=50-1 : 
				sub_sum = [self.values["Price"][i] for i in range(i, i-50, -1)]
				self.values["MMA50"].append(round(sum(sub_sum)/50,DECIMAL_LEVEL))

		# add MMA30 vs MMA 50
		for i in range(self.size): 
			if self.values["MMA30"][i] > self.values["MMA50"][i] and self.values["MMA30"][i] and self.values["MMA50"][i] : 
				self.values["MMA30_vs_MMA50"].append("+")
			elif self.values["MMA30"][i] < self.values["MMA50"][i] and self.values["MMA30"][i] and self.values["MMA50"][i] : 
				self.values["MMA30_vs_MMA50"].append("-")
			elif self.values["MMA30"][i] == self.values["MMA50"][i] and self.values["MMA30"][i] and self.values["MMA50"][i]:
				self.values["MMA30_vs_MMA50"].append("=")
			elif not (self.values["MMA30"][i] and self.values["MMA50"][i]) :
				self.values["MMA30_vs_MMA50"].append("")
			else : 
				raise ValueError

		# add delta MMA30 MMA50
		for i in range(self.size):
			if i < 50 : 
				self.values["delta_MMA30_MMA50"].append(0)
			else:
				self.values["delta_MMA30_MMA50"].append(round(
					(self.values["MMA30"][i] - self.values["MMA50"][i]) / self.values["MMA50"][i],DECIMAL_LEVEL))

		# add MMA30 X MMA50
		for i in range(self.size): 
			if self.values["MMA30_vs_MMA50"][i] and \
			self.values["MMA30_vs_MMA50"][i] != self.values["MMA30_vs_MMA50"][i-1]:
				self.values["MMA30_X_MMA50"].append(True)
			else : 
				self.values["MMA30_X_MMA50"].append("")


	def add_price_MMA30(self):
		"""based intials data in values orderdict, create technical idndicarors based on 
		moving mean vs price : price VS MMA300, delta_price_MMA30, and price X MMA30"""

		# creates empty elements of orderdict values
		self.values["price_vs_MMA30"], self.values["delta_price_MMA30"], \
		self.values["price_X_MMA30"]  = list(), list(), list()

		# add price vs MMA 30
		for i in range(self.size): 
			if self.values["Price"][i] > self.values["MMA30"][i] and self.values["MMA30"][i] : 
				self.values["price_vs_MMA30"].append("+")
			elif self.values["Price"][i] < self.values["MMA30"][i] and self.values["MMA30"][i] : 
				self.values["price_vs_MMA30"].append("-")
			elif self.values["Price"][i] == self.values["MMA30"][i] and self.values["MMA30"][i]:
				self.values["price_vs_MMA30"].append("=")
			elif not (self.values["MMA30"][i]) :
				self.values["price_vs_MMA30"].append("")
			else : 
				raise ValueError

		# add delta price MMA30
		for i in range(self.size):

			if i<30 : 
				self.values["delta_price_MMA30"].append(0)
			else:
				self.values["delta_price_MMA30"].append(round(
				(self.values["Price"][i] - self.values["MMA30"][i]) / self.values["MMA30"][i],DECIMAL_LEVEL))

		# add price X MMA30
		self.values["price_X_MMA30"].append("") # --> ????
		for i in range(1, self.size): 
			if self.values["price_vs_MMA30"][i] and \
			self.values["price_vs_MMA30"][i] != self.values["price_vs_MMA30"][i-1]:
				self.values["price_X_MMA30"].append(True)
			else : 
				self.values["price_X_MMA30"].append("")


	def add_KPI(self):
		"""self.KPI is an order dict, each elem of this dict is also a dic with the keys value, buy and sell
		"""

		# dumb indicator : buy the first day, sell the last one
		self.KPI["buy_begin_sell_end"] = coll.OrderedDict()
		self.KPI["buy_begin_sell_end"]["value"] = round( 1 + ((self.values["Price"][self.size - 1] - self.values["Price"][0]) / self.values["Price"][0]), DECIMAL_LEVEL)
		self.KPI["buy_begin_sell_end"]["buy"] = [0]
		self.KPI["buy_begin_sell_end"]["sell"] = [data.size - 1]
		
		#looks for the smalest global Price and the highest (but after the lower one)
		id_global_min, val_global_min = 0, self.values["Price"][0]
		for i,j in enumerate(self.values["Price"]) :
			if j < val_global_min : 
				id_global_min, val_global_min = i, j

		id_global_max, val_global_max = 0, self.values["Price"][0]
		for i,j in enumerate(self.values["Price"]) :
			if j > val_global_max and i > id_global_min : 
				id_global_max, val_global_max = i, j

		self.KPI["global_max_possible"] = coll.OrderedDict()
		self.KPI["global_max_possible"]["value"] = round(1 + ((val_global_max - val_global_min) / val_global_min), DECIMAL_LEVEL)
		self.KPI["global_max_possible"]["buy"] = [id_global_min ]
		self.KPI["global_max_possible"]["sell"] = [id_global_max ]

		
		# buy and sells for NB_LOCAL_MIN_MAX local min/max
		self.KPI["local_max_possible"] = coll.OrderedDict()

		def find_local_min(nb_locals=NB_LOCAL_MIN_MAX): 
			local_data = [(j,i) for (i,j) in enumerate(data.values["Price"])]
			local_min = sorted(local_data)[:nb_locals]
			local_min = [j for (i,j) in local_min]
			local_min = sorted(local_min)
			return local_min

		def find_local_max(local_min, nb_locals=NB_LOCAL_MIN_MAX) : 
			local_data = [(j,i) for (i,j) in enumerate(data.values["Price"])]
			local_max = list()
			for i in range(len(local_min)-1) :
				start, end  = local_min[i], local_min[i+1]
				local_max.append(max(local_data[start : end]))
			
			local_max.append(max(local_data[local_min[-1] : ]))

			local_max = [j for (i,j) in local_max]

			if len(local_max) == len(local_min) : 
				return local_max
			else : 
				raise ValueError

		def buy_sell_locals(local_values):     
			money, quantity, = 100, 0
			for (i,j) in local_values : 
				quantity = money / self.values["Price"][i]
				money = quantity * self.values["Price"][j]

			return round(money/100, DECIMAL_LEVEL)

		self.KPI["local_max_possible"]["value"] = 0
		self.KPI["local_max_possible"]["buy"] = local_min = find_local_min()
		self.KPI["local_max_possible"]["sell"] = local_max = find_local_max(local_min)
		local_values = zip(local_min,local_max)
		self.KPI["local_max_possible"]["value"] = buy_sell_locals(local_values)
		

		# buy and sells when MMA30 X MMA50
		def buy_sell_when_X(X_indicator, vs_indicator) : 
			buy, sell = list(), list()
			money, quantity, opened_order = 100, 0, False

			for i in range(data.size):
				if self.values[X_indicator][i] and self.values[vs_indicator][i] == "+" : 
					# Buy
					quantity = money / self.values["Price"][i]
					opened_order = True
					buy.append(i)

				elif self.values[X_indicator][i] and self.values[vs_indicator][i] == "-" \
				and opened_order: 
					# Sell if already a buy order
					money = quantity * self.values["Price"][i]
					opened_order = False
					sell.append(i)

			if opened_order : # if order opened, sell the last day 
				money = quantity * self.values["Price"][data.size -1]
				sell.append(i)
		
			return round(money/100, DECIMAL_LEVEL), buy, sell

		self.KPI["MMA30_X_MMA50"] = coll.OrderedDict()
		self.KPI["MMA30_X_MMA50"]["value"], self.KPI["MMA30_X_MMA50"]["buy"], self.KPI["MMA30_X_MMA50"]["sell"] =\
			buy_sell_when_X("MMA30_X_MMA50", "MMA30_vs_MMA50")

		self.KPI["price_X_MMA30"] = coll.OrderedDict()
		self.KPI["price_X_MMA30"]["value"], self.KPI["price_X_MMA30"]["buy"], self.KPI["price_X_MMA30"]["sell"] =\
			buy_sell_when_X("price_X_MMA30", "price_vs_MMA30")


	def convert_data_to_text(self, sep=SEP,coma_vs_point=True): 
		"""covert the values order dict in a text, with comas and return needed
		for CSV export"""

		text = str()

		# creates fist line with titles
		for i in self.values.keys() : 
			text+=str(str(i)+";")
		text +="\n"
	
		# creates data in str format for each line		
		for i in range(self.size):
			for j in self.values.keys() : 
				text+=str(str(self.values[j][i]) + sep)
			text+="\n"
		
		# be carefull for Excell or Odt : need a coma and no point 
		if coma_vs_point : 
			text = text.replace(".", ",")
		
		return text



#########################
# 	FUNCTIONS
#########################

"""

OLD FUNCTIONS FROM v1.0.0
Most of Them need to desapear or be integrated in class 
Data or other 

"""

def ask_original_filename(default=DEFAULT_FILENAME):
	
	"""
	while True : 
		ans = input("Nous sommes dans le dossier {}, est-ce le bon ?\n y/n\t".format(os.cwd))
		if not ans : 
			ans = "y"

		if ans ="y": 
			break
		elif : 
			ans = input("Veuillez saisir chemin du dossier parent\n")
			try : 
				change_dossier(ans)
				break
			except:
				input("Chemin {} invalide, tappez sur <Entrée> pour continuer...\n".format(ans))
	"""

	while True : 
		file_name = input("Quel est le fichier d'origine : \t")
		if not file_name : 
			return default
		if ".CSV" or ".csv" in file_name : 
			return file_name
		print("Erreur, ce doit etre un fichier CSV")


def save_csv(text, file_name=DEFAULT_FILENAME):
	fichier = open(str("py."+ file_name), "w")
	fichier.write(text)
	fichier.close()



#########################
# 	MAIN
#########################


file_name = ask_original_filename()

data = Data(file=file_name)

data.extract_file()
data.manage_raw_data()
data.add_MMA30_MMA50()
data.add_price_MMA30()
data.add_KPI()

text = data.convert_data_to_text()

save_csv(text)

