# BTC_stock_market

Standable script wich import from an abcbourse extract stock market datas, compute basic technical indidactors and retrun profitability of various trading strategy

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
	un attribut values qui est un dict reprenant les data spécifiques self.values["Price"], 
		self.values["Date"] etc etc
	un attribut KPI qui est un dictionnaire de dictionnaire.
	pour chaque stratégie testée, il enregistre la performance générée ["value"], les ordres
		d'achats ["buy"], et de vente ["buy"] 

Enfin le script recompile le tout dans un nouveau fichier CSV. 
Il enregistre le fichier en ajoutant "py." avant le nom du fichier original

Previous :	
	passage en mode classe

Next :		
	Rajouter le MACD
	Rjouter une fonction qui sur la base du code de l'action FR00001234 va récupérer le nom de laction.
	terminier les locals min/max
	passer en sous objets, pas normal d'avoir un self.KPI["strategie"]["value"]
	quid de l'utilité des OrderDict()


Version :	1.0.2

Date 	:	18/09/2017

Auteur 	: 	Alexandre GAZAGNES
