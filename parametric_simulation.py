#Author: Ruizhe Huang
#Created at: 2022. 10. 25
import os

import json
import copy

from StaticEplusEngine import run_eplus_model,convert_json_idf


def run_combine_simulation_helper(eplus_run_path, idf_path, output_dir,
								parameter_key, parameter_val,parameter_key_b,parameter_val_b):
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
	inner_dict[parameter_key_b[-1]] = parameter_val_b


	######### step 4: dump the JSON dict to JSON file #########
	with open(epjson_path, 'w') as epjson:
		json.dump(epjson_dict, epjson)

	######### step 5: convert JSON file to IDF file #########
	convert_json_idf(eplus_run_path, epjson_path)

	######### step 6: run simulation #########
	run_eplus_model(eplus_run_path, idf_path, output_dir)

def run_one_parameter_parametric(eplus_run_path,idf_path,output_dir,parameter_key,parameter_vals,parameter_key_b,parameter_vals_b):
	dic_output={}
	os.makedirs(output_dir)
	for i in range(len(parameter_vals)):
		for j in range(len(parameter_vals_b)):
			o=output_dir+os.sep+str(parameter_vals[i])+'_'+str(parameter_vals_b[j])
			run_combine_simulation_helper(eplus_run_path,idf_path,o,parameter_key,parameter_vals[i],parameter_key_b,parameter_vals_b[j])
			dic_output[str(parameter_vals[i])+'_'+str(parameter_vals_b[j])]=o+os.sep+'eplusout.csv'
	return dic_output




