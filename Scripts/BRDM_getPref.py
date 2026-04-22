#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BRDM_getPref
# 
# Created by Brad Morris
# Monday 20 October 2025
# Last Modified Tuesday 14 April 2026

import os, glob
import sys

def BRDM_getPref(pref_name='base_pathname'):
	fname = "BRDM_preferences.txt"
	dyn_vars = {}

	f = open(fname, "r")
	a = f.read()
	f.close()

	a_list = a.split("\n")
	for aa in a_list:
		if not aa.startswith('#') and aa:
			aas = aa.split('=')
			vn = aas[0].rstrip()
			vq = aas[1].lstrip()
			dyn_vars[vn] = vq

			# print(aas)
	
	if pref_name in dyn_vars:
		match pref_name:
			case 'do_write'|'do_plot':# Convert to Boolean
				if dyn_vars[pref_name] in ('True', 'true'):
					pref_out = True
				elif dyn_vars[pref_name] in ('False', 'false'):
					pref_out = False
				else:
					pref_out = True
			case 'alm_type_all':# Convert to list
				pref_out = dyn_vars[pref_name].split(',')
			case _:
				pref_out = dyn_vars[pref_name]
	else:
		pref_out = ''

	#if 'base_pathname' in dyn_vars:
	#	print(dyn_vars['base_pathname'])

	return pref_out
