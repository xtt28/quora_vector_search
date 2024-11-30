# Welcome to the source repository of quora_vector_search.

Get Quora question search results from a broad query using vector search.
Powered by pgvector for Postgres and all-MiniLM-L6-v2 embeddings model.

## Getting Started

### Prerequisites

- Python 3
- PostgreSQL database
- pgvector Postgres extension - follow the instructions at
  https://github.com/pgvector/pgvector to get up and running with the extension
- Quora questions dataset — A plain text file with one question per line. Save
  it as dataset_quora_questions.txt. I used the question1 column of this Kaggle
  dataset: https://www.kaggle.com/datasets/sambit7/first-quora-dataset

### Instructions

#### Database

Prepare your PostgreSQL database by running the commands in schema.sql in the
database shell.

Make a copy of template.env, rename it to .env, and populate it with the info
of your PostgreSQL database.

#### Workspace

Create a virtual environment: `python3 -m venv .venv`  
Activate the virtual environment in the manner according to your OS/platform.

Install project dependencies: `pip install -r requirements.txt`

#### Embeddings

Run the script embeddings_generate.py. This will read the dataset in the file
dataset_quora_questions.txt, generate embeddings for the questions, and store
the questions along with their embeddings in the PostgreSQL database with the
pgvector extension.

> [!IMPORTANT]
> By default, the script only considers the first 10,000 lines of the dataset
> for the sake of my own computer. If you want to use the full dataset, replace
> `for line in lines[:10_000]:` with `for line in lines:` in the
> embeddings_generate.py script.

#### Running the REST API

After performing the previous step, execute the shell script start_server.sh to
start the question search REST API, then visit the URL printed in the console.

You can search for a question by making a GET request to:
`https://<URL>/search/Your+question+goes+here`

The top 5 results from the database will be returned. Example response:
```json
{"results":[["How can I speed up my Internet connectionn?"],["How can I increase the traffic to a website?"],["How can I increase the traffic to my website?"],["How can I increase the speed of my internet connection while using a VPN?"],["How do I  increase traffic on my site?"]]}
```

## License

MIT