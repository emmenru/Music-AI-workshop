# Custom stats functions 
import numpy as np
import pandas as pd 
from scipy.stats import chi2_contingency, chi2
from statsmodels.stats.contingency_tables import cochrans_q


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

# McNemar test 
def calculate_mcnemar_test(df, image_questions, sound_questions, threshold=3):
    '''
    Calculate a 2x2 contingency table and McNemar test statistic without continuity correction.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing binary response data for each participant.
      Each row represents a participant's responses to a series of questions, with columns
      indicating each question.
    - image_questions (list of str): List of column names corresponding to questions with images.
    - sound_questions (list of str): List of column names corresponding to questions with sounds.
    - threshold (int, optional): Minimum correct responses to classify a participant as
      high-performing in each condition. Default is 3 (out of 6 questions, for a 50% threshold).

    Returns:
    - contingency_table (pandas.DataFrame): 2x2 DataFrame showing counts for the McNemar test categories:
      [Yes-Yes, Yes-No, No-Yes, No-No].
    - mcnemar_statistic (float): McNemar test statistic (without continuity correction).
    - p_value (float): P-value associated with the McNemar test statistic.
    '''

    # Calculate correct answer counts for each condition per participant
    df['image_correct'] = df[image_questions].sum(axis=1)
    df['sound_correct'] = df[sound_questions].sum(axis=1)

    # Apply threshold to classify each participant's performance in each condition
    df['image_high'] = df['image_correct'] >= threshold
    df['sound_high'] = df['sound_correct'] >= threshold

    # Calculate counts for the McNemar test table categories
    a = ((df['image_high'] == True) & (df['sound_high'] == True)).sum()
    b = ((df['image_high'] == True) & (df['sound_high'] == False)).sum()
    c = ((df['image_high'] == False) & (df['sound_high'] == True)).sum()
    d = ((df['image_high'] == False) & (df['sound_high'] == False)).sum()

    # Populate a 2x2 contingency table
    contingency_table = pd.DataFrame({
        'Sound Correct (Yes)': [a, c],
        'Sound Incorrect (No)': [b, d]
    }, index=['Image Correct (Yes)', 'Image Incorrect (No)'])

    # Calculate the McNemar test statistic without continuity correction
    mcnemar_statistic = (b - c)**2 / (b + c) if (b + c) != 0 else 0

    # Calculate the p-value using chi-square distribution with 1 degree of freedom
    p_value = chi2.sf(mcnemar_statistic, df=1)

    # Print the contingency table, test statistic, and p-value (optional for debugging)
    print("McNemar's 2x2 Contingency Table:")
    print(contingency_table)
    print("\nMcNemar test statistic (without continuity correction):", mcnemar_statistic)
    print("p-value:", p_value)

    return contingency_table, mcnemar_statistic, p_value