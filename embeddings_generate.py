from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

import os
import psycopg2.pool

with open("dataset_quora_questions.txt") as f:
    global lines
    lines = f.readlines()
    
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

count = 0

# Here, we use the first 10,000 entries in the dataset to expedite the embedding
# generation process.
for line in lines[:10_000]:
    line = line.replace("\n", "")
    embedding = model.encode(line)
    cur.execute("INSERT INTO questions (question, embedding) VALUES (%s, %s)", (line, embedding))
    count += 1
    print(count)

conn.commit()