#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BRDM_getLocations
# 
# Created by Brad Morris
# Monday 20 October 2025
# Last Modified Friday 17 April 2026

import os, glob
import sys
import pandas as pd

script_path = os.getcwd() + os.sep + 'Scripts' + os.sep
sys.path.append(script_path)
from loadCSV import loadCSV
from pysideListALMLocType import pysideListALMLocType

def BRDM_getLocations(stype=None, scode=None, loc=None, ltype=None):	
	survey_locations = loadCSV(os.getcwd() + os.sep + 'Reference' + os.sep, 'BRDM_locations.csv')
	# print(survey_locations)

	if stype:
		survey_locations = survey_locations.loc[survey_locations['LocationType'] == stype]
		#Filter out non-NSW postcodes (older data)
		survey_locations = survey_locations.loc[survey_locations['Postcode'].str.startswith('2')]
		
	if scode:
		loc_info = survey_locations.loc[survey_locations['SiteCode'] == scode]
		loc_info = loc_info.squeeze(axis=0)
		survey_locations = loc_info['CleanupLocation']

	if loc:
		sc_info = survey_locations.loc[survey_locations['CleanupLocation'] == loc]
		sc_info = sc_info.squeeze(axis=0)
		if stype == 'ALM':
			if not ltype:
				ltype = pysideListALMLocType()
			survey_locations = sc_info['SiteCode'] + '-' + ltype
		else:
			survey_locations = sc_info['Postcode']
		
	return survey_locations



