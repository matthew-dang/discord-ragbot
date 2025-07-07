# Discord RAG Bot

A Retrieval-Augmented Generation (RAG) Discord bot that answers user questions using vector search and LLMs.

## Overview

This bot uses:
- **FAISS** for fast vector similarity search
- **Azure Inference SDK** to generate document embeddings
- **DeepSeek LLM** to answer questions based on retrieved context
- **FastAPI** to expose the RAG pipeline as an API
- **Discord.py** to interact with users on Discord
- **Render** + **Docker** for deployment

## How It Works

1. Text documents are embedded and indexed with FAISS.
2. When a user asks a question, the backend:
   - Embeds the query
   - Retrieves the most relevant chunks
   - Sends the context + question to DeepSeek
3. The LLM returns an answer, and the bot replies in the channel.

## Tech Stack

- Python, FastAPI
- FAISS, Azure AI Inference, DeepSeek
- Discord.py
- Docker
- Render

## Setup

### Prerequisites

- Python 3.10+
- Docker (optional for deployment)
- Discord bot token
- Azure embedding endpoint/key
- DeepSeek API key

### Install & Run Locally

```bash
git clone https://github.com/your-username/discord-ragbot.git
cd discord-ragbot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt