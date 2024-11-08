import json
import numpy as np
import os
import pandas as pd
from scipy.stats import chi2_contingency
from statsmodels.stats.contingency_tables import cochrans_q
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

# Cochran's Q test 
def perform_cochran_q_test(data):
    '''
    Performs Cochran's Q test on binary data and prints results.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame with binary (0 or 1) data.

    Returns:
    - float: Cochran's Q. 
    
    Raises:
    - ValueError: If data contains non-binary values.
    '''
    if not np.array_equal(data.values, data.values.astype(bool)):
        raise ValueError('Data must be binary (0 or 1) for Cochran\'s Q test.')

    results = cochrans_q(data.values)
    q_statistic = results.statistic
    p_value = results.pvalue

    print(f'Cochran\'s Q Statistic: {q_statistic}')
    print(f'P-value: {p_value}')
    
    if p_value < 0.05:
        print('Significant differences among the questions.')
    else:
        print('No significant differences among the questions.')
    print('-' * 50)
    return q_statistic

# Chi Square Goodness of Fit test 
def perform_chi2_test(df, column_name):
    '''
    Perform a Chi-Square Goodness of Fit test on a specified column of categorical data.

    Parameters
    ----------
    df : pandas.DataFrame
    - The DataFrame containing the categorical data.
        
    column_name : str
    - The name of the column to perform the test on.

    Returns: 
    - float: p_value
    -------
    None
        Prints the Chi-square statistic, p-value, and an interpretation of the result.
    '''
    # Calculate observed and expected frequencies
    observed_frequencies = df[column_name].value_counts().values
    total_observations = len(df)
    num_categories = len(observed_frequencies)
    expected_frequency = total_observations / num_categories
    expected_frequencies = [expected_frequency] * num_categories

    # Perform Chi-square Goodness of Fit test
    chi2, p_value, dof, _ = chi2_contingency([observed_frequencies, expected_frequencies])

    # Print results
    print(f'Chi-Square Goodness of Fit Test for column: {column_name}')
    print(f'Chi-square statistic: {chi2:.4f}')
    print(f'p-value: {p_value:.4f}')
    print(f'Degrees of freedom: {dof}')

    # Interpret significance
    if p_value < 0.05:
        print(f'****** Significant difference detected for {column_name}. ******')
    else:
        print(f'No significant difference detected for {column_name}.')
    print('-' * 50)
    return(p_value)

# Pairwise McNemar tests 


# Plotting functions
