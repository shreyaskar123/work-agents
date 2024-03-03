import argparse
import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_normalize_shakespeare(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        # Normalize the text
        data = data.lower()
        data = re.sub(r'[^a-z\s]', '', data)
        data = re.sub(r'\s+', ' ', data)
        return data

def calculate_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    cos_sim = cosine_similarity(vectors)[0][1]
    return cos_sim

def main():
    parser = argparse.ArgumentParser(description='Compare user input with Shakespeare text')
    parser.add_argument('-i', '--input', help='Input file path for the works of Shakespeare', required=True)
    parser.add_argument('-u', '--user_input', help='User input text to compare', required=False)

    args = parser.parse_args()
    input_file = args.input
    user_input = args.user_input

    if not user_input:
        user_input = input('Please enter your text input: ')

    try:
        shakespeare_text = load_and_normalize_shakespeare(input_file)
        user_input_normalized = re.sub(r'[^a-z\s]', '', user_input.lower())
        cos_sim = calculate_cosine_similarity(shakespeare_text, user_input_normalized)
        result = {'similarity_score': cos_sim}
    except Exception as e:
        result = {'error': str(e)}

    print(json.dumps(result))

if __name__ == '__main__':
    main()