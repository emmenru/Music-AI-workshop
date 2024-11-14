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

def create_answer_matrix(df, correct_answers):
    '''
    Create a matrix of 1s and 0s representing correct and incorrect answers.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the quiz data.
    correct_answers (list): A list of the correct answers, in the order of the quiz questions.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the answer matrix.
    '''
    correct_answers_dict = {}
    for i, answer in enumerate(correct_answers):
        if i < 6:
            correct_answers_dict[f"Q{i+1}"] = answer + ' image'
        else:
            correct_answers_dict[f"Q{i+1}"] = answer + ' sound'
    
    df_correct = df.copy()
    
    for i in range(12):
        df_correct[f'Q{i+1}'] = df_correct[f'Q{i+1}'].apply(lambda x: 1 if x == correct_answers[i] else 0)
    
    return df_correct.iloc[:, 3:]