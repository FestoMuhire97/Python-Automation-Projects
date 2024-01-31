import os
import glob
import csv
import shutil
import datetime
import pandas as pd
import openpyxl as pxl


# specify source directory
source_directory = "C:/Users/Festo Muhire/Desktop/LogFiles"
#source_directory = "C:/Program Files (x86)/HAMILTON/LogFiles" 

# specify destination directory
destination_directory = "C:/Program Files (x86)/HAMILTON/LogFiles/path_trc"

# Get a list of all files in the source directory
files = glob.glob(source_directory + '/*')

for file in files:
    if file.endswith('Trace.trc'):
        shutil.copy(file, destination_directory)
        
os.listdir(destination_directory)

# Creating a .csv file for details:
with open('Method_Output.csv', 'w', newline='') as file_Method:
    writer = csv.writer(file_Method)
    field = ['Start Time', 'Date', 'Method Name', 'End Time', 'Time Elapsed']
    writer.writerow(field)


# looking in the Trace files:
files_trace = glob.glob(destination_directory + '/*')
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
                #outputs Method start time
                method_start_time = method_date_time[1]

            if 'checksum' in line:
                final_method_date_time = line.split('>')
                final_method_date_time = final_method_date_time[0].split(' ')
                #outputs Method final time
                method_end_time = final_method_date_time[1]

            #outputs time elapsed from start to finish:
                # ---> Method start & end time into a time object
                method_start_time_obj = datetime.datetime.strptime(method_start_time, '%H:%M:%S')
                method_end_time_obj = datetime.datetime.strptime(method_end_time, '%H:%M:%S')
                #outputs time elapsed for the entire method:
                method_time_elapsed = str(method_end_time_obj - method_start_time_obj)
                
            #Exporting the Method details into a .csv file.
                with open('Method_Output.csv', 'a', newline='') as file_Method:
                    writer = csv.writer(file_Method)
                    writer.writerow([method_start_time, method_date, method_name,method_end_time,method_time_elapsed])

#Opening the .csv file using panda
Method_csv = pd.read_csv("C:/Users/Festo Muhire/Desktop/Python learning/New folder/Method_Output.csv")

#Arranging and counting the methods, and saving into an excel file format
Methods_count = Method_csv['Method Name'].value_counts()
method_metrics = pd.DataFrame(Methods_count)
method_metrics_excel = method_metrics.to_excel("Method_Output.xlsx", sheet_name="Method Count Metrics")

#Opening the workbook to append the Time & Date details
excel_workbook = pxl.load_workbook("C:/Users/Festo Muhire/Desktop/Python learning/New folder/Method_Output.xlsx")

#Creating another worksheet in the workbook
excel_method_TimeDate= excel_workbook.create_sheet(title = "Method Time Date Metrics")

#Appending the headers.
excel_method_TimeDate.append(field)

#Appending the contents in the new worksheet
for index,row in Method_csv.iterrows():
    excel_method_TimeDate.append(row.tolist())

#Saving the workbook to exit.
excel_workbook.save("C:/Users/Festo Muhire/Desktop/Python learning/New folder/Method_Output.xlsx")
