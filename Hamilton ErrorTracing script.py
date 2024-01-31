import os
import glob
import csv
import shutil
import datetime
import pandas as pd
import openpyxl as pxl

#specify source directory
#source_directory = "C:/Users/Festo Muhire/Desktop/LogFiles"
source_directory = "C:/Program Files (x86)/HAMILTON/LogFiles"
#source_directory = "C:/Program Files (x86)/HAMILTON/LogFiles/LogFiles_SMVantage"

# specify destination directory
destination_directory = "C:/Program Files (x86)/HAMILTON/LogFiles/Error Trace"

# Creating a .csv file for details:
with open('Error_Metrics.csv', 'w', newline='') as file_Method:
    writer = csv.writer(file_Method)
    field = ['Date', 'Method Name', 'Error description']
    writer.writerow(field)

# looking in the Trace files:
files_trace = glob.glob(source_directory + '/*')
for file in files_trace:
    with open(file, 'r') as trc_file:
        for line in trc_file:
            if 'Analyze method - start' in line:
                method_start_line = line.split("\\")
                #Outputs Method name
                method_name = (method_start_line[-1]).replace('\n','').replace('hsl','med')
                #Outputs Method date and time
                method_date_time = (method_start_line[0]).split('>')
                method_date_time = method_date_time[0].split(" ")
                #outputs Method date
                method_date = method_date_time[0]
            
            # Looks for ADC errors and enclose files in a new folder
            if 'ADC Error' in line:
                shutil.copy(file, destination_directory)
            
            # Looks for error description for aborting:
            if 'Main - error' in line:
                error_line= line.split('Vector. ')
                error_description = error_line[1]
    
            #Exporting the Method details into a .csv file.
                with open('Error_Metrics.csv', 'a', newline='') as file_Method:
                    writer = csv.writer(file_Method)
                    writer.writerow([method_date, method_name,error_description])