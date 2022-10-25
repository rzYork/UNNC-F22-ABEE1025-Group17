#Author: Ruizhe Huang
#Created at: 2022. 10. 25
import os

import json
import copy

from StaticEplusEngine import run_eplus_model,convert_json_idf

eplus_run_path = './EnergyPlus9.5/energyplus'
idf_path = './1ZoneUncontrolled_win_1.idf'
parameter_key = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'] 
parameter_vals = [0.1,0.2,0.3,0.4,0.5]
output_dir = './result'


def run_one_simulation_helper(eplus_run_path, idf_path, output_dir,
								parameter_key, parameter_val):
	"""
	This is a helper function to run one simulation with the changed
	value of the parameter_key
	"""
	######### step 1: convert an IDF file into JSON file #########
	convert_json_idf(eplus_run_path, idf_path)
	epjson_path = idf_path.split('.idf')[0] + '.epJSON'

	######### step 2: load the JSON file into a JSON dict #########
	with open(epjson_path) as epJSON:
		epjson_dict = json.load(epJSON)

	######### step 3: change the JSON dict value #########
	# ['WindowMaterial:SimpleGlazingSystem', 
	#			 				'SimpleWindow:DOUBLE PANE WINDOW', 
	#			 				'solar_heat_gain_coefficient']
	inner_dict = epjson_dict
	for i in range(len(parameter_key)):
		if i < len(parameter_key) - 1:
			inner_dict = inner_dict[parameter_key[i]]
	inner_dict[parameter_key[-1]] = parameter_val

	######### step 4: dump the JSON dict to JSON file #########
	with open(epjson_path, 'w') as epjson:
		json.dump(epjson_dict, epjson)

	######### step 5: convert JSON file to IDF file #########
	convert_json_idf(eplus_run_path, epjson_path)

	######### step 6: run simulation #########
	run_eplus_model(eplus_run_path, idf_path, output_dir)

def run_one_parameter_parametric(eplus_run_path,idf_path,output_dir,parameter_key,parameter_vals):
	dict_1={}
	os.mkdir(output_dir)
	for i in range(len(parameter_vals)):
		o=output_dir+os.sep+str(i)+'_'+str(parameter_vals[i])
		run_one_simulation_helper(eplus_run_path,idf_path,o,parameter_key,parameter_vals[i])
		dict_1[str(parameter_vals[i])]=o+os.sep+'eplusout.csv'

	return dict_1




