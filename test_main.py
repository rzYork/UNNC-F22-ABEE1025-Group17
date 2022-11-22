#Name: Shenghang Chai
#edit time: 2022,11,22
from two_para_simulation import Simulation

eplus_run_path = './EnergyPlus9.5/energyplus'
idf_path = './1ZoneUncontrolled_win_test.idf'
out_put_dir='./simulation_output'
para_keys_1 = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'] 
para_keys_2 = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'] 
start_1=0.25
end_1=0.75
start_2=1.0
end_2=2.5
interval=0.02



simul=Simulation(eplus_run_path,idf_path,out_put_dir)
simul.interval=0.25
simul.start_a=0.25
simul.end_a=0.75
simul.start_b=1.0
simul.end_b=2.5
simul.para_key_a=para_keys_1
simul.para_key_b=para_keys_2



simul.run_simulation()
result=simul._result_set_value


result=result.split('_')
print(simul._simulation_results)
print("%s: \nOptiomal value:%f\n%s: \n Optiomal value: %f\nHighest Average Temperature: %f" 
	%(simul.para_key_a,float(result[0]),simul.para_key_b,float(result[1]),simul._highest_average_value))

# print("Interval %d\nPara A: %s\nValue range: %d-%d\nPara B: %s\nValue range: %d-%d" %(simul.interval,simul.para_key_a,simul.start_a,simul.end_a,simul.para_key_b,simul.start_b,simul.end_b))
# print("The combine simulation with the highest average inndoor air temperature\nPara A: %s\nOptimal value: %d\nPara B: %s\nOptimal value: %d" %(simul.para_key_a,result[0],simul.para_key_b,result[1]))
