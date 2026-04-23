#!/usr/bin/env python
# coding: utf-8
# 
# BRDM_st_dev
# 
# 
# Created by Brad Morris
# Tuesday 21 April 2026
# Last Modified Tuesday 21 April 2026

import os, glob
import sys
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

script_path = os.getcwd() + os.sep + 'Scripts' + os.sep
sys.path.append(script_path)
from BRDM_getPref import BRDM_getPref
from BRDM_getLocations import BRDM_getLocations
from BRDM_getRegions import BRDM_getRegions
from BRDM_getValueNames import BRDM_getValueNames
from BRDM_load_item import BRDM_load_item

# Setup
st.set_page_config(layout="wide")

st.markdown('Simple app to display results of KLIS/ALM data analyses for a single item from a single location')
st.space('small')

col1, col2 = st.columns([0.3, 0.7], gap='large')

with st.sidebar:
	st.title('BRDM Main Item')
	# Survey type
	stypes_all = ['EST', 'ALM']
	stype = st.pills('Survey Type',stypes_all,default='EST')

# st.markdown(stype)

# Variable type
vtype = BRDM_getPref('vtype')

# Write to file
do_write = BRDM_getPref('do_write')

# Get location (including NSW/region)
pc = BRDM_getLocations(stype)
regions = BRDM_getRegions(stype)
loc_list = regions.tolist()
loc_list.extend(pc['CleanupLocation'].to_list())
loc_list.insert(0,'NSW')
loc_list.insert(1,'NSWtarget')

with st.sidebar:
	loc = st.selectbox('Select Location',
					loc_list,
					index=0,
					placeholder='Select Location...',
					)

#st.write('Survey type: ' + stype)
#st.write('Selected location: ' + loc)

# Get location type
if stype == 'ALM':
	ltype_list = BRDM_getPref('alm_type_all')
	with st.sidebar:
		ltype = st.selectbox('Select Location Type',
							ltype_list,
							index=0,
							placeholder='Select Location...',
					)
	
if loc == 'NSW':
	pp = 'NSW'
	is_reg = True
elif loc == 'NSWtarget':
	pp = 'NSWtarget'
	is_reg = True
elif loc in BRDM_getRegions(stype):
	pp = loc
	is_reg = True
else:
	if stype == 'EST':
		survey_locations = BRDM_getLocations(stype)
		pp = survey_locations['SiteCode'][survey_locations['CleanupLocation'] == loc].item()
	else:
		# ltype = 'IND'
		pp = BRDM_getLocations(stype,None,loc,ltype)

	is_reg = False

# Get item
vn = BRDM_getValueNames()
match stype:
	case 'EST'|'RMB':
		items_list= vn['KLIS item name'].to_list()
	case 'ALM':
		items_list= vn['ALM item name'].to_list()
items_list = [x for x in items_list if pd.notna(x)]#Remove Nan values

with st.sidebar:
	value_name = st.selectbox('Select Item',
					items_list,
					index=0,
					placeholder='Select Item...',
					)

# st.write(value_name)
idx_quan = BRDM_getValueNames(None, value_name, stype)

# Get count data for single quantity
# Try to load first
count_data, stderr_data = BRDM_load_item(stype, idx_quan, vtype)
# Simplified to only display processed data

# Table
with col1:
	# Combo count + stderr for plotting
	if pp in count_data.columns:
		df_combo = pd.concat([count_data['surveys'].astype('Int64'), count_data[pp], stderr_data[pp]], axis=1)
		df_combo.columns = ['surveys', 'count', 'stderr']

		if stype == 'ALM':
			fs = 0
		else:
			fs = 1
		df_combo['bar_colours'] = ['grey' if surveys == fs else 'green' for surveys in df_combo.surveys]
		if len(df_combo)>5:
			df_combo.iloc[1:4,3] = ['blue', 'blue', 'blue']

		st.write('**BRDM_' + value_name + '**')
		st.dataframe(df_combo, hide_index=True, column_config={'bar_colours': None})
	else:
		st.write('No data available for: ' + value_name + ' - ' + pp)
		df_combo = pd.DataFrame()

# Plot
with col2:
	if not df_combo.empty:
		#Bar plot for site
		# df_combo['bar_colours'] = ['grey' if surveys == 1 else 'green' for surveys in df_combo.surveys]
		# df_combo.iloc[1:4,3] = ['blue', 'blue', 'blue']

		quan = 'count'
		if vtype == 'count':
			ylab = 'Count'
		elif vtype =='countarea':
			if quan == 'percent':
				ylab = 'Percentage % (Count/Area)'
			else:
				ylab = 'Count (Num/1000m2)'

		if stype == 'ALM':
			loc = loc + ' (' + pp.split('-')[1] + ')'
		
		if quan == 'count':#Single
			pt = 'Location: ' + str(loc) + ' - Quantity: [' + idx_quan + '] ' + value_name
		
		if len(df_combo)<5:
			tns = 5
		else:
			tns = len(df_combo)
			
		# Create bars
		bars = alt.Chart(df_combo, title = pt).mark_bar(size=10).encode(
			alt.X('surveys').title('Survey Number').scale(domain=(1,tns)),
			y=quan,
			color=alt.Color('bar_colours').scale(None)
		)
		
		# Create error bars (calculated as Value +/- Error)
		error_bars = alt.Chart(df_combo).mark_errorbar(ticks=True).encode(
			alt.X('surveys').axis(format='d').scale(domain=(fs,tns)),
			alt.Y(quan, title=ylab),
			yError='stderr',
			color=alt.value('black')
		)
		
		# Layer them and display
		st.altair_chart(bars + error_bars, use_container_width=True)
