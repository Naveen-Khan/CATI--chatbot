import json 
import fitz
import os
import re # for text processing
from langchain.text_splitter import RecursiveCharacterTextSplitter



# ========================text extraction===========================================

def extract_text_from_pdfs(pdf_folder):
    all_text= ""
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path=os.path.join(pdf_folder,filename)
            doc=fitz.open(pdf_path)
            for page in doc:
                all_text += page.get_text()
            print("✅ extrated text done")
    return all_text

# =====================================preprocessing text  =======================================

def preprocess(text):
    text=re.sub (r'\n+','\n',text)  # remove extra line into single
    text=re.sub(r'\s{2,}',' ',text)  # remove 2 space into single
    text=re.sub(r'\t', '',text)       # remove tab in text
    return text.strip()

#=====================================chunnking===============================================
def chunk_pdf(text,chunk_size=500,overlap=100):
    splitter=  RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=overlap)
    chunks=splitter.split_text(text)
    print(f"total chunks created {len(chunks)}")
    return chunks



#===============================================usage====================================================

#   1. extract text from pdfs
pdf_folder="pdfs"
text =extract_text_from_pdfs(pdf_folder)

#2. preprocess text
text=preprocess(text)

# 3. apply cunkking chunks function
chunks=chunk_pdf(text)

# 4. save in json formate 



#=============================save cunks in josonl file ===============================================

output_path="knowledge_base.jsonl"
with open(output_path,"w",encoding="utf-8") as f:
    for i,chunk in enumerate(chunks):
        json.dump({
            "chunks_id":f"chunk_{i}",
            "text":chunk,
            
        },f)
        f.write("\n")
    print(f"saved chunks {len(chunks)} to {output_path}")
