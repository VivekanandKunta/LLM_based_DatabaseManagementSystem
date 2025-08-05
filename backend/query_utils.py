import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def query_generator(loc: str):
    with open(loc, "r") as file:
        return file.read()

def get_db_connection(config):
    return psycopg2.connect(
        dbname=config.database,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port
    )

def run_query(config, sql_query: str):
    conn = get_db_connection(config)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    conn.commit()
    cursor.close()
    conn.close()
    return df

def get_schema(config):
    schema_sql = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """
    df = run_query(config, schema_sql)

    schema = {}
    schema_text = ""
    for _, row in df.iterrows():
        table = row["table_name"]
        column = row["column_name"]
        dtype = row["data_type"]
        schema.setdefault(table, []).append((column, dtype))

    for table_name, columns in schema.items():
        schema_text += f"Table: {table_name}\n"
        schema_text += "Columns:\n"
        for col_name, data_type in columns:
            schema_text += f"- {col_name} ({data_type})\n"
        schema_text += "\n"

    return schema_text.strip(), schema

def generate_sql_query(schema_text: str, instruction: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
    Given the following database schema:
    {schema_text}

    Generate an SQL query based on this instruction:
    {instruction}

    Return only the query nothing more  in thid pattern ```sql ... ``` markers.
    """

    response = model.generate_content(prompt)
    return response.text

def extract_sql_content(query_text: str):
    import re
    match = re.search(r"```sql\s*(.*?)\s*```", query_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return query_text.strip()
