import os

db_config = {
    'user': os.environ["DB_USER"],
    'password': os.environ["DB_PASS"],
    'host': os.environ["DB_HOST"],
    'database': os.environ["DB_DATABASE"],
    'port': os.environ["DB_PORT"]
}

open_ai_key = os.environ["OPENAI_API_KEY"]