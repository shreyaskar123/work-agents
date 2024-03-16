import openai
import json
import os 
import re 
from openai import OpenAI
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
    
def subtask(transcript):
    prompt = f"{transcript} Please divide this task into subtasks give each subtask as a JSON. Only give the JSON and nothing else. Thinking step by step. The only field should have task and description and nothing else. Make each description super specific so someone without asking any questions can do it. Each task should involve writing code and nothing else. Also ensure that the final output is valid json and only valid json. Don't forget to add commas. Make sure all opening brace has closing brace (very important!)"
    return make_gpt4_call(prompt)

def write_code(codebase, task, description, percent_pass=None, result=None, prev_generated_code=None):
    prompt = f"Please do task: {task} with description {description}. The current codebase is {codebase}. Please tell me what file you want to add the code to , if you want to create a new file with code and the line number where you want me to start putting this code. Specifically give me a json for each file with fields: 'file_name', 'new' (bool), 'code' and 'start_line_number'. Please give me absolutely nothing else expect for the valid JSON. Make sure to put commas if needed (important!). Please don't have Invalid \escape in your code (very important!). Make sure your file_name is always a FILE in the current folder and never like a folder/file_name.  Make sure to not have the word python in the begenning of the the code, it should be runnable directly"
    if percent_pass:
        self_reflection_context = None #self_reflection_summary(percent_pass=percent_pass, 
                                                         # result=result, 
                                                         # generated_code=prev_generated_code, 
                                                         # subtask_descr=description, 
                                                         # codebase=codebase)
        prompt = f"Please do task: {task} with description {description}. Previously, I wrote the following code {prev_generated_code}. But the percent pass is {percent_pass}. I want 100\% pass. More specifically this is the result of the test cases {result}. A third-party person said that this might be a reason as to why we are failing some tests: {self_reflection_context}. The current codebase is {codebase}. Please tell me what file you want to add the code to and if you want to create a new file with code and the line number from where you want me to start putting the code. Also if you want to delete please give me start_line_number and end_line_number for this deletion. Specifically give me a json for each file with fields: 'file_name', 'delete' (bool -- true for delete and false for add), 'new' (bool), 'code', 'start_line_number', 'end_line_number'. Make sure all of these keys (including the code key is always there). Please give me absolutely nothing else expect for the valid JSON. Make sure to put commas if needed (important!). Please don't have Invalid \escape in your code (very important!). Make sure your file_name is always a FILE in the current folder and never like a folder/file_name"

    return make_gpt4_call(prompt)
    
def write_test(codebase, task, description, directory_name):
    file_name = f'{task}_{directory_name}.json'
    prompt = f"I am writing code to do this task: {task} with description {description}. The current codebase is {codebase}. You are tasked to write enterprise-grade tests, both unit and integration tests, to test that my code is working rigurously. They need to be fully complete. If the codebase already has relavent testing files, it means that the testing didn't comple so please fix it. Often times this happens because the name of the file that you are trying to import to test is wrong. Another case is if you are trying to use a module like pytest. All your python commands should only have python has input. That's it (no pytest). Specifically, if I run the test files that you will produce then it should run the tests cases through the code and give what percent of the tests passed. Please print out the percent and the specific tests that didn't pass. Specifically, say 'percent':  percent and then in the new line start giving me the tests that didn't pass. Please return the following: a json for each test file with fields 'file_name', 'new' (bool) and 'code'. Also in the json in the field commands, please give me comma separated commands that when executed will print out the percent and the tests that didn't pass. For reference the directory name is {directory_name}. Please incorporate that in your command. The command should be runnable on powershell (so it should include the directory name and also like \\ or whatever as needed to make it properly run in powershell). If you do cd please make sure to go back to current dir after running it. Make sure that the command is like runnable when i run it, so for example don't use ',' when seperating the two statements and you something like ; instead. Remeber in json you need to use double quote for keys instead of single keys so make sure keys have double quote (super important!). The error I don't want is Expecting property name enclosed in double quotes so make sure the json doesn't have that (super important!). Remember regardless of what happens the output should always be 'Percent': percent and what test cases failed. This format is standardized. The output should always be exactly that . Don't tell me how many failed. Give me percent instead Make sure that when i run the code that the code doesn't give any errors. Please give me absolutely nothing else expect for the valid JSON. Make sure to put commas if needed (important!).Make sure that when I run command, the code works. This is especially important for local imports. If the command has cd directory_name then don't do directory_name.function in the test file. Also make sure (super important!) that when you do imports that the file name and the function name are both accurate as reflected in the codebase given in the prompt. Make the command simple. in the code. Please don't have Invalid \escape in your code (very important!). Make sure your file_name is always a FILE in the current folder and never like a folder/file_name. DO NOT have anything else like explanaiton or something. ONLY JSON. Make sure to not have the word python in the begenning of the the code, it should be runnable directly "
    output = make_gpt4_call(prompt)
    with open(file_name, "w") as file:
        file.write(output)
    return output 


