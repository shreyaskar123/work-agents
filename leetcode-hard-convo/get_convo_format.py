import os
import time
from openai import OpenAI
import csv
import os

client = OpenAI()

def make_gpt4_call(prompt):
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    try:
        # Directly returning the string assuming further processing will be done later
        return response.choices[0].message.content
    except (KeyError, AttributeError):
        return "Unable to process the response."
    
def get_next_filename():
    """Finds the next available filename according to the specified pattern."""
    i = 1
    while os.path.exists(f"ps{i}.txt"):
        i += 1
    return f"ps{i}.txt"

def process_description(description):
    """Makes a GPT-4 call with the question description and saves the output to a new file."""
    convo = make_gpt4_call('simulate a conversation about this question like it is an interview interviewee type thing (dont have those as roles have like peoples names). You can have as many people as you want.  The conversation should provide someone full information to be able to go and do it. Dont actually give the solution. Just like walk through it maybe the intervieww can ask some like sample questions. Like this isnt just a interview but like a normal conversation/meeting Make sure to put it into it in the context of like a normal meeting' + description)
    
    output_filename = get_next_filename()
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(convo)

def process_csv(file_path):
    """Reads the 'description' column from a CSV and processes each entry."""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_description(row['description'])

if __name__ == "__main__":
    process_csv("leetcode_hard.csv")
