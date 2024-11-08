import json

ordinal_columns = {
    'Human_or_AI_music': [
        'I strongly prefer human-made',
        'I prefer human-made', 
        'I slightly prefer human-made', 
        'I am neutral',
        'I slightly prefer AI-made', 
        'I prefer AI-made',
        'I strongly prefer AI-made'
    ],
    'Music_or_silence': [
        'I strongly prefer music', 
        'I prefer music',
        'I slightly prefer music', 
        'I am neutral',
        'I slightly prefer silence', 
        'I prefer silence', 
        'I strongly prefer silence'
    ],
    'Personalized_music': [
        'Strongly agree', 
        'Agree',
        'Slightly agree', 
        'I am neutral',
        'I slightly disagree', 
        'I disagree', 
        'I strongly disagree'
    ],
    'Privacy_vs_personalization': [
        'maximum privacy, minimum personalization', 
        'very high privacy, very low personalization',
        'high privacy, low personalization', 
        'moderate privacy, moderate personalization',
        'low privacy, high personalization', 
        'very low privacy, very high personalization', 
        'minimum privacy, maximum personalization'
    ],
    'Sharing_data': [
        'I strongly agree', 
        'I agree',
        'I slightly agree', 
        'I am neutral',
        'I slightly disagree', 
        'I disagree', 
        'I strongly disagree'
    ]
}

# Save to a JSON file
def save_ordinal_columns(file_path='ordinal_cols.json'):
    """Save the ordinal columns dictionary to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(ordinal_columns, file)

if __name__ == "__main__":
    save_ordinal_columns()