#Name: Ruizhe Huang
#Created Date: 2022.11.22

import sys,os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from parametric_simulation import run_one_parameter_parametric

# class RangeError(Exception):
# 	def __init__():
# 		pass

class Simulation():

	def __init__(self,eplus_run_path: str,
						idf_path: str,
						output_dir: str):
		self.interval=0.02
		self.para_vals=[]
		self.eplus_run_path=eplus_run_path
		self.idf_path=idf_path
		self.output_dir=output_dir
		self._start_a = None
		self._end_a = None
		self._start_b = None
		self._end_b = None
		self._para_key_a=None
		self._para_key_b=None
		self._plot_column_name='ZONE ONE:Zone Mean Air Temperature [C](TimeStep) '
		self._temp_mean_a=None
		self._temp_mean_b=None
		self._highest_average_value=None
		self._simulation_results=None
		self._result_set_value=None
	@property
	def interval(self):
		return self._interval
	
	@interval.setter
	def interval(self,new_interval):
		try:
				new_interval=float(new_interval)
				if new_interval>0:
					self._interval=new_interval
		except: 
			print("illegal interval,it should be digital")
			sys.exit(1)

	@property
	def para_key_b(self):
		return self._para_key_b

	@para_key_b.setter
	def para_key_b(self,new_para_key_b):
		self._para_key_b=new_para_key_b

	@property
	def para_key_a(self):
		return self._para_key_a

	@para_key_a.setter	
	def para_key_a(self,new_para_key_a):
		self._para_key_a=new_para_key_a

	@property
	def start_a(self):
		return self._start_a

	@start_a.setter
	def start_a(self,start):
		start=float(start)
		if start<0:
			raise Exception("illegal start value,it should be positive")
		elif self._end_a is not None and start>=self._end_a:
			raise Exception("Start value should less than end value!")
		else:
			self._start_a=start
	@property
	def start_b(self):
		return self._start_b
	@start_b.setter
	def start_b(self,start):
		start=float(start)
		if start<0:
			raise Exception("illegal start value,it should be positive")
		elif self._end_b is not None and start>=self._end_b:
			raise Exception("Start value should less than end value!")
		else:
			self._start_b=start
	@property
	def end_a(self):
		return self._end_a
	@end_a.setter
	def end_a(self,end):
		end=float(end)
		if end<0:
			raise Exception("illegal end value,it should be positive")
		elif self._start_a is not None and end<=self._start_a:
			raise Exception("End value should more than start value!")
		else:
			self._end_a=end
	@property
	def end_b(self):
		return self._end_b
	@end_b.setter
	def end_b(self,end):
		end=float(end)
		if end<0:
			raise Exception("illegal end value,it should be positive")
		elif self._start_b is not None and end<=self._start_b:
			raise Exception("End value should more than start value!")
		else:
			self._end_b=end

	@property
	def highest_average_value(self):
		if self._highest_average_value is None:
			raise Exception("You should run the simulatoin first!")
		return self._highest_average_value

	@property
	def simulation_results(self):
		if self._simulation_results is None:
			raise Exception("You should run the simulatoin first!")
		return self._simulation_results
	@property
	def result_set_value(self):
		if self.result_set_value is None:
			raise Exception("You should run the simulation first!")
		return self._result_set_value


	

	

	def run_simulation(self):
		if(self.start_a is None or self.start_b is None or self.end_a is None or self.end_b is None or self.para_key_a is None or self.para_key_b is None):
			raise Exception("Please done the init steps first!")

		num_a=int((self.end_a-self.start_a)/self.interval)
		para_vals_a=[]

		num_b=int((self.end_b-self.start_b)/self.interval)
		para_vals_b=[]
		if num_a == 0:
			para_vals_a=[self.start_a,self.end_a]
		else:
			for i in range(num_a+1):
				para_vals_a.append(self.start_a+self.interval*i)
			if para_vals_a[len(para_vals_a)-1]<self.end_a:
				para_vals_a.append(self.end_a)


		if num_b==0:
			para_vals_b=[self.start_b,self.end_b]
		else:
			for i in range(num_b+1):
				para_vals_b.append(self.start_b+self.interval*i)
			if para_vals_b[len(para_vals_b)-1]<self.end_b:
				para_vals_b.append(self.end_b)

		out=run_one_parameter_parametric(self.eplus_run_path,self.idf_path,self.output_dir,self.para_key_a,para_vals_a,self.para_key_b,para_vals_b)

		d={}
		for item in out.keys():
			table_df=pd.read_csv(out[item])
			temp_vals=table_df[self._plot_column_name].values
			d[item]=sum(temp_vals/len(temp_vals))
			
		self._result_set_value=max(d,key=d.get)
		self._simulation_results=d
		self._highest_average_value=d[max(d,key=d.get)]


	
	# def get_mean(self,output):
	# 	d={}
	# 	for item in output.keys():
	# 		table_df=pd.read_csv(output[item])
	# 		temp_vals=table_df[self._plot_column_name].values
	# 		d[item]= sum(temp_vals)/len(temp_vals)
	# 	return d

	
	# def run_simulation(self):
	# 	if(self.start_a is None or self.start_b is None or self.end_a is None or self.end_b is None or self.para_key_a is None or self.para_key_b is None):
	# 		raise Exception("Please done the init steps first!")

	# 	num_a=int((self.end_a-self.start_a)/self.interval)
	# 	para_vals_a=[]

	# 	num_b=int((self.end_b-self.start_b)/self.interval)
	# 	para_vals_b=[]
	# 	if num_a == 0:
	# 		para_vals_a=[self.start_a,self.end_a]
	# 	else:
	# 		for i in range(num_a+1):
	# 			para_vals_a.append(self.start_a+self.interval*i)
	# 		if para_vals_a[len(para_vals_a)-1]<self.end_a:
	# 			para_vals_a.append(self.end_a)


	# 	if num_b==0:
	# 		para_vals_b=[self.start_b,self.end_b]
	# 	else:
	# 		for i in range(num_b+1):
	# 			para_vals_b.append(self.start_b+self.interval*i)
	# 		if para_vals_b[len(para_vals_b)-1]<self.end_b:
	# 			para_vals_b.append(self.end_b)

	# 	out_dict_a=run_one_parameter_parametric(self.eplus_run_path,self.idf_path,self.output_dir+os.sep+'a',self.para_key_a,para_vals_a)
	# 	out_dict_b=run_one_parameter_parametric(self.eplus_run_path,self.idf_path,self.output_dir+os.sep+'b',self.para_key_b,para_vals_b)

	# 	max_combine_avg=None
	# 	max_combine_a=None
	# 	max_combine_b=None
	# 	self._temp_mean_a=self.get_mean(out_dict_a)
	# 	self._temp_mean_b=self.get_mean(out_dict_b)

	# 	for i in self._temp_mean_a.keys():
	# 		for j in self._temp_mean_b.keys():
	# 			if max_combine_avg is None or max_combine_avg<self._temp_mean_a[i]+self._temp_mean_b[j]:
	# 				max_combine_avg=self._temp_mean_a[i]+self._temp_mean_b[j]
	# 				max_combine_a=i
	# 				max_combine_b=j




	# 	return [max_combine_a,max_combine_b]
