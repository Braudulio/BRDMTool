#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# loadCSV
#
# Created by Brad Morris
# Tuesday 11 November 2025
# Last Modified Wednesday 4 March 2026

import os, glob
import sys
import pandas as pd
#from NWT_getPref import NWT_getPref

def loadCSV(pname, fname, is_new_format=False):
	#print('Input: ' + pname + fname)

	if is_new_format:
		data = pd.read_csv(pname + fname, dtype=str, header=None, encoding='windows-1252')
	else:
		data = pd.read_csv(pname + fname, dtype=str, encoding='windows-1252')
	
	#data = []
	#with open(pname + fname, 'r') as file:
	#	reader = csv.DictReader(file)
	#	for row in reader:
	#		data.append(row)

	return data