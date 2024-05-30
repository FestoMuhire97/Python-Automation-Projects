import os
import shutil
import datetime

def get_files_from_startingdate(directory):

    # Create destination folder for all the files:
    error_folder = "C:/Users/Festo Muhire/Desktop/Error_folder"

    # Define the start date and the end date:
    x = int(input('what is the year:'))
    y = int(input('what is the month:'))
    z = int(input('what is the date:'))
    
    start_date = datetime.datetime(x,y,z)
    start_date = start_date.timestamp()
    print(start_date)
    end_date = datetime.datetime.now()
    end_date = end_date.timestamp()
    print(end_date)

    # Iterate through all files in the directory:
    for filename in os.listdir(directory):
        file_path = os.path.join(directory,filename)

        #check if it a file (not a directory):
        if os.path.isfile(file_path):
            # Get the creation time of the file:
            creation_time = os.path.getctime(file_path)

            # copy files if the creation is between the specified start date and now:
            if start_date <= creation_time <= end_date:
                shutil.copy2(file_path, error_folder)

# Directory path:
directory = 'C:/Program Files (x86)/HAMILTON/LogFiles'

get_files_from_startingdate(directory)
