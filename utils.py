import pandas as pd, os, shutil, random, time
# from mail import SendAnEmail
from datetime import datetime, timedelta

def random_sleep(a=3,b=7,reson = ""):
    random_time = random.randint(a,b)
    print('time sleep randomly :',random_time) if not reson else print('time sleep randomly :',random_time,f' for {reson}')
    time.sleep(random_time)

def close_every_chrome():
    import subprocess

    # Get the path to the Chrome executable using the `whereis` command.
    chrome_path = subprocess.check_output(["whereis", "google-chrome"]).decode().split()[1]

    # Create a new subprocess object.
    subprocess_object = subprocess.Popen(
        [chrome_path, "--tab-close"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for the subprocess to finish executing.
    subprocess_object.wait()

    # Check if the subprocess exited successfully.
    if subprocess_object.returncode != 0:
        # Handle the error.
        raise Exception("Failed to close Chrome tab.")
    
    
def add_data_in_csv(json_data : dict, path : str):
    """
    Add a new row of data to a CSV file.

    Parameters:
        json_data (dict): A dictionary containing data for the new row.
        path (str): The path to the CSV file. If the file does not have a '.csv' extension, it will be appended.

    Returns:
        None
    """
    
    if not path.endswith('.csv'):
        path = path + '.csv'
    pathh = os.path.join(os.getcwd(),'csv',path)
    df = pd.read_csv(path)
    new_row = pd.DataFrame([json_data])
    new_df = pd.concat([df, new_row], ignore_index=True)
    new_df.to_csv(pathh, index=False)
    
    ...
    
def list_files_in_folder(folder_path):
    """
    Return a list of all files in the given folder path.
    
    Parameters:
        folder_path (str): The path to the folder.
        
    Returns:
        list: A list of file names in the folder.
    """
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and str(file_path).endswith('.csv'):
            files.append(file_name)
    return files


def check_csv_with_columns(path):
    """
    Create a CSV file with the specified columns if the given path does not exist.
    If the file already exists, check if all specified columns are present,
    and add any missing columns.

    Parameters:
        columns (list): A list of column names for the CSV file.
        path (str): The path to the CSV file.

    Returns:
        None
    """
    # Ensure the path ends with '.csv'
    if not path.endswith('.csv'):
        path = path + '.csv'
    
    # Define default columns based on the type
    columns = [
            "Likes",
            "Disclike",
            "Url",
            "Title",
            "Discription",
            "Release-Date",
            "Poster-Image_uri",
            "poster_download_uri",
            "Video-name",
            "video_download_uri",
            "Photo-name",
            "Pornstarts",
            "Category",
            "Username"
        ]
    
    # Check if the file already exists
    if os.path.exists(path):
        print("File already exists.")
        # Read existing CSV into a DataFrame
        df = pd.read_csv(path)
        # Check if all specified columns are present
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            print(f"Adding missing columns: {missing_columns}")
            # Add missing columns to the DataFrame
            for col in missing_columns:
                df[col] = None
            # Write DataFrame back to CSV
            df.to_csv(path, index=False)
            print(f"Columns added to existing CSV file at {path}")
        else:
            print("All specified columns are present.")
    else:
        # Create DataFrame with specified columns
        df = pd.DataFrame(columns=columns)
        # Write DataFrame to CSV
        df.to_csv(path, index=False)
        print(f"CSV file with columns {columns} created at {path}")
        
import os

def rename_file_with_description(file_path, new_path, new_name):
    """
    Rename a Python file with a given description.

    Args:
        file_path (str): Path to the Python file.
        description (str): Description to append to the filename.

    Returns:
        str: New filename with the description appended.
    """
    if not os.path.exists(file_path):
        print(f"Source file '{file_path}' does not exist.")
        return
    
    # Rename the file
    os.rename(file_path, new_path+'/'+ new_name)

    return new_name

# Example usage:
file_path = "example.py"  # Path to your Python file
description = "with_description"  # Description to append
new_file_path = ''

def move_file(source_path, destination_path):
    """
    Move a file from the source path to the destination path.

    Parameters:
        source_path (str): The path of the file to be moved.
        destination_path (str): The destination path where the file will be moved.

    Returns:
        None
    """
    # Check if the source file exists
    if not os.path.exists(source_path):
        print(f"Source file '{source_path}' does not exist.")
        return

    # Move the file to the destination path
    try:
        shutil.move(source_path, destination_path)
        print(f"File moved from '{source_path}' to '{destination_path}'.")
    except Exception as e:
        print(f"Error: {e}")
        
def move_downloading_video_to_destination_after_download(error_emails: list, destination_path: str):
    """
    Move a downloading video file from the 'downloads' directory to the specified destination directory.

    This function checks for any downloading video files in the 'downloads' directory. 
    If there is more than one downloading video file, it sends an error email.
    If there is exactly one downloading video file, it moves it to the specified destination directory.

    Parameters:
        error_emails (list): List of email addresses to send error notifications.
        destination_path (str): The path of the destination directory where the downloading video file will be moved.

    Returns:
        None
    """
    # Get the names of all downloading video files with the '.crdownload' extension
    downloading_videos = [i for i in os.listdir('downloads') if i.endswith('.crdownload')]
    # Check if there are more than one downloading video files
    
    # if len(downloading_videos) > 1:
    #     print('There are more downloading videos than expected.')
    #     SendAnEmail('There are more downloading videos than expected.', error_emails)
    #     return

    while True :
        time.sleep(1)
        new_video_download = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
        if not new_video_download:
            break  
    
    random_sleep(5,10)
    # If there is exactly one downloading video file
    if downloading_videos:
        video_name = downloading_videos[0].replace('.crdownload', '')
        # Move the downloading video file to the destination directory
        move_file(os.path.join(os.getcwd(), 'downloads', video_name), os.path.join(destination_path, video_name))

        
    
    
