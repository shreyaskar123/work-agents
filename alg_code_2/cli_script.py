```python
import argparse
import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load Shakespeare data
def load_shakespeare_data(filename):
    # Define the path to the file
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    file_path = os.path.join(data_folder, filename)

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        shakespeare_data = file.read()

    # Find the start and the end of the actual text
    start_pos = shakespeare_data.find('*** START OF THIS PROJECT GUTENBERG') + 1
    end_pos = shakespeare_data.find('*** END OF THIS PROJECT GUTENBERG')
    if start_pos > 0 and end_pos > 0:
        shakespeare_data = shakespeare_data[start_pos:end_pos]
    elif start_pos > 0:
        shakespeare_data = shakespeare_data[start_pos:]

    # Strip any additional whitespace that may exist
    shakespeare_data = shakespeare_data.strip()

    return shakespeare_data

# Function to evaluate the Shakespearean-ness of a prompt
def evaluate_prompt(prompt):
    # Load the Shakespeare dataset
    shakespeare_data = load_shakespeare_data('shakespeare.txt')

    # Tokenization: Using NLTK for tokenization
    nltk.download('punkt', quiet=True)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    shakespeare_tokens = tokenizer.tokenize(shakespeare_data)
    prompt_tokens = tokenizer.tokenize(prompt)

    # Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(shakespeare_tokens + prompt_tokens)

    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Average the similarity scores for a final 'Shakespearean-ness' score
    score = similarity.mean()
    return score

# Create the parser
parser = argparse.ArgumentParser(description='Evaluate the Shakespearean-ness of a prompt.')

# Add the '--prompt' argument
parser.add_argument('--prompt', type=str, help='A string input from the user.')

# Parse the arguments
args = parser.parse_args()

# Print the result if '--prompt' is used
if args.prompt:
    # Call the evaluate_prompt function and print the score
    score = evaluate_prompt(args.prompt)
    print(f'The Shakespearean-ness score of the prompt is: {score}')
```