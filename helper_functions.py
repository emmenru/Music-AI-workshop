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
    
