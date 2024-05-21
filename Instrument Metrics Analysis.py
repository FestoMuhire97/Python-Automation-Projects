import os
import shutil
from datetime import datetime
import glob
import csv

def generate_instrument_metrics():
    if not os.path.isdir('C:/Program Files (x86)/HAMILTON/Instrument Metrics'):
    #if not os.path.isdir('C:/Users/Festo Muhire/Documents/Instrument Metrics'):
        #metrics_folder_path = os.mkdir('C:/Users/Festo Muhire/Documents/Instrument Metrics')
        metrics_folder_path = os.mkdir('C:/Program Files (x86)/HAMILTON/Instrument Metrics')
    
    #metrics_folder_path = 'C:/Users/Festo Muhire/Documents/Instrument Metrics'
    metrics_folder_path = os.mkdir('C:/Program Files (x86)/HAMILTON/Instrument Metrics')
    if not os.path.isfile(metrics_folder_path + '/' + 'Instrument Metrics Analysis' + '.csv'):
        with open (metrics_folder_path + '/' + 'Instrument Metrics Analysis' + '.csv', 'w', newline = '') as file_method:
            writer = csv.writer(file_method)
            writer.writerow(['Method Name'])
generate_instrument_metrics()

# function to append Method name to the .csv file:
def append_csv_file(method_name):
    csv_file = 'C:/Program Files (x86)/HAMILTON/Instrument Metrics'+ '/' + 'Instrument Metrics Analysis' + '.csv'
    with open (csv_file, 'a', newline = '') as file_method:
    #with open ('C:/Users/Festo Muhire/Documents/Instrument Metrics' + '/' + 'Instrument Metrics Analysis' + '.csv', 'a', newline = '') as file_method:
                writer = csv.writer(file_method)
                writer.writerow(method_name)

def generate_date_month_folders():
    if not os.path.isdir('C:/Program Files (x86)/HAMILTON/Hamilton Error Logs'):
    #if not os.path.isdir('C:/Users/Festo Muhire/Documents/Hamilton Error Logs'):
        #folder_path = os.mkdir('C:/Users/Festo Muhire/Documents/Hamilton Error Logs')
        folder_path = os.mkdir('C:/Program Files (x86)/HAMILTON/Hamilton Error Logs')
generate_date_month_folders()

def get_creation_month_year(tracefile_path):
    creation_time = os.path.getctime(tracefile_path)
    creation_date = datetime.fromtimestamp(creation_time)
    return creation_date.strftime('%m-%Y')

def get_creation_year(tracefile_path):
    creation_time = os.path.getctime(tracefile_path)
    creation_date = datetime.fromtimestamp(creation_time)
    return creation_date.strftime('%Y')

def move_tracefiles_to_folders(base_path, destination_folder):

    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path,file_name)
        # Get the month-year folder name
        month_year = get_creation_month_year(file_path)
        year = get_creation_year(file_path)


        # Create a month-year folder if doesn't exist
        destination_majorfolder = os.path.join(destination_folder +'/'+ 'Error logs - '+ f'{year}')
        if not os.path.isdir(destination_majorfolder):
             os.mkdir(destination_majorfolder)
        destination_path = os.path.join(destination_majorfolder +'/'+ month_year)
        if not os.path.isdir(destination_path):
            os.mkdir(destination_path)

        #Make Miscellaneous folder:
        destination_misc_path = os.path.join(destination_majorfolder +'/Misc')
        if not os.path.isdir(destination_misc_path):
            os.mkdir(destination_misc_path)

        #For trace logs, they will go in the folders, other folders will go in the Misc folder.
        if file_name.endswith('Trace.trc'):
             shutil.copy2(file_path, os.path.join(destination_path,file_name))
             with open(file_path,'r') as trace_file:
                  for line in trace_file:
                       if 'Analyze method - start' in line:
                            method_name = line.split('\\')[-1].replace('\n','').replace('hsl','med')
                            append_csv_file([method_name])
        else:
             shutil.copy2(file_path, os.path.join(destination_misc_path,file_name))

#base_path = 'C:/Users/Festo Muhire/Desktop/LogFiles'
base_path = 'C:/Program Files (x86)/HAMILTON/LogFiles'
#base_path = 'C:/Users/Festo Muhire/Desktop/Vantage3 Log files'
#destination_folder= 'C:/Users/Festo Muhire/Documents/Hamilton Error Logs'
destination_folder= 'C:/Program Files (x86)/HAMILTON/Hamilton Error Logs'

#Trace_folder = glob.glob(destination_path)+ '/*')

move_tracefiles_to_folders(base_path,destination_folder)
