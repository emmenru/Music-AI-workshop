import subprocess
import json
import os

def load_ordinal_columns(script_path: str, json_file: str) -> dict:
    """
    Run a script to generate a JSON file with column category order and load the JSON file.
    Parameters:
    - script_path (str): Path to the Python script that generates the JSON file.
    - json_file (str): Path to the JSON file to be loaded.
    Returns:
    - dict: The loaded dictionary from the JSON file.
    Raises:
    - subprocess.CalledProcessError: If the script fails to run.
    - FileNotFoundError: If the JSON file does not exist.
    """
    # Run script to create JSON file
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        print(f"{script_path} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e.stderr}")
        raise

    # Load the ordinal columns configuration file
    try:
        with open(json_file, 'r') as file:
            ordinal_columns = json.load(file)
        return ordinal_columns
    except FileNotFoundError:
        raise FileNotFoundError(f"{json_file} was not created. Check {script_path} for issues.")

def convert_to_categorical(col, ordinal_columns):
    """
    Converts a column to a categorical type with specified categories and order if the column is in the ordinal_columns dictionary.
    Parameters:
    - col (pandas.Series): The column to convert.
    - ordinal_columns (dict): Dictionary with column names as keys and category lists as values.
    Returns:
    - pandas.Series: The column as a ordered categorical type if it's in the dictionary, otherwise the original column.
    """
    if col.name in ordinal_columns:  # Check if column needs to be converted
        return pd.Categorical(col, categories=ordinal_columns[col.name], ordered=True)
    return col  # Return column unchanged if not in the dictionary

# Old stuff below
import pandas as pd 
def get_user_input():
    while True:
        try:
            user_number = int(input("Please enter a number: "))
            return user_number 
        except ValueError:
            print("That's not a valid number. Please try again.")


### Consider removing this 
### Seems columns in rows are flipped 
def input_data(columns, index): 
    # Initialize empty DataFrame with columns for answers and indices for questions
    df = pd.DataFrame(columns=columns, index=index)
    # Example of adding data for Q1:
    #df.loc['Q1'] = [1, 2, 3, 4, 5, 6]  # Replace with actual values for Q1
    # is it possible to input this from a CSV directly? What kind of data do we get from Mentimeter?

    # Loop through each question and ask for input for each answer
    for question in index:
        print(f"Enter answers for {question} (A-F):")
        answers = []
        for answer in columns:
            while True:
                try:
                    # Prompt for each answer value and convert it to an integer or desired data type
                    value = int(input(f"  Count for {answer}: "))
                    answers.append(value)
                    break  # Break out of the loop if input is successful
                except ValueError:
                    print("Please enter a valid integer.")
        
        # Assign the answers to the corresponding row in the DataFrame
        df.loc[question] = answers
    
    print("\nCompleted DataFrame:")
    print(df)
    return(df)
    
