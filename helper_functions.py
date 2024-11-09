import json
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import pandas as pd
from scipy.stats import chi2_contingency, chi2
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

# Plotting functions
# Survey
def plot_survey(df, columns_to_plot, color, output_dir='plots/survey'):
    '''
    Create a bar plot for each specified column in the DataFrame `df`, saving the figure
    in the specified directory.

    Parameters:
    - df (DataFrame): The DataFrame containing survey data.
    - columns_to_plot (list): List of column names to plot.
    - output_dir (str): Directory path to save the plot. Default is 'plots/survey'.
    - color (str): Color for the bar plots. 
    '''
    max_x = 18 
    
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up figure
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 5))
    axes = axes.flatten()
    
    # Plot each column
    for i, col in enumerate(columns_to_plot):
        if i >= len(axes):  # Safety check in case there are more columns than subplots
            break
        ax = axes[i]
        value_counts = df[col].value_counts().sort_index()  # Maintain ordinal order
        value_counts.plot(kind='barh', ax=ax, color=color)
        
        ax.set_xlabel('Count', fontsize=12)
        ax.set_title(f'{col.replace('_', ' ')}', fontsize=14)
        ax.set_xticks(range(0, max_x + 1, 2))
        ax.set_xlim(0, max_x+1)  # Set x-axis limit
        ax.set_ylabel('', fontsize=12)
        
    # Remove unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    # Save and display
    plt.tight_layout()
    plt.savefig(f'{output_dir}/survey_results.png', dpi=300, bbox_inches='tight')
    plt.show()

# Quiz
def plot_and_save_questions(df, title, color_map, unique_categories, correct_answers_dict, output_dir='plots/quiz', max_x=13):
    '''
    Create a set of bar plots for each column in the DataFrame `df`, saving individual plots and a combined figure.

    Parameters:
    - df (DataFrame): The DataFrame containing survey data.
    - title (str): Title for the main plot figure.
    - color_map (dict): Mapping of categories to colors.
    - unique_categories (array): List of unique categories in the responses.
    - output_dir (str): Directory to save the plots. Default is 'plots/quiz'.
    - max_x (int): Maximum x-axis value for the plots. Default is 13.
    '''
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    
    # Create main figure
    fig, axes = plt.subplots(3, 2, figsize=(15, 8))
    axes = axes.flatten()
    
    # Iterate over columns and plot
    for i, col in enumerate(df.columns):
        ax = axes[i]
        
        # Count occurrences of each response and reindex to ensure all categories are represented
        counts = df[col].value_counts().reindex(unique_categories, fill_value=0)
        
        # Create bar plot for each column
        counts.plot(kind='barh', ax=ax, color=[color_map[category] for category in counts.index])
        ax.set_title(f"{col}: {correct_answers_dict.get(col, '')}", wrap=True, fontsize=14)
        ax.set_xlabel("Count", fontsize=12)
        ax.set_ylabel("")
        ax.set_xlim(0, max_x)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.tick_params(axis='both', labelsize=12)

        # Save individual subplot
        individual_fig = plt.figure(figsize=(8, 5))
        individual_ax = individual_fig.add_subplot(111)
        counts.plot(kind='barh', ax=individual_ax, color=[color_map[category] for category in counts.index])
        individual_ax.set_title(f"{col}: {correct_answers_dict.get(col, '')}", wrap=True, fontsize=14)
        individual_ax.set_xlabel("Count", fontsize=12)
        individual_ax.set_ylabel("")
        individual_ax.set_xlim(0, max_x)
        individual_ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        individual_ax.tick_params(axis='both', labelsize=12)

        # Save group plot
        individual_fig.tight_layout()
        individual_fig.savefig(f"{output_dir}/{col.lower()}_plot.png", dpi=300, bbox_inches='tight')
        plt.close(individual_fig)
    
    # Finalize and save the main figure
    fig.tight_layout()
    plt.suptitle(title, fontsize=16, y=0.95)
    plt.subplots_adjust(top=0.9)
    main_filename = f"{output_dir}/subplots_{title.lower().replace(' ', '_').replace(':', '')}.png"
    plt.savefig(main_filename, dpi=300, bbox_inches='tight')
    plt.show()

