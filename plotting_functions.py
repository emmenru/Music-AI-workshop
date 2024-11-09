import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix

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


def plot_confusion_matrix(df_guesses, correct_answers_subset, title):
    # 1. Flatten the correct answers and guesses for the selected questions (Q1-Q6)
    y_true = []
    y_pred = []
    
    for question, correct_answer in correct_answers_subset.items():
        y_true.extend([correct_answer] * len(df_guesses))  # Repeat correct answer for each participant
        y_pred.extend(df_guesses[question].tolist())       # Append each participant's guesses
    
    # 2. Generate the combined confusion matrix
    labels = list(set(y_true + y_pred))  # Unique categories for consistent labeling
    conf_matrix = confusion_matrix(y_true, y_pred, labels=labels)
    
    # 3. Plot the combined confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Participant Guesses')
    plt.ylabel('Correct Answer')
    plt.title(title)
    plt.show()