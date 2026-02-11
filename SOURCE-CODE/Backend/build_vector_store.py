                         #**************2nd file to execute*************



from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import json

import os



#============================load chunks from jsonl file=======================================

def load_chunks(jsonl_file):
    documents = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            documents.append(Document(page_content=item['text']))
    return documents



#===============================convert docs into vector embeddings============================
                         #create faiss for fast similarity search

def build_vector_store(docs, faiss_path="vector_store"):
    # embeddings = GPT4AllEmbeddings()                     # this help to convert text into number
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)          #in docs ,list of object is in document formate with page content
    db.save_local(faiss_path)
    print(f"✅ FAISS vector store saved to: {faiss_path}")



#==================================main method where execution is started==========================

if __name__ == "__main__":
    jsonl_file = "knowledge_base.jsonl"
    vectorstore_path = "vector_store"

    if not os.path.exists(jsonl_file):
        print("❌ knowledge_base.jsonl not found.")
    else:
        docs = load_chunks(jsonl_file)
        build_vector_store(docs, vectorstore_path)
