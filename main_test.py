from parametric_simulation import run_one_parameter_parametric
from post_processor import plot_1D_results

eplus_run_path = './EnergyPlus9.5/energyplus'
idf_path = './1ZoneUncontrolled_win_test.idf'
parameter_key = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'] 
parameter_vals=[]
for i in range(25):
	parameter_vals.append(0.25+i*0.02)
output_dir = './param_exp_1'

plot_column_name='ZONE ONE:Zone Mean Air Temperature [C](TimeStep) '
y_axis_title='Indoor Air Temperature (C)'
plot_title=' Simulation of Indoor Air Temperature vs. SHGC'

out_dict=run_one_parameter_parametric(eplus_run_path,idf_path,output_dir,parameter_key,parameter_vals)

plot_1D_results(out_dict,plot_column_name,y_axis_title,plot_title)