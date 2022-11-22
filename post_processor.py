#Author: Shenghang Chai
#First created: 2022 10 25
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
def eplus_to_datetime(date_str):
    if date_str[-8:-6] != '24':
        dt_obj = pd.to_datetime(date_str)
    else:
        date_str = date_str[0: -8] + '00' + date_str[-6:]
        dt_obj = pd.to_datetime(date_str) + dt.timedelta(days=1)
    return dt_obj
#Inputs:
#         i. output_paths, dict type, the same as the output_paths from the previous function
#         ii. plot_column_name, string type, the column name of which the results will be plotted in eplusout.csv
#         iii. y_axis_title, string, the title to the y axis of the plot
#         iv. plot_title, string, the title to the plot
#b) outputs: this function has no outputs. It will read all eplusout.csv files listed in output_paths, and plot the data at the column plot_column_name using matplotlib. The final plot figure must have:
#            i. use hourly time steps as the x-axis
#            ii. have y_axis_title as the y axis title
#            iii. have plot_title as the plot title
#            iv. each line in the plot has the key in output_paths as the legend 
def plot_1D_results(output_paths,plot_column_name,y_axis_title,plot_title):
	
	fontsize = 20
	fig, axs = plt.subplots(1, 1, figsize=(20,10))
	
	for item in output_paths.keys():
		table_df=pd.read_csv(output_paths[item])
		this_y = table_df[plot_column_name].values
		table_df['Date/Time']='2002'+table_df['Date/Time']
		table_df['Date/Time']=table_df['Date/Time'].apply(eplus_to_datetime)
		data_st_date = table_df.iloc[0]['Date/Time']
		data_ed_date = table_df.iloc[-1]['Date/Time']
		date_list = table_df['Date/Time']
		axs.plot(date_list, this_y,
	            alpha = 0.7,
	            linestyle = '--',
	            linewidth = 2,
	            label = item)
	datetime_ax_loc = mdates.HourLocator()  
	datetime_ax_fmt = mdates.DateFormatter('%H:%M')
	axs.xaxis.set_major_locator(datetime_ax_loc)
	axs.xaxis.set_major_formatter(datetime_ax_fmt)
	for tick in axs.xaxis.get_major_ticks():
		tick.label.set_fontsize(fontsize*0.8) 
	for tick in axs.yaxis.get_major_ticks():
		tick.label.set_fontsize(fontsize*0.8) 
	axs.tick_params('x', labelrotation=45)
	axs.set_xlabel('Time (%s to %s)'%(data_st_date, data_ed_date),
	              fontsize = fontsize)
	axs.set_ylabel(y_axis_title,
	              fontsize = fontsize)
	axs.set_title(plot_title)
	axs.legend(fontsize = fontsize)
	plt.show()