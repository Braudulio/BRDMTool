#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BRDM_getRegions
# 
# Created by Brad Morris
# Thursday 12 February 2026
# Last Modified Thursday 12 February 2026

import os, glob
import sys
import pandas as pd

script_path = os.getcwd() + os.sep + 'Scripts' + os.sep
sys.path.append(script_path)
from loadCSV import loadCSV

def BRDM_getRegions(stype, region=None):
	survey_locations = loadCSV(os.getcwd() + os.sep + 'Reference' + os.sep, 'BRDM_locations.csv')
	
	survey_locations = survey_locations.loc[survey_locations['LocationType'] == stype]
	#Filter out non-NSW postcodes (older data)
	survey_locations = survey_locations.loc[survey_locations['Postcode'].str.startswith('2')]
		
	if region:
		survey_locations = survey_locations.loc[survey_locations['Region'] == region]
	else:
		survey_locations = survey_locations['Region'].unique()
	
	return survey_locations
