# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 19:24:00 2023

@author: victo
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import re
# Get the current working directory
# Change the current working directory to a new path
new_directory = "C:/Users/victo/Google Drive/HDDM/3_parameter_trace/a_trace"
os.chdir(new_directory)


# List all files in the directory
file_list = os.listdir(new_directory)

# Filter files that end with "_slopes.csv"
csv_files = [file for file in file_list if file.endswith('_slopes.csv')]

# Loop through the filtered CSV files and read their data
for csv_file in csv_files:
    file_path = os.path.join(new_directory, csv_file)    
    # Read the CSV file using pandas
    df = pd.read_csv(file_path)
    # extract the ROI number from csv file title
    numbers = re.findall(r'\d+', csv_file)    
    numbers = [int(number) for number in numbers] # the numbers here isa list
    ROI = numbers[0]
    
    # Create the first figure for columns proto_slopes, rulefollower_slopes, and exception_slopes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    # Plot the first two columns (proto_slopes and rulefollower_slopes) on the first subplot
    ax1.plot(df['proto_slopes'], label='proto_slopes')
    ax1.plot(df['rulefollower_slopes'], label='rulefollower_slopes')
    ax1.plot(df['exception_slopes'], label='exception_slopes')
    # Plot the third column (exception_slopes) on the second subplot
    ax2.plot(df['proto_rf'], label='proto_rf')
    ax2.plot(df['rf_excep'], label='rf_excep')
    ax2.plot(df['proto_excep'], label='proto_excep')
    
    # Add labels, legends, and titles to the subplots
    ax1.set_xlabel('Trace')
    ax1.set_ylabel('Trace slope')
    ax1.legend()
    ax1.set_title(f'ROI{ROI} Slopes of threshold trace by stimuli')
    
    ax2.set_xlabel('Trace')
    ax2.set_ylabel('Slope Difference')
    ax2.legend()
    ax2.set_title(f'ROI{ROI} Differences of threshold trace slopes')
    # Adjust spacing between subplots
    plt.tight_layout()
    
    # Show the plots
    
    plt.savefig(f'ROI{ROI}_slopes_a.png')
    plt.show()










