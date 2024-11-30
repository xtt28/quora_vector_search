from dotenv import load_dotenv
from fastapi import FastAPI
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

import os
import psycopg2.pool

load_dotenv()

pool = psycopg2.pool.SimpleConnectionPool(
    2, 3,
    user=os.getenv("QUORA_DB_USER"),
    password=os.getenv("QUORA_DB_PASS"),
    host=os.getenv("QUORA_DB_HOST"),
    port=os.getenv("QUORA_DB_PORT"),
    database=os.getenv("QUORA_DB_NAME")
)
conn = pool.getconn()

cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI()

@app.get("/search/{query}")
def search(query: str):
    embedding = model.encode(query)

    cur.execute('SELECT question FROM questions ORDER BY embedding <-> %s LIMIT 5', (embedding,))
    return {"results": cur.fetchall()}