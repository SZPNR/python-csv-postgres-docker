import pandas as pd
import os

def get_resource_csv_path(filename):
    current_directory = os.getcwd()
    resources_directory = os.path.join(current_directory, 'resources')
    file_path = os.path.join(resources_directory, f'{filename}.csv')
    return file_path

def import_csv_to_dataframe(filename):
    file_path = get_resource_csv_path(filename)
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return None

def export_dataframe_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    try:
        df.to_csv(file_path, index=False)
        print(f"Data exported to {file_path}")
    except Exception as export_error:
        print("Error exporting data:", export_error)
