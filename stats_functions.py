# Custom stats functions 
import numpy as np
import pandas as pd 
from scipy.stats import chi2_contingency, chi2
from statsmodels.stats.contingency_tables import cochrans_q

def interpret_significance(p_value): 
    if p_value < 0.05:
        print(f'****** Significant difference ******')
    else:
        print(f'No significant difference ')
    print('-' * 50)

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
    
    interpret_significance(p_value)
    return q_statistic

# G test that works column-wise, comparing different categories 
def g_test(df, column_name):
    '''
    Perform the G-test (Likelihood Ratio Test) for a categorical column in the DataFrame.

    Args:
    - df (pandas.DataFrame): DataFrame containing the data.
    - column_name (str): The name of the categorical column to perform the G-test on.

    Returns:
    - g_statistic (float): The G-statistic value.
    - p_value (float): The p-value indicating the significance of the result.    
    '''
    # Get the observed frequencies for the specified column
    observed = df[column_name].value_counts().values
    # Print to verify that all 7 (resp 3) categories are indeed represented (even if 0 counts)
    # print(df[column_name].value_counts())

    # Total number of observations
    total = np.sum(observed)
    #print(total)
    
    # Compute the expected frequencies assuming equal distribution
    expected = np.array([total / len(observed)] * len(observed))
    #print(expected)

    # Add a small constant to observed and expected to handle zeros
    epsilon = 1e-10  # Small constant to prevent division by zero
    observed = observed + epsilon
    expected = expected + epsilon

    # Calculate the G-statistic manually using the likelihood ratio formula
    g_statistic = 2 * np.sum(observed * np.log(observed / expected))

    # Degrees of freedom (number of categories - 1)
    dof = len(observed) - 1

    # Calculate the p-value using the chi-square distribution
    p_value = 1 - chi2.cdf(g_statistic, dof)

    # Print results 
    print(f'Column name: {column_name}\n'
      f'Observed: {observed}\n'
      f'Expected: {expected}\n'
      f'G-statistic: {g_statistic}\n'
      f'P-value: {p_value}')
    
    # Interpret significance
    interpret_significance(p_value)

    return(p_value)

# G test used for pairwise post hoc tests 
def g_test_pairwise(df, column_name, category1, category2):
    '''
    Perform the G-test (Likelihood Ratio Test) for a specific pair of categories in a categorical column.

    Args:
    - df (pandas.DataFrame): DataFrame containing the data.
    - column_name (str): The name of the categorical column to perform the G-test on.
    - category1 (str): The first category to compare.
    - category2 (str): The second category to compare.

    Returns:
    - g_statistic (float): The G-statistic value.
    - p_value (float): The p-value indicating the significance of the result.    
    '''
    # Get the observed frequencies for the specified column for the two categories
    observed = df[column_name].value_counts().loc[[category1, category2]].values
    # If categories do not exist in the column, set their count to 0
    if len(observed) < 2:  # If one of the categories has no data
        observed = np.append(observed, [0]*(2 - len(observed)))

    # Total number of observations in the entire dataset
    total = len(df)  # Total observations in the full dataset
    
    # Compute the expected frequencies assuming equal distribution across 3 categories
    expected = np.array([total / 3] * 2)  # For the two categories being compared, divide by 3

    # Add a small constant to observed and expected to handle zeros
    epsilon = 1e-10  # Small constant to prevent division by zero
    observed = observed + epsilon
    expected = expected + epsilon

    # Calculate the G-statistic manually using the likelihood ratio formula
    g_statistic = 2 * np.sum(observed * np.log(observed / expected))

    # Degrees of freedom (2 categories - 1)
    dof = 1  # df for 2 categories is always 1

    # Calculate the p-value using the chi-square distribution
    p_value = 1 - chi2.cdf(g_statistic, dof)

    # Print results
    print(f'Comparing categories: {category1} vs. {category2}\n'
      f'Observed counts: {observed}\n'
      f'Expected counts: {expected}\n'
      f'G-statistic: {g_statistic}\n'
      f'P-value: {p_value}')

    # Interpret significance
    interpret_significance(p_value)

    return p_value

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

    # Print the contingency table, test statistic, and p-value 
    print(f'McNemars 2x2 Contingency Table:\n'
      f'Table: {contingency_table}\n'
      f'McNemar test statistic (without continuity correction): {mcnemar_statistic}\n'
      f'P-value: {p_value}')
    
    return contingency_table, mcnemar_statistic, p_value