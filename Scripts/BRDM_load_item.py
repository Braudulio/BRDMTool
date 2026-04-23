# -*- coding: utf-8 -*-
#
# BRDM_load_item
# 
# Created by Brad Morris
# Friday 6 February 2026
# Last Modified Friday 6 February 2026

import os, glob
import sys
import math
import pandas as pd

script_path = os.getcwd() + os.sep + 'Scripts' + os.sep
sys.path.append(script_path)
from BRDM_getPref import BRDM_getPref
from BRDM_getValueNames import BRDM_getValueNames

def BRDM_load_item(stype, idx_quan, vtype = 'countarea'):
	# Input(s)
	# stype = 'EST'
	# vtype = 'countarea'
	# idx_quan = 'V17'

	pname = os.getcwd() + os.sep + 'Output' + os.sep
	fname = 'BRDM_' + vtype + '_' + stype + '_' + idx_quan + '_' + BRDM_getValueNames(idx_quan, None, stype).replace(' ','')
	# print(fname)
	st.write(pname + fname)
	
	# Check if file exists [dev]
	if os.path.exists(pname + fname + '.xlsx'):
		data_all = pd.read_excel(pname + fname + '.xlsx', sheet_name=None)
	
		count_data = data_all['count']
		stderr_data = data_all['stderr']
	else:
		count_data = pd.DataFrame()
		stderr_data = pd.DataFrame()
		
		print('No file for: ' + idx_quan)
	
	return (count_data, stderr_data)
