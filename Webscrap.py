# -*- coding: utf-8 -*-

###########################
###########################

# Webscrap.py 

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



#########################
# 	FUNCTIONS
#########################


def ask_for_web_site() : 
	"""
	commentary
	"""
	while True :
		ans = input("voulez-vous passer par abcbourse?\n y/n\t")
		print()
		if not ans or ans = "y":
			break
		else : 
			print("Fonctionnalité en développement :)")
			raise ValueError


def ask_for_companies() : 
	"""
	commentary
	"""

	cac40 = ['Accor Hotels', 'Air Liquide', 'Airbus', 'Arcelor Mittal', 'Atos', 'Axa', 
	'Bnp Paribas', 'Bouygues', 'Cap Gemini', 'Carrefour', 'Credit Agricole', 'Danone',
	 'Engie', 'Essilor Intl', 'Kering', 'LafargeHolcim', 'Legrand SA', "L'oreal", 'Lvmh',
	  'Michelin', 'Orange', 'Pernod Ricard', 'Peugeot', 'Publicis Groupe', 'Renault', 
	  'Safran', 'Saint Gobain', 'Sanofi', 'Schneider Electric', 'Societe Generale', 
	  'Sodexo', 'Solvay', 'Stmicroelectronics', 'TechnipFMC', 'Total', 'Unibail-Rodamco', 
	  'Valeo', 'Veolia Environ.', 'Vinci', 'Vivendi']


	action_list = list()
	first_ans = True

	print("""Tappez votre/vos actions, puis <Enter>. 
			Tappez 'all' pour toutes les actions du cac40 et 'end' une fois votre liste terminée, 
			ou 'q' pour quitter le programme""")
	while True : 
		ans = input()
		if ans == "all" and first_ans: 
			return cac40
		elif ans == "all" and not first_ans : 
			print("choix impossible, appuyez sur 'end' pour stopper la saisie ou 'q' pour quitter")
		elif ans == 'q':
			raise ValueError
		elif ans : 
			first_ans = False
			action_list.append(ans)
		elif ans = "end":
			break

	return action_list


#########################
# 	MAIN
#########################



website = ask_for_web_site()

action_list = ask_for_companies()
action_symbol  = list()

for action in action_list: 
	# rectifier 
	action = rectificate_action_name(action) # faire que renaut devienne renault"
	
	# trouver la bonne page wikipedia
	url_wiki = url_search_google(action + "action euronext")
	url_wiki = "https://fr.wikipedia.org/wiki/Vivendi"

	
	# trouver le symbol
	url_euronext = "https://www.euronext.com/fr/search_instruments/"
	web_page = urllib.request.urlopen(url_wiki)
	html = str(web_page.read())
	nb = html.find(url_euronext)
	symbol = html[len(url_euronext) + nb : len(url_euronext) + nb + 10]
	nb = symbol.find("?")
	symbol = symbol[0:nb]
	
	# trouver url abcbourse

	url_abcbourse = "https://www.abcbourse.com/download/download.aspx?s={}p".format(symbol)
	web_page = urllib.request.urlopen(url_abcbourse)
	html = str(web_page.read())
	nb = html.find("télécharger cotations")


	#telecharger sur yahoo.finance

	symbol = str(symbol.upper()+".PA")

	url_yahoo_finance_webpage = "https://fr.finance.yahoo.com/quote/{}/history?period1={1474322400}&period2={1505858400}&interval=1d&filter=history&frequency=1d".format(
	symbol, 1474322400, 1505858400)
	url_yahoo_finance_dl = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}".format(
	symbol, 1474322400, 1505858400, "b2GHn7G5QTJ")






proceed_data() 