def clean_code(code):
    prompt = f"Please cleanup the following code (if needed) {code} so that it compiles. For example, delete multiple __main__ and put all the library imports at the begenning of file. Please return the entire code of that file as input. DO NOT be lazy and please give each and every code line of the file. Also be sure to ONLY include the code. Include the FULL code and NOTHING else. The most important thing is that when your response is compiled and run it should work without errors. I am going to copy and paste your full response including any words that you write so ensure only the code is given as your output. Assume that all local imports are correct so don't delete them"
    output =  make_gpt4_call(prompt)
    lines = output.strip().split('\n')
    if lines[0] == 'python' or lines[0] == '```python':
        lines = lines[1:]
    cleaned_code = '\n'.join(lines)
    return cleaned_code

def get_test_info(command):
    import subprocess
    parts = command.split(';')
    cwd = os.getcwd()
    percent_pass_final, result_final = None, None 
    updated_dir = ""
    for part in parts:
        part = part.strip() 

        if part.startswith('cd '):
            # Change the directory within Python
            new_directory = part.split('cd ')[1].strip()
            new_dir = part[3:]  # Extract the directory to change to
            try:
                os.chdir(new_dir)
                updated_dir = new_dir 
            except FileNotFoundError:
                print(f"Directory '{new_dir}' not found. Attempting to continue with subsequent commands.")
        else:
            code_is_working = False 
            iter = 0
            while not code_is_working and iter < 3:
                iter += 1
                print(f'the current dir is {os.getcwd()}')
                result = subprocess.run(part, shell=True, text=True, capture_output=True)
                if result.returncode != 0:
                    cur_dir = os.getcwd()
                    basename = os.path.basename(cur_dir)
                    print(basename)
                    if basename != 'zoom':
                        parent_dir = os.path.dirname(cur_dir)
                        os.chdir(parent_dir)
                    if iter == 2:
                        if len(updated_dir) > 0:
                            os.chdir(updated_dir)
                    print(f"Command '{part}' failed with error: {result.stderr}")
                    continue 
                else:
                    code_is_working = True 
                    output = result.stderr
                    first_line = output.split('\n')[0]
                    passed_tests = first_line.count('.')
                    total_tests = first_line.count('F') + first_line.count('E') + first_line.count('.')
                    if total_tests == 0:
                        percent_pass_final, result_final = 0, result
                    else:
                        percent_pass = (passed_tests / total_tests) * 100
                        percent_pass_final, result_final = percent_pass, result
            if iter >= 2:
                return -1, result_final
    os.chdir(cwd)
    print(result_final)
    return percent_pass_final, result_final   
def self_reflection_summary(percent_pass, result, generated_code, subtask_descr, codebase):
    prompt = f'. The task Im trying to do is {subtask_descr}. The current codebase is {codebase}. I generated this code {generated_code}. But the following is the percent of test cases that passed {percent_pass} and this is more specific info on the text cases {result}. I want my code to have 100\% accuracy. Please self-reflect and give me what needs to be modified for the correct answer. Note that the line numbers here are given just for your convenience (and arent there when the code is actually run)'
    make_gpt4_call(prompt)
    
    

def clean_json_string(json_string):
    # Remove triple backticks
    clean_string = json_string.replace("```json", "").replace("```", "").strip()
    return clean_string

def fix_invalid_escapes(json_string):
    # Convert Python boolean and None values to JSON equivalents
    json_string = re.sub(r'\bTrue\b', 'true', json_string)
    json_string = re.sub(r'\bFalse\b', 'false', json_string)
    json_string = re.sub(r'\bNone\b', 'null', json_string)
    # Preprocess the string to escape backslashes, ensuring not to double-escape
    json_string = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_string)
    """
    try:
        json_dict = json.loads(json_string)
    except json.JSONDecodeError as e:
        # Handle JSON decoding error (e.g., logging, raising an exception)
        raise ValueError("Invalid JSON string") from e
    """
    # Convert the Python dictionary back into a JSON string with double quotes
    # json_string = json.dumps(json_dict)
    # Now, convert single quotes to double quotes around JSON keys and string values
    # This is a naive approach and might need refinement based on your specific cases
    # Finally, escape newlines, carriage returns, and tabs in the "code" string value
    # This specifically targets the "code" key in your JSON structure
    def escape_special_characters(match):
        escaped_string = match.group(1).replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
        # Further escaping backslashes within the code content to ensure valid JSON
        return '"{}"'.format(escaped_string.replace('\\', '\\\\'))

    # json_string = re.sub(r'"code":\s*"((?:[^"\\]|\\.)*)"', escape_special_characters, json_string)
    return json_string

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
        if filename.endswith(".py"):  # TODO: probably should change this line soon
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                code_lines = file.readlines()
                code_with_line_numbers = "".join(f"{i+1}: {line}" for i, line in enumerate(code_lines))
                files_and_code += f"filename: {filename}, code:\n{code_with_line_numbers}\n"
    return files_and_code

def should_be_combined(t_i, d_i, t_j, d_j):
    prompt = f"You are given the following edits to make to a codebase: {t_i} and {t_j}. The description of {t_i} is {d_i}, and the description of {t_j} is {d_j}. Are these two tasks interconnected enough that it makes sense to combine them into one task in the planning segment? Answer 'yes' or 'no'."
    return make_gpt4_call(prompt)

def combine(t_i, d_i, t_j, d_j):
    prompt = f"You are given the tasks: {t_i} and {t_j}. The description of {t_i} is {d_i}, and the description of {t_j} is {d_j}. Combine {t_i} and {t_j} into one task."
    task = make_gpt4_call(prompt)
    prompt = f"You are given the tasks: {t_i} and {t_j}. The description of {t_i} is {d_i}, and the description of {t_j} is {d_j}. Combine {d_i} and {d_j} into one description."
    description = make_gpt4_call(prompt)
    return task, description

def find_file(codebase, task, description):
    prompt = f"You want to do task: {task} with description {description}. The current codebase is {codebase}. Please tell me what file(s) you want to add the code to in the following form: ['filename1', 'filename2', 'filename3']"
    return make_gpt4_call(prompt)

def new_file(codebase, task, description):
    res = ""
    while "yes" not in res.lower() and "no" not in res.lower(): 
        prompt = f"You want to do task: {task} with description {description}. The current codebase is {codebase}. Do you need to create a new file? ANSWER yes or no, ANSWER IN ONE WORD!"
        res = make_gpt4_call(prompt)
    if "yes" in res.lower():
        return True
    else:
        return False

def write_code_to_file(code_json, directory):
    # Ensure the 'alg_code' directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        code_json_fixed = fix_invalid_escapes(code_json)
        code_info = json.loads(code_json_fixed)
    except json.JSONDecodeError as e:
        print(f"JSON decode error (line 155): {e}")
        return -1 
    # Extract information from the JSON
    try:
        file_name = code_info.get("file_name")
        new = code_info.get("new")
        code = code_info.get("code")
        delete = code_info.get("delete", False)
        start_line_number = code_info.get("start_line_number", None)
        end_line_number = code_info.get("end_line_number", None)
    except:
        code_info = code_info[0]
        file_name = code_info.get("file_name")
        new = code_info.get("new")
        code = code_info.get("code")
        delete = code_info.get("delete", False)
        start_line_number = code_info.get("start_line_number", None)  
        end_line_number = code_info.get("end_line_number", None)      
    # Construct the full path to the file within the 'alg_code' directory
    file_path = os.path.join(directory, file_name)

    if delete and start_line_number is not None and end_line_number is not None:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Delete specified lines
            del lines[start_line_number-1:end_line_number]

            with open(file_path, 'w') as file:
                file.writelines(lines)

            print(f"Lines {start_line_number} to {end_line_number} deleted from '{file_name}'.")
        else:
            print(f"Cannot delete lines. File '{file_name}' does not exist.")
        return
    # Handling file creation or modification
    if new:
        with open(file_path, 'w') as file:
            file.write(code)
        print(f"File '{file_name}' has been successfully created/updated in '{directory}'.")
    else:
        # Read existing content if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Modify the content based on start_line_number
            if start_line_number is not None:
                # Ensure start_line_number is within the file size or append if it's larger
                while len(lines) < start_line_number:
                    lines.append("\n")
                lines[start_line_number-1:start_line_number-1] = [code + "\n"]

                # Write the modified content back
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                print(f"Code inserted starting from line {start_line_number} in file '{file_name}'.")
            else:
                # Append code if no start_line_number is provided
                with open(file_path, 'a') as file:
                    file.write("\n" + code)
                print(f"Code appended to existing file '{file_name}'.")
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

