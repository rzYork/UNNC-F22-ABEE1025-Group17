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
    pass