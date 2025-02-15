import subprocess
import json
import os
import numpy as np
import pandas as pd
from llm_helper import call_llm
from utils import read_file, write_file, list_files
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def read_tasks(file_path: str) -> pd.DataFrame:
    tasks = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            tokens = line.strip().split(None, 1)
            if len(tokens) < 2:
                continue
            task_type, description = tokens
            tasks.append((task_type, description))
    return pd.DataFrame(tasks, columns=["TaskType", "Description"])

def get_top_similar_tasks(app: object, query: str):
    data = read_tasks("tasks.txt")
    query_embedding = app.state.model.encode([query])
    similarity = cosine_similarity(app.state.embeddings, query_embedding).flatten()
    most_similar = np.argsort(similarity)[-3:][::-1]
    return data.iloc[most_similar].assign(Score=similarity[most_similar])

def execute_task(embeddings: object, task: str) -> str:
    toptasks = get_top_similar_tasks(embeddings, task)
    first_task_type = toptasks.iloc[0, 0]
    print(first_task_type)
    print(toptasks)
    with open('schema.json', 'r') as file:
        schema = json.load(file)
    """Parses and executes the given task."""
    match first_task_type:
        case "A1.":
            params = call_llm(task, schema["task_schema"]["A1."])
            return params
            #return install_uv_and_run_script(params)
        case "A2.":
            params = call_llm(task, schema["task_schema"]["A2."])
            return params
            #return format_markdown(params)
        case "A3.":
            params = call_llm(task, schema["task_schema"]["A3."])
            return params
            #return count_wednesdays(params)
        case "A4.":
            params = call_llm(task, schema["task_schema"]["A4."])
            return params
            #return sort_contacts(params)
        case "A5.":
            params = call_llm(task, schema["task_schema"]["A5."])
            return params
            #return process_logs(params)
        case "A6.":
            params = call_llm(task, schema["task_schema"]["A6."])
            return params
            #return index_markdown_files(params)
        case "A7.":
            params = call_llm(task, schema["task_schema"]["A7."])
            return params
            #return extract_email(params)
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
            return params
            #return calculate_ticket_sales(params)
        case _:
            raise ValueError("Unsupported task description.")

def install_uv_and_run_script(params: json) -> str:
    subprocess.run(["pip", "install", "uv"], check=True)
    email = extract_argument(task)
    script_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    subprocess.run(["python", "-m", "urllib.request", "", script_url, email], check=True)
    return "Data generation script executed successfully."

def format_markdown(task: str) -> str:
    query = (
        "understand the task as described in the line below. \n"
        + json.dumps(task)
        + "\nNow you need to identify the filename of the markdown file that needs to be formatted. "
        + "Output your answer as a json object with the key 'filename' and the value as the filename."
    )
    response = call_llm(query)
    file_path = json.loads(response)["filename"]
    subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], check=True)
    return "Markdown file formatted successfully."

def count_wednesdays(task: str) -> str:
    from datetime import datetime
    with open("/data/dates.txt", "r") as f:
        dates = f.readlines()
    count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)
    write_file("/data/dates-wednesdays.txt", str(count))
    return "Counted Wednesdays successfully."

def sort_contacts(task: str) -> str:
    contacts = json.loads(read_file("/data/contacts.json"))
    contacts.sort(key=lambda c: (c["last_name"], c["first_name"]))
    write_file("/data/contacts-sorted.json", json.dumps(contacts, indent=2))
    return "Contacts sorted successfully."

def process_logs(task: str) -> str:
    log_files = sorted(list_files("/data/logs/", ".log"), key=os.path.getmtime, reverse=True)[:10]
    log_lines = [read_file(log).splitlines()[0] for log in log_files if read_file(log)]
    write_file("/data/logs-recent.txt", "\n".join(log_lines))
    return "Processed log files successfully."

def index_markdown_files(task: str) -> str:
    md_files = list_files("/data/docs/", ".md")
    index = {}
    for md_file in md_files:
        lines = read_file(md_file).splitlines()
        title = next((line[2:] for line in lines if line.startswith("# ")), "Untitled")
        index[os.path.basename(md_file)] = title
    write_file("/data/docs/index.json", json.dumps(index, indent=2))
    return "Markdown index created successfully."

def extract_email(task: str) -> str:
    content = read_file("/data/email.txt")
    email = call_llm("Extract sender's email from this text:", content)
    write_file("/data/email-sender.txt", email)
    return "Extracted sender's email successfully."

def extract_credit_card(task: str) -> str:
    card_text = call_llm("Extract credit card number from this image:", image_path="/data/credit-card.png")
    write_file("/data/credit-card.txt", card_text.replace(" ", ""))
    return "Extracted credit card number successfully."

def find_similar_comments(task: str) -> str:
    comments = read_file("/data/comments.txt").splitlines()
    most_similar = call_llm("Find the most similar pair of comments:", comments)
    write_file("/data/comments-similar.txt", "\n".join(most_similar))
    return "Identified similar comments successfully."

def calculate_ticket_sales(task: str) -> str:
    import sqlite3
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0
    write_file("/data/ticket-sales-gold.txt", str(total_sales))
    conn.close()
    return "Calculated total sales for 'Gold' ticket type successfully."

def extract_argument(task: str) -> str:
    """Extracts the user email argument from the task description using LLM."""
    email = call_llm("Extract the email from this text:", task)
    return email.strip()