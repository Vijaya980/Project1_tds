import subprocess
import json
import os
from llm_helper import call_llm, call_llm_prompt, parse_llm_output
from utils import read_file, write_file, list_files
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
system_message_for_classifier = read_file("task_classifier_system_message.txt")

def execute_task(task: str) -> str:
    response = call_llm_prompt(task, system_message_for_classifier)
    json_response, python_response = parse_llm_output(response)
    
    task_type = json_response["task"] #read first word of the response
    first_task_type = task_type.split()[0] + "." #read first word of the response

    with open('schema.json', 'r') as file:
        schema = json.load(file)
    """Parses and executes the given task."""
    match first_task_type:
        case "A1.":
            params = call_llm(task, schema["task_schema"]["A1."])
            return install_uv_and_run_script(params)
        case "A2.":
            params = call_llm(task, schema["task_schema"]["A2."])
            return format_markdown(params)
        case "A3.":
            params = call_llm(task, schema["task_schema"]["A3."])
            return count_days(params)
        case "A4.":
            params = call_llm(task, schema["task_schema"]["A4."])
            return sort_contacts(params)
        case "A5.":
            params = call_llm(task, schema["task_schema"]["A5."])
            return process_logs(params)
        case "A6.":
            params = call_llm(task, schema["task_schema"]["A6."])
            return index_markdown_files(params)
        case "A7.":
            params = call_llm(task, schema["task_schema"]["A7."])
            return extract_email(params, schema["task_schema"]["EMAIL."])
        case "A8.":
            params = call_llm(task, schema["task_schema"]["A8."])
            return params
            #return extract_credit_card(params)
        case "A9.":
            params = call_llm(task, schema["task_schema"]["A9."])
            return params
            #return find_similar_comments(params)
        case "A10.":
            params = call_llm(task, schema["task_schema"]["A10."])
            return execute_sql(params)
        case _:
            raise ValueError("Unsupported task description.")

def install_uv_and_run_script(params: json) -> str:
    logger.info("Installing uv and running script." + str(params))
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["pip", "install", "faker"], check=True)
    logger.info("Installed uv and faker.")
    email = params["user_email"]
    script_url = params["python_script_url"]
    # execute the remote script with the user email as an argument
    try:
        subprocess.run(
            ["python", "-c", 
            f"import urllib.request; urllib.request.urlretrieve('{script_url}', 'script.py'); "
            f"import subprocess; subprocess.run(['python', 'script.py', '{email}'])"], 
            check=True
        )
        logger.info("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while executing the script: {e}")
        raise e
    return "Data generation script executed successfully."

def format_markdown(params: json) -> str:
    logger.info("Formatting Markdown file." + str(params))
    input_file = params["input_file"]
    format_tool = params["format_tool"]
    subprocess.run(["npx", "install", "-g", format_tool], check=True)
    subprocess.run([format_tool, "--write", input_file], check=True)
    return "Formatted Markdown file successfully."

def count_days(params: json) -> str:
    logger.info("Counting days." + str(params))
    from datetime import datetime
    input_file = params["input_file"]
    outout_file = params["output_file"]
    day_of_week = params["day_of_week"] # e.g., "Wednesday"
    dates_file_content = read_file(input_file)
    resp = call_llm_prompt("Just answer a number. no explnations. Count the number of days in the file that are a " + day_of_week + "." + "\n" + dates_file_content)
    write_file(outout_file, resp)
    return "Counted Days successfully."

def sort_contacts(params: json) -> str:
    logger.info("Sorting contacts." + str(params))
    input_file = params["input_file"]
    outout_file = params["output_file"]
    sorting_params_in_order_array = params["sorting_params_in_order_array"]

    contacts = json.loads(read_file(input_file))
    contacts.sort(key=lambda c: tuple(c[param] for param in sorting_params_in_order_array))
    write_file(outout_file, json.dumps(contacts, indent=2))
    return "Contacts sorted successfully."

def process_logs(params: json) -> str:
    logger.info("Processing logs." + str(params))
    which_line_number = params["which_line_number"]
    how_many_files = params["how_many_files"]
    file_extension = params["file_extension"]
    file_folder = params["file_folder"]
    output_file = params["output_file"]
    log_files = sorted(list_files(file_folder, file_extension), key=os.path.getmtime, reverse=True)[:how_many_files]
    log_lines = [read_file(log).splitlines()[which_line_number] for log in log_files if read_file(log)]
    write_file(output_file, "\n".join(log_lines))
    return "Processed log files successfully."

def index_markdown_files(params: json) -> str:
    logger.info("Indexing Markdown files." + str(params))
    md_files = list_files(params["input_folder"], params["file_type"])
    index = {}
    for md_file in md_files:
        lines = read_file(md_file).splitlines()
        title = next((line[2:] for line in lines if line.startswith("# ")), "Untitled")
        index[os.path.basename(md_file)] = title
    write_file(params["output_file"], json.dumps(index, indent=2))
    return "Markdown index created successfully."

def extract_email(params: json, schema: json) -> str:
    logger.info("Extracting email." + str(params))
    content = read_file(params["input_file"])
    isSender = params["is_sender"]
    isReceiver = params["is_receiver"]
    isCC = params["is_cc"]
    isBCC = params["is_bcc"]
    isTo = params["is_to"]

    parsed_email_json = call_llm(content, schema)
    response = ""
    if isSender: response += str(parsed_email_json.get("from", ""))
    elif isReceiver: response += str(parsed_email_json.get("to", ""))
    elif isCC: response += str(parsed_email_json.get("cc", ""))
    elif isBCC: response += str(parsed_email_json.get("bcc", ""))
    elif isTo: response += str(parsed_email_json.get("to", ""))

    write_file(params["output_file"], response)
    return "Extracted email successfully."

def extract_credit_card(params: json) -> str:
    logger.info("Extracting credit card." + str(params))
    card_text = call_llm("Extract credit card number from this image:", image_path="/data/credit-card.png")
    write_file("/data/credit-card.txt", card_text.replace(" ", ""))
    return "Extracted credit card number successfully."

def find_similar_comments(params: json) -> str:
    logger.info("Finding similar comments." + str(params))
    comments = read_file("/data/comments.txt").splitlines()
    most_similar = call_llm("Find the most similar pair of comments:", comments)
    write_file("/data/comments-similar.txt", "\n".join(most_similar))
    return "Identified similar comments successfully."

def execute_sql(params: json) -> str:
    import sqlite3
    logger.info("Executing SQL." + str(params))
    conn = sqlite3.connect(params["db_file"])
    cursor = conn.cursor()
    cursor.execute(params["sql_query"])
    total_sales = cursor.fetchone()[0] or 0
    write_file(params["output_file"], str(total_sales))
    conn.close()
    return "Calculated total sales for 'Gold' ticket type successfully."

def extract_argument(task: str) -> str:
    """Extracts the user email argument from the task description using LLM."""
    email = call_llm("Extract the email from this text:", task)
    return email.strip()