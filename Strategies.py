# -*- coding: utf-8 -*-

##########################
##########################

# Strategies.py 

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


#########################
# 	CLASSES
#########################

class Strategy : 
	"""
	blabla
	"""

	def __init__(self, when_buy, when_sell) : 
		"""
		blabla
		"""


#########################
# 	FUNCTIONS
#########################


#########################
# 	MAIN
#########################

# DUMB STRATEGIES
buy_first_sell_last = Strategy(("Date"==start_date),("Date"==end_date))
random_buy_sell = Strategy(("Date"==random()),("Date"==random()))

# TECHNICAL STRATEGIES
X_MMAs = Strategy((MMA1_X_MMA2 and MMA1_vs_MMA2>0),(MMA1_X_MMA2 and MMA1_vs_MMA2<0))
price_X_MMA = Strategy((price_X_MMA and price_vs_MMA>0),(price_X_MMA and price_vs_MMA<0))
mix_MMA_price = Strategy((MMA1_X_MMA2 and MMA1_vs_MMA2>0),(price_X_MMA and price_vs_MMA<0 ))
delta_MMA1_MMA2 = Strategy((MMA1_X_MMA2 and MMA1_vs_MMA2>0),(delta_MMA1_MMA2>15/100)) #or 30% or 50% etc etc
delta_price_MMA = Strategy((price_X_MMA and price_vs_MMA>0),(delta_price_MMA>15/100) #or 30% or 50% etc etc


#RANDOM STRATEGIES
random_buy_sell_if_5pc_loose_or_15pc_win
random_buy_sell_if_10pc_loose_or_30pc_win
random_buy_sell_if_3pc_loose_or_30pc_win
...



# MARTINGAL STRATEGIES
martingal_x2_stop_5pc
martingal_x3_stop_10pc
martingal_x2_5_stop_10pc
...

