import openai
import json
import os 
import re 
from openai import OpenAI
client = OpenAI()

def make_gpt4_call(prompt):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You help write code as an expert software engineer.",
            },
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
    
def subtask(transcript):
    prompt = f"{transcript} Please divide this task into subtasks give each subtask as a JSON. Only give the JSON and nothing else. Thinking step by step. The only field should have task and description and nothing else. Make each description super specific so someone without asking any questions can do it. Each task should involve writing code and nothing else. Also ensure that the final output is valid json and only valid json. Don't forget to add commas. Make sure all opening brace has closing brace (very important!)"
    return make_gpt4_call(prompt)

def write_code(codebase, task, description):
    prompt = f"Please do task: {task} with description {description}. The current codebase is {codebase}. Please tell me what file you want to add the code to and if you want to create a new file with code. Specifically give me a json for each file with fields: 'file_name', 'new' (bool) and 'code' . Please give me absolutely nothing else expect for the valid JSON. Make sure to put commas if needed (important!). Please don't have Invalid \escape in your code (very important!). Make sure your file_name is always a FILE in the current folder and never like a folder/file_name"
    return make_gpt4_call(prompt)
    
def write_test(codebase, task, description):
    prompt = f"I am writing code to do this task: {task} with description {description}. The current codebase is {codebase}. You are tasked to write enterprise-grade tests, both unit and integration tests, to test that my code is working rigurously. They need to be fully complete. Specifically, if I run the test files that you will produce then it should run the tests cases through the code and give what percent of the tests passed. Please print out the percent and the specific tests that didn't pass. Specifically, say 'percent':  percent and then in the new line start giving me the tests that didn't pass. Please return the following: a json for each test file with fields 'file_name', 'new' (bool) and 'code'. Also in the json in the field commands, please give me comma separated commands that when executed will print out the percent and the tests that didn't pass.  Remember regardless of what happens the output should always be 'Percent': percent and what test cases failed. This format is standardized. The output should always be exactly that . Don't tell me how many failed. Give me percent instead Make sure that when i run the code that the code doesn't give any errors. Please give me absolutely nothing else expect for the valid JSON. Make sure to put commas if needed (important!). Please don't have Invalid \escape in your code (very important!). Make sure your file_name is always a FILE in the current folder and never like a folder/file_name"
    return make_gpt4_call(prompt)

def clean_code(code):
    prompt = f"Please cleanup the following code (if needed) {code} so that it compiles. For example, delete multiple __main__ and put all the library imports at the begenning of file. Please return the entire code of that file as input. DO NOT be lazy and please give each and every code line of the file. Also be sure to ONLY include the code. Include the FULL code and NOTHING else. The most important thing is that when your response is compiled and run it should work without errors. I am going to copy and paste your full response including any words that you write so ensure only the code is given as your output. Assume that all local imports are correct so don't delete them"
    return make_gpt4_call(prompt)

def clean_json_string(json_string):
    # Remove triple backticks
    clean_string = json_string.replace("```json", "").replace("```", "").strip()
    return clean_string

def fix_invalid_escapes(json_string):
    # Escape unescaped backslashes but ignore valid escape sequences
    fixed_string = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_string)
    
    # Optionally, handle specific cases, like Windows paths, more precisely
    # This example is simplistic and may need adjustment based on your data
    fixed_string = re.sub(r'\\\\([a-zA-Z])', r'\\\1', fixed_string)
    
    return fixed_string

def process_transcript_file(file_path):
    tasks = []
    descriptions = []
    with open(file_path, 'r') as file:
        transcript = file.read()  # Read the entire file content
        response_text = subtask(transcript)
        # Clean the response text
        cleaned_response_text = clean_json_string(response_text)
        
        # First, try parsing without modification
        try:
            tasks_descriptions = json.loads(cleaned_response_text)
        except json.JSONDecodeError:
            # If parsing fails, it indicates a deeper issue with the JSON format
            print(f"Error decoding JSON: {cleaned_response_text}")
            return tasks, descriptions
        
        # If parsing is successful
        for task_description in tasks_descriptions:
            tasks.append(task_description.get('task', ''))
            descriptions.append(task_description.get('description', ''))

    return tasks, descriptions

def fix_faulty_json(json_string):
    # Fix common escape character issues
    json_string = json_string.replace('\\"', '"').replace("\\'", "'")
    
    
    # Attempt to fix unquoted keys
    json_string = re.sub(r'([{,]\s*)(\w+)(\s*:\s*)', r'\1"\2"\3', json_string)
    
    # Attempt to correct simple single/double quote issues
    json_string = json_string.replace("'", '"')
    
    return json_string
def get_files_and_code(folder_path):
    files_and_code = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):  # Consider only Python files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                code = file.read()
                files_and_code += f"filename: {filename}, code: {code}\n"
    return files_and_code

def write_code_to_file(code_json):
    # Ensure the 'alg_code' directory exists
    directory = "alg_code_4"
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        code_info = json.loads(fix_invalid_escapes(code_json))
    except json.JSONDecodeError as e:
        # print(f"JSON decode error: {e}")
        return 
    try:
        file_name = code_info.get("file_name")
        new = code_info.get("new")
        code = code_info.get("code")
    except:
        file_name = code_info[0].get("file_name")
        new = code_info[0].get("new")
        code = code_info[0].get("code")
    
    # Construct the full path to the file within the 'alg_code' directory
    file_path = os.path.join(directory, file_name)
    
    # Write or overwrite the file with the provided code
    if new:
        try:
            with open(file_path, 'w') as file:
                file.write(code)
            print(f"File '{file_name}' has been successfully created/updated in '{directory}'.")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        # If the file should not be created anew, append to it if it exists
        if os.path.exists(file_path):
            try:
                with open(file_path, 'a') as file:
                    file.write("\n" + code)
                print(f"Code appended to existing file '{file_name}'.")
            except Exception as e:
                print(f"Error appending to file: {e}")
        else:
            print(f"File '{file_name}' does not exist. Set 'new' to True to create it.")


def update_files_with_cleaned_code(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):  # Filter for Python files
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    original_code = file.read()
                cleaned_code = clean_code(original_code)
                with open(file_path, 'w') as file:
                    file.write(clean_json_string(cleaned_code))
                print(f"{filename} has been cleaned and updated.")
            except Exception as e:
                print(f"Failed to clean {filename}: {e}")

def main(file_path):
    tasks, descriptions = process_transcript_file(file_path)
    if len(tasks) != len(descriptions):
        raise ValueError("susssss.")
    for idx in range(len(tasks)):
        codebase = get_files_and_code('alg_code_4')
        task, description = tasks[idx], descriptions[idx]
        json_code = write_code(codebase, task, description)
        write_code_to_file(clean_json_string(json_code))
    update_files_with_cleaned_code('alg_code_4')


