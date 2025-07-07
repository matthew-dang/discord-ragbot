import os
import faiss
import logging
import numpy as np
import requests
import re
from dotenv import load_dotenv

from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

AZURE_EMBEDDING_ENDPOINT = os.getenv("AZURE_EMBEDDING_ENDPOINT")
AZURE_EMBEDDING_KEY = os.getenv("AZURE_EMBEDDING_KEY")

DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

embedding_client = EmbeddingsClient(
    endpoint=AZURE_EMBEDDING_ENDPOINT,
    credential=AzureKeyCredential(AZURE_EMBEDDING_KEY)
)

dimension = 1536
index = faiss.IndexFlatL2(dimension)
docs = []

def get_embedding(text: str):
    logging.debug(f"Generating embedding for: {text[:60]}...")
    try:
        response = embedding_client.embed(input=[text])
        logging.info("Embedding generated successfully.")
        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        logging.error(f"Embedding generation failed: {str(e)}")
        raise

def ingest_documents():
    logging.info("Starting document ingestion...")
    with open("data/docs.txt", "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            if clean:
                try:
                    emb = get_embedding(clean)
                    index.add(np.array([emb]))
                    docs.append(clean)
                except Exception as e:
                    logging.warning(f"Failed to embed line: {clean[:60]}... | Error: {str(e)}")
    logging.info("Document ingestion complete.")

def retrieve_chunks(question: str, k=3):
    logging.info(f"Retrieving top {k} chunks for question: {question}")
    query_vec = get_embedding(question)
    D, I = index.search(np.array([query_vec]), k)
    results = [docs[i] for i in I[0]]
    logging.debug(f"Top chunks: {results}")
    return results

def generate_answer(question: str, chunks: list[str]):
    logging.info(f"Generating answer for question: {question}")
    context = "\n".join(chunks)
    prompt = f"Use this context to answer:\n{context}\n\nQuestion: {question}"

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for AI Bootcamp interns."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": DEEPSEEK_API_KEY
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        logging.info("Successfully received response from LLM.")
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"[DeepSeek Error]: {str(e)}")
        return f"[DeepSeek Error]: {str(e)}"

def extract_answer(response_text):
    return re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()

def run_rag_pipeline(question: str):
    logging.info("Running full RAG pipeline.")
    if len(docs) == 0:
        logging.info("Docs not loaded yet. Ingesting documents...")
        ingest_documents()

    top_chunks = retrieve_chunks(question)
    answer = generate_answer(question, top_chunks)
    logging.info("RAG pipeline completed successfully.")
    return answer, top_chunks