import json
import os
import pandas as pd
import subprocess

# Formatting categorical data
def load_recode_mappings(json_file: str) -> dict:
    '''
    Loads recode mappings from a JSON file.
    
    Parameters:
    - json_file (str): Path to the JSON file containing recode mappings.
    
    Returns:
    - dict: Loaded dictionary of recode mappings.
    
    Raises:
    - FileNotFoundError: If the JSON file does not exist.
    '''
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f'{json_file} does not exist. Please check the file path.')


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