def plot_stacked_bar(df_subset, title, color_map, unique_categories, label_dict, output_dir='plots/quiz'):
    """
    Create a stacked bar plot for survey questions, saving the figure in the specified directory.

    Parameters:
    - df_subset (DataFrame): The subset of the DataFrame containing survey data.
    - title (str): Title for the stacked bar plot.
    - color_map (dict): Mapping of categories to colors.
    - unique_categories (array): List of unique categories in the responses.
    - label_dict (dict): Dictionary mapping column names to their labels.
    - output_dir (str): Directory to save the plot. Default is 'plots/quiz'.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create figure and calculate response counts
    ax = df_subset.apply(pd.Series.value_counts).fillna(0).T.reindex(columns=unique_categories, fill_value=0).plot(
        kind='bar', stacked=True, figsize=(15, 8), color=color_map.values())
    
    # Title, labels, and tick formatting
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlabel("Questions", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    ax.set_xticklabels([f"{col}: {label_dict[col]}" for col in df_subset.columns], rotation=45, ha='right', fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    # Y-axis and legend settings
    ax.set_ylim(0, ax.get_ylim()[1] + 1)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.legend(title="Response", loc='upper left', fontsize=12, title_fontsize=14, bbox_to_anchor=(1, 1))
    
    # Save and display plot
    plt.tight_layout()
    plt.savefig(f"{output_dir}/stacked_{title.lower().replace(' ', '_').replace(':', '')}.png", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def plot_correct_answers(total_correct_per_question, correct_answers_dict, colorblind_palette, IMAGE_LIST, SOUND_LIST, output_dir='plots/quiz'):
    '''
    Plot a horizontal bar chart showing the number of correct answers per question,
    with distinct colors for image and sound-related questions, and save the figure.

    Parameters:
    - total_correct_per_question (Series): Series containing the number of correct answers for each question.
    - correct_answers_dict (dict): Mapping of question numbers to their descriptions.
    - colorblind_palette (list): List of colors for visual distinction (e.g., for images and sounds).
    - IMAGE_LIST (list): List of image-related question identifiers (e.g., Q1-Q6).
    - SOUND_LIST (list): List of sound-related question identifiers (e.g., Q7-Q12).
    - output_dir (str): Directory to save the plot. Default is 'plots/quiz'.
    '''
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert Series to DataFrame and sort by 'CorrectAnswers'
    correct_answers_df = total_correct_per_question.reset_index()
    correct_answers_df.columns = ['Questions', 'CorrectAnswers']
    correct_answers_df = correct_answers_df.sort_values(by='CorrectAnswers', ascending=True)

    # Create detailed labels combining question number and description
    detailed_labels = [f"{q} : {correct_answers_dict.get(q, '')}" for q in correct_answers_df['Questions']]
    
    # Define colors based on question categories (image or sound)
    colors = [colorblind_palette[0] if q in IMAGE_LIST else colorblind_palette[1] 
              for q in correct_answers_df['Questions']]
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar plot
    plt.barh(range(len(detailed_labels)), correct_answers_df['CorrectAnswers'], color=colors)
    
    # Set the y-tick positions and labels
    plt.yticks(range(len(detailed_labels)), detailed_labels)
    
    # Title and axis labels
    plt.title('Correct Answers per Question', fontsize=16)
    plt.xlabel('Number of Correct Answers', fontsize=12)
    plt.ylabel('Question', fontsize=12)
    
    # Set x-axis ticks to integers
    plt.xticks(range(0, math.ceil(correct_answers_df['CorrectAnswers'].max()) + 2))

    # Add legend
    legend_handles = [
        patches.Patch(color=colorblind_palette[0], label='Images (Q1-Q6)'),
        patches.Patch(color=colorblind_palette[1], label='Sounds (Q7-Q12)')
    ]
    plt.legend(handles=legend_handles, title='Condition', loc='upper right')

    # Adjust layout and save the plot
    plt.tight_layout()
    filename = f"{output_dir}/corrects.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()