def main(file_path, MAX_ITER = 10):
    small_iter = 2
    sum_iter_convg, total_iter = 0, 0
    with open(file_path, 'r') as file:
        transcript_file = file.read()
    directory_name = 'cot_' + os.path.basename(file_path) + '_react' # make_gpt4_call('i am writing code to do the following task with this transcript file:' + transcript_file + 'what would be the best name for it. Give me exactly one name that captures what we are trying to do. Dont give me anything else. Strictly give one name and thats it.  This name will directly be the name of the directory with no modification (so no \')') + '_5'
    print(directory_name)
    os.makedirs(directory_name, exist_ok=True)
    tasks, descriptions = process_transcript_file(file_path)
    if len(tasks) != len(descriptions):
        raise ValueError("susssss.")
    for idx in range(len(tasks)):
        iter = 0
        should_do_task = True
        codebase = get_files_and_code(directory_name)

        task, description = tasks[idx], descriptions[idx]
        json_code = write_code(codebase, task, description)
        write_code_to_file(clean_json_string(json_code), directory_name)  
        """
        for idx in range(len(tasks)):
            # Iterate in reverse
            i = len(tasks) - idx - 1
            task, description = tasks[idx], descriptions[idx]

            # For each task, check if it should be combined with any other task
            for j in range(len(tasks)):
                res = should_be_combined(tasks[i], descriptions[i], tasks[j], descriptions[j]).lower()
                while (not "yes" in res and not "no" in res):
                    res = should_be_combined(tasks[i], descriptions[i], tasks[j], descriptions[j]).lower()

                # If yes, combine tasks
                if "yes" in res:
                    tasks[j], descriptions[j] = combine(tasks[i], descriptions[i], tasks[j], descriptions[j])
                    tasks.pop(i)
                    descriptions.pop(i)
                    break
        """
        update_files_with_cleaned_code(directory_name)
        test_json = clean_json_string(write_test(codebase=codebase,
                               task=task, 
                               description=description, 
                               directory_name=directory_name))
        threshold = 90 # TODO: calculate this based upon task. 
        write_code_to_file(clean_json_string(str(test_json)), directory_name)
        while (write_code_to_file(clean_json_string(str(test_json)), directory_name) == -1) and small_iter < 5:
            test_json = clean_json_string(write_test(codebase=codebase,
                               task=task, 
                               description=description, 
                               directory_name=directory_name))
            small_iter += 1
            print("in here")
            write_code_to_file(clean_json_string(json_code), directory_name)  
            update_files_with_cleaned_code(directory_name)

        update_files_with_cleaned_code(directory_name)
        
        # Check if the string already has square brackets
        """
        if not (test_json.startswith("[") and test_json.endswith("]")):
            # Add square brackets to make it a valid JSON array
            formatted_str = f"[{test_json}]"
        else:
            # If it's already formatted as an array, no need to add brackets
            formatted_str = test_json        
        for test_script in json.loads(formatted_str):
            print("the test script is")
            print(test_script)
            # write_code_to_file(clean_json_string(str(test_script)), directory_name)
        """
        command = json.loads(test_json)["commands"] 
        print("the command is")
        print(command)
        while should_do_task:
            codebase = get_files_and_code(directory_name)
            [percent_pass, result] = get_test_info(command)
            while percent_pass == -1 and small_iter < 5:
                test_json = clean_json_string(write_test(codebase=codebase,
                                task=task, 
                                description=description, 
                                directory_name=directory_name))
                write_code_to_file(clean_json_string(json_code), directory_name)  
                update_files_with_cleaned_code(directory_name)
                [percent_pass, result] = get_test_info(command)
                small_iter += 1
            print(percent_pass)
            json_code = write_code(codebase=codebase, 
                                   task=task, 
                                   description=description, 
                                   percent_pass=percent_pass, 
                                   result=result, 
                                   prev_generated_code=json_code)
            write_code_to_file(clean_json_string(json_code), directory_name) 
            update_files_with_cleaned_code(directory_name) 
            iter += 1
            # percent_pass = threshold + 0.01
            should_do_task = iter <= MAX_ITER and percent_pass < threshold
        sum_iter_convg += iter 
        total_iter += 1 

    print('iter' + str(iter))
    update_files_with_cleaned_code(directory_name)


