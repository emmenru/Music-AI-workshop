import json
import os
import pandas as pd
import subprocess

# Formatting categorical data
def load_ordinal_columns(script_path: str, json_file: str) -> dict:
    '''
    Runs a script to generate a JSON file with column category order, and loads the JSON file.
    
    Parameters:
    - script_path (str): Path to the Python script generating the JSON file.
    - json_file (str): Path to the JSON file to be loaded.
    
    Returns:
    - dict: Loaded dictionary from the JSON file.
    
    Raises:
    - subprocess.CalledProcessError: If the script fails to run.
    - FileNotFoundError: If the JSON file does not exist.
    '''
    try:
        subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        print(f'{script_path} ran successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error running {script_path}: {e.stderr}')
        raise

    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f'{json_file} was not created. Check {script_path} for issues.')

def convert_to_categorical(col, ordinal_columns):
    '''
    Converts a column to ordered categorical type if in the ordinal_columns dictionary.
    
    Parameters:
    - col (pandas.Series): Column to convert.
    - ordinal_columns (dict): Dictionary with column names as keys and category lists as values.
    
    Returns:
    - pandas.Series: Ordered categorical column if in dictionary, else original column.
    '''
    if col.name in ordinal_columns:
        return pd.Categorical(col, categories=ordinal_columns[col.name], ordered=True)
    return col