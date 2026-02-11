import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

app = FastAPI()

# === Load FAISS Vector Store ===
vectorstore_path = "vector_store"
if not os.path.exists(vectorstore_path):
    raise Exception("❌ FAISS vector store not found. Run build_vectorstore.py first.")

print("📂 Loading FAISS vector store...")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(vectorstore_path, embedding, allow_dangerous_deserialization=True)
print("✅ Vector store loaded.")

# === Set Groq API Key ===
GROQ_API_KEY = "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"  # 🔴 Replace with your key

# === Input Schema ===
class Question(BaseModel):
    question: str

# === Groq Request Function ===
def ask_groq_mistral(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model":"meta-llama/llama-4-maverick-17b-128e-instruct",
     # or use "mistral-7b-8k" if preferred
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("❌ Groq API Error:", response.text)
        return "An error occurred while generating a response."

# ======================================================= API Endpoint =======================================================
@app.post("/ask")
def ask_question(q: Question):
    relevant_docs = vectorstore.similarity_search(q.question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
Use the company knowledge below to answer the user's question.

Company Knowledge:
{context}

User Question:
{q.question}
"""
    answer = ask_groq_mistral(prompt)
    return {"answer": answer}
