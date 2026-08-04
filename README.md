# Preliminary-Test-for-the-internship
## Preliminary Test for AI/Automation &amp; Infrastructure Internship

----------------------------------------------------------
## Answers to Part 2:
Comment: I kept the entire code and wrote comments directly under the mistakes. 

import sqlite3
import requests

DB_PATH = "app.db"
API_KEY = "sk-prod-abc123xyz" # hardcoded
# This is a very unsafe way of handling API key, making it be exposed to anyone with an access to the repository/code file. These keys needs to be stored 
# outside of the code, like environment variables or a secrets management system.

def search_documents(question):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  query = "SELECT id, title, content FROM documents WHERE content LIKE '%" + question + "%'"
  cursor.execute(query)
# This creates a possible issue with SQL, because user input is directly inserted into the SQL query,
# where a malicious user could manipulate the quesry and possibly access data. 
# User input should be treated as data, instead of an executable SQL code - using parameterized SQL with placeholders in the actual query. 
  
  rows = cursor.fetchall()
  conn.close()
  return rows

def ask_llm(question, docs):
  context = ""
  for doc in docs:
    context += doc[2] + "\n\n"
# Techically, its not a mistake, but it sends every(!) retrieved document's content to the LLM as part of the prompt.
# However, it becomes a problem when the amount of documents is huge, and can become very inefficent and can increase the token usage
# of the LLM or can fail if the amount of tokens is not enough. 
# A better approach would be using RAG with chunking, embeddings and retrieving only the most relevant documents (ex. best 10 instead of all of them) 
  
  prompt = f"Context:\n{context}\n\nQuestion: {question}"
  response = requests.post(
    "https://api.example.com/v1/generate",
    json={"model": "some-model", "prompt": prompt},
    headers={"Authorization": f"Bearer {API_KEY}"}
  )
  return response.json()["response"]

def save_answer(question, answer):
  conn = sqlite3.connect(DB_PATH)
  conn.execute(
    "INSERT INTO answers (question, answer) VALUES ('" + question + "', '" + answer + "')"
  )
  # THe same issue as before with direct insert of the user input in the query, that can be very unsafe for the data. 
  # A proper fix of the issue is using parameterized SQL with placeholders in the actual query. 
  
  conn.commit()
  conn.close()

if __name__ == "__main__":
  q = input("Ask: ")
  docs = search_documents(q)
  print(ask_llm(q, docs))
  save_answer(q, ask_llm(q, docs)) # called twice
# The LLM is called two times for the same question, which wastes time and tokens, creating more than one issue. 
# Instead, the response should be stored in a variable once to not lose it and then reused for printing and saving. 


----------------------------------------------------------
## Answers to Part 3:
Comment: I used more natural language to explain my answers, and in the Q2 referenced the comment from Part 2!

Q1. The script above uses SQLite with a LIKE '%...%' search. If you switch to Postgres
and the documents table grows to 1,000,000 rows, what becomes slow or risky first?
What would you do about it?
  The LIKE '%...%' search means that the query will go through all of the data to check what will contain the word between %, making a full table scan and
becoming an issue with huge document amount significantly slowing down the searching process. I believe that it would be better to add proper index and maybe 
full-text search to make it better. Also a pgvector can be useful, however I haven't had any experience with that and will need to read and practice on how to work with it. 


Q2. The script sends all found documents into the prompt. Why is this a bad idea once
you have many documents? Briefly describe how a basic RAG approach (chunking +
embeddings + top-k) would fix this. You don't need to write code.
  As mentioned previously, such solution is not only time consuming, but also expensive (tokens). A RAG approach splits the documents into smaller
chunks, converts them into embeddings with their meaning, retrieve only the most relevant chunks using top-k similarity search and only those 
will be further send to the LLM.


Q3. The LLM call has no error handling. Name 3 things that can go wrong when calling
an external LLM API, and for each — how you would handle it in production.
  The top three issues i can recall network issues, API rate limit and overall server error. Network failure usually caused by either taking too long to respond or 
internet connection drops - to fix it needs to be done a timeout and retry. API rate limits is caused by too many requests, the solution is simple - wait 
and retry(2s -> 4s -> 8s -> ...). As for the server error caused on the server side - log the information (details of the error) and provide a message to the users
on the screen (example).

Q4 (bonus, optional). Imagine this becomes a chatbot that remembers user history.
What 1-2 Postgres tables would you create? A short schema sketch or plain words —
both fine.
  In my opinion useful would be creating a users table to store basic information about each user (ex.: user_id and email). And basing on the previous tasks, 
creating a messages table with user_id, message content, email and a timestamp. The two tables are connected and can be easily used to provide the information for 
the chatbot. 
