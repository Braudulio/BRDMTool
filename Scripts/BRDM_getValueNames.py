#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BRDM_getValueNames
# 
# Created by Brad Morris
# Monday 20 October 2025
# Last Modified Wednesday 25 March 2026

import os, glob
import sys
import math
import pandas as pd
import numpy as np

script_path = os.getcwd() + os.sep + 'Scripts' + os.sep
sys.path.append(script_path)
from loadCSV import loadCSV

def BRDM_getValueNames(ID=None, Vname=None, stype='EST'):	
	# value_names = loadCSV(os.getcwd() + os.sep  + 'Reference' + os.sep, 'KLIS_names_categories.csv')
	value_names = loadCSV(os.getcwd() + os.sep  + 'Reference' + os.sep, 'KLIS-ALM_index.csv')
	if stype == 'EST' or stype == 'RMB':
		val_quan = 'V'
	elif stype == 'ALM':
		val_quan = 'A'
		
	if ID:
		# v_info = value_names.loc[value_names['ID'] == ID]
		v_info = value_names.loc[value_names[val_quan + '#'] == ID.replace(val_quan,'')]

		v_info = v_info.squeeze(axis=0)
		# value_names = v_info['KLIS_ITEM']
		value_names = v_info['KLIS item name']
	elif Vname:
		# v_info = value_names.loc[value_names['KLIS_ITEM'] == Vname]
		v_info = value_names.loc[value_names['KLIS item name'] == Vname]
		v_info = v_info.squeeze(axis=0)

		# Check for parent V numbers
		# Check for non numbers in Parent
		try:
			pID = int(v_info['Parent V#'])
		except ValueError:
			pID = np.nan

		if not math.isnan(pID):
			if pID != int(v_info[val_quan + '#']):
				# print(pID)
				value_names = [val_quan + v_info[val_quan + '#'], val_quan + str(pID)]
			else:
				value_names = val_quan + v_info[val_quan + '#']
		else:
			value_names = val_quan + v_info[val_quan + '#']
			
		# Version 1
		# value_names = val_quan + v_info[val_quan + '#']

	return value_names



