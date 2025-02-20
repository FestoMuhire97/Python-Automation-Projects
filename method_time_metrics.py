import os
import glob
import csv
import shutil
import datetime
import pandas as pd


def determine_time_elapsed(source_directory: str) -> str:
    """
    This function determines the time elapsed for each method in the source directory.
    It creates a .csv file called "Method_Output.csv" in the source directory and writes the details of each method to it.

    Parameters:
    ----------
        source_directory (str): The path to the directory containing the Trace.trc files.

    Returns:
    --------
        str: The path to the .csv file containing the details of each method.
    """

    # specify destination directory
    destination_directory = os.path.join(source_directory, "path_trc")

    print(destination_directory)

    # create the destination directory if it doesn't exist
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Get a list of all files in the source directory
    files = glob.glob(source_directory + "/*")

    # Loop through each file in the source directory
    for file in files:
        if file.endswith("Trace.trc"):
            # copy the file to the destination directory
            shutil.copy(file, destination_directory)

    # create a .csv file for details:
    csv_file_path = os.path.join(source_directory, "Method_Output.csv")
    with open(csv_file_path, "w", newline="") as file_Method:
        writer = csv.writer(file_Method)
        field = [
            "Start Time",
            "Date",
            "Method Name",
            "End Time",
            "Time Elapsed",
            "Status",
        ]
        writer.writerow(field)

    # looking in the Trace files:
    files_trace = glob.glob(destination_directory + "/*")
    for file in files_trace:
        with open(file, "r") as trc_file:
            # Initialize variables before processing the file
            method_status = "Completed"  # default status
            method_start_time = None
            method_end_time = None
            method_date = None
            method_name = None
            method_time_elapsed = None

            for line in trc_file:
                if "Analyze method - start" in line:
                    method_start_line = line.split("\\")
                    # Outputs Method name
                    method_name = (
                        (method_start_line[-1]).replace("\n", "").replace("hsl", "med")
                    )
                    # Outputs Method date and time
                    method_date_time = (method_start_line[0]).split(">")
                    method_date_time = method_date_time[0].split(" ")
                    # outputs Method date
                    method_date = method_date_time[0]
                    # outputs Method start time
                    method_start_time = method_date_time[1]

                # check if the method went to completion or aborted:
                if "Main - error;" in line:
                    method_status = "Aborted"

                if "checksum" in line:
                    final_method_date_time = line.split(">")
                    final_method_date_time = final_method_date_time[0].split(" ")
                    # outputs Method final time
                    method_end_time = final_method_date_time[1]

                    # outputs time elapsed from start to finish:
                    # ---> Method start & end time into a time object
                    method_start_time_obj = datetime.datetime.strptime(
                        method_start_time, "%H:%M:%S"
                    )
                    method_end_time_obj = datetime.datetime.strptime(
                        method_end_time, "%H:%M:%S"
                    )
                    # outputs time elapsed for the entire method:
                    method_time_elapsed = str(
                        method_end_time_obj - method_start_time_obj
                    )

                    # Exporting the Method details into a .csv file.
                    with open(csv_file_path, "a", newline="") as file_Method:
                        writer = csv.writer(file_Method)
                        writer.writerow(
                            [
                                method_start_time,
                                method_date,
                                method_name,
                                method_end_time,
                                method_time_elapsed,
                                method_status,
                            ]
                        )

    # the function will return the csv file with method details:
    return csv_file_path


def get_method_time_metrics(method_output_file: str) -> pd.DataFrame:
    """
    This function calculates the mean time elapsed for each method in the method_output_file.

    Parameters:
    ----------
        method_output_file (str): The path to the .csv file containing the details of each method.

    Returns:
    --------
        pd.DataFrame: A dataframe containing the mean time elapsed for each method.
    """

    # read the method output file into a dataframe:
    time_metrics_df = pd.read_csv(method_output_file)

    # filter the dataframe to only include completed methods:
    completed_methods = time_metrics_df[time_metrics_df["Status"] == "Completed"]
    aborted_methods = time_metrics_df[time_metrics_df["Status"] == "Aborted"]

    # change the time elapsed to a timedelta object for completed methods:
    completed_methods["Time Elapsed"] = pd.to_timedelta(
        completed_methods["Time Elapsed"]
    )

    # calculate the mean time elapsed for completed methods:
    mean_time_elapsed = (
        completed_methods.groupby("Method Name")["Time Elapsed"]
        .mean()
        .apply(lambda x: str(x).split(".")[0].split("days")[1])
    ).to_frame()

    mean_time_elapsed["Completed"] = completed_methods["Method Name"].value_counts()
    mean_time_elapsed["Aborted"] = aborted_methods["Method Name"].value_counts()
    mean_time_elapsed["Aborted"] = mean_time_elapsed["Aborted"].fillna(0).astype(int)
    mean_time_elapsed["Total"] = (
        mean_time_elapsed["Completed"] + mean_time_elapsed["Aborted"]
    ).astype(int)
    return mean_time_elapsed


def write_output_to_csv(df: pd.DataFrame, output_file: str):
    """
    This function writes the dataframe to a .csv file in the source directory.

    Parameters:
    ----------
        df (pd.DataFrame): The dataframe to write to a .csv file.
        output_file (str): The path to the .csv file to write the dataframe to.

    Returns:
    --------
        None: The function does not return anything/ it writes the dataframe to a .csv file.
    """

    df.to_csv(output_file, index=True)


def main():
    source_directory = "C:/Program Files (x86)/HAMILTON/LogFiles"
    method_time_metrics = determine_time_elapsed(source_directory)
    time_metrics_df = get_method_time_metrics(method_time_metrics)
    output_file = os.path.join(source_directory, "Method_Time_Metrics.csv")
    write_output_to_csv(time_metrics_df, output_file)


if __name__ == "__main__":
    main()
