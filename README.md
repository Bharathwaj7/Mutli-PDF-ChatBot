# Save the README content as a file

readme_content = """
# 📄 Chat with PDF using Groq

## 📋 Overview

Interact with your PDF documents using a conversational AI powered by Groq's cutting-edge LLMs and Streamlit!  
Built for document understanding, question answering, and real-time knowledge extraction. 🚀

## ✨ Features

- **Multi-PDF Upload**  
  Upload one or several PDF documents at once for combined analysis. 📄
  
- **Dynamic Chunking**  
  Automatically adjusts the text split size based on document size for optimized retrieval. 🔄

- **Embeddings-Based Search**  
  Create vector representations of document chunks using Sentence Transformers. 🧠

- **Groq Model Selection**  
  Choose from a wide range of high-performance Groq models for answering your queries. 🤖

- **First-Time Setup Auto-Install**  
  Automatically installs missing Python packages if they aren't detected. ⚙️

- **Streamlit Interface**  
  Clean, minimal, and interactive web UI for uploading files and chatting. 💻

- **Environment Configurable**  
  Manage API keys and settings easily via `.env` files. 🔑

## 🔧 Technical Stack

### Backend
- **LangChain**: Document loading, splitting, retrieval, and QA chains. 🔗
- **FAISS**: High-performance local vector store for fast similarity search. ⚡
- **Sentence Transformers**: Embedding generation via Hugging Face. 💬
- **PyPDF2**: PDF parsing and text extraction. 📑
- **Groq API**: Hosted LLM access for chat generation. 🌐

### Frontend
- **Streamlit**: Real-time web UI for uploads, processing, and question answering. 🖥️

### Infrastructure
- **Python-dotenv**: Environment variable management. 🛠️
- **Subprocess / pip Auto-Installer**: First-time dependency management. 📦

## 🚀 Getting Started

### 1. Clone the Repo  
```bash
git clone https://github.com/yourusername/chat-with-pdf-groq.git
cd chat-with-pdf-groq
```
### 2. Create & Activate Virtual Env  
```bash
python3 -m venv venv
source venv/bin/activate
``` 
### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```
### 4. Set Environment Variables
```bash
Create a .env file in the project root with your Groq API key
GROQ_API_KEY=your-groq-api-key-here
```
### 5. Run the App
```bash
streamlit run app.py
```

## 📚 Models Supported
- qwen-qwq-32b
- deepseek-r1-distill-llama-70b
- gemma2-9b-it
- compound-beta
- compound-beta-mini
- llama-3.1-8b-instant
- llama3-70b-8192
- meta-llama/llama-4-maverick-17b-128e-instruct
- mistral-saba-24b
- whisper-large-v3
- allam-2-7b
- and more... 🧑‍💻
