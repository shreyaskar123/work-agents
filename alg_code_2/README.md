# CLI Shakespearean-ness Evaluator

This tool evaluates the "Shakespearean-ness" of a given string of text by comparing it with the works of William Shakespeare using TF-IDF vectorization and cosine similarity.

## Setup

To set up the environment, you need to:

1. Ensure Python is installed on your system.
2. Install the required libraries by running `pip install -r requirements.txt`. The `requirements.txt` should contain `nltk`, `scikit-learn`, and any other necessary packages.

## Running the script

Run the script using Python from the command line:


python cli_script.py --prompt "Your text here"


Replace `"Your text here"` with the string you want to evaluate.

## Overview of the CLI

The CLI accepts a single argument, `--prompt`, which is the text prompt provided by the user. The script then evaluates its Shakespearean-ness and returns the score.

## Functions

- `load_shakespeare_data(filename)`: This function loads the text data of Shakespeare's works, parses it, and returns it.
- `evaluate_prompt(prompt)`: This function evaluates the Shakespearean-ness of the passed prompt. It makes use of the `load_shakespeare_data` function and processes the data further to return a similarity score.
