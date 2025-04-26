import streamlit as st
# Set page config as the very first Streamlit command
st.set_page_config(page_title="Chat PDF")

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Check if packages are already installed by looking for a flag file
install_flag_file = Path(".packages_installed")
if not install_flag_file.exists():
    # Package installation section - runs only once
    st.info("First-time setup: Installing required packages...")
    required_packages = [
        "sentence-transformers",
        "PyPDF2",
        "langchain",
        "langchain_community",
        "langchain_groq",
        "faiss-cpu"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_").split("_")[0])
        except ImportError:
            st.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            st.success(f"Successfully installed {package}")
    
    # Create flag file to mark that installation has been done
    with open(install_flag_file, "w") as f:
        f.write("Packages installed successfully")
    
    st.success("All required packages have been installed! The app is ready to use.")

# Now import the rest of the packages
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# List all available Groq (and other) models for selection
AVAILABLE_MODELS = [
    "qwen-qwq-32b",
    "deepseek-r1-distill-llama-70b",
    "gemma2-9b-it",
    "compound-beta",
    "compound-beta-mini",
    "distil-whisper-large-v3-en",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "llama-guard-3-8b",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "mistral-saba-24b",
    "whisper-large-v3",
    "whisper-large-v3-turbo",
    "playai-tts",
    "playai-tts-arabic",
    "allam-2-7b",
]

def get_pdf_text(pdf_docs):
    text = ""
    total_bytes = 0
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text() or ""
            text += page_text
        # accumulate file size
        pdf.seek(0, os.SEEK_END)
        total_bytes += pdf.tell()
        pdf.seek(0)
    return text, total_bytes


def compute_chunk_size(text_length, total_bytes):
    # Heuristic: target ~20 chunks, constrain between 1000 and 5000 chars
    target_chunks = 20
    estimated = max(text_length // target_chunks, 1000)
    return min(estimated, 5000)


def get_text_chunks(text, total_bytes):
    # Automatically compute chunk size based on text length and file size
    text_length = len(text)
    chunk_size = compute_chunk_size(text_length, total_bytes)
    overlap = int(chunk_size * 0.1)
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_text(text)
    return chunks, chunk_size


def get_embeddings():
    # Using Sentence Transformers for free embeddings
    model_name = "all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)


def get_vector_store(text_chunks):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def make_qa_chain(model_name):
    prompt_template = """
    Answer based on this context only. If answer isn't in context, say "answer not available in context".
    
    Context: {context}
    Question: {question}
    
    Answer:
    """
    model = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=0.3,
        max_tokens=1000
    )
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)


def user_input(user_question):
    embeddings = get_embeddings()
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(user_question, k=3)
    try:
        chain = make_qa_chain(st.session_state.selected_model)
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        st.write("**Reply:**", response["output_text"])
    except Exception as e:
        st.error(f"Error: {e}")
        st.warning("The document might be too large for processing. Try uploading smaller files or asking more targeted questions.")


def main():
    st.header("Chat with PDF using Groq 💁")
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and click 'Process'", accept_multiple_files=True
        )
        st.subheader("Model Selection")
        st.session_state.selected_model = st.selectbox(
            "Choose a model:", AVAILABLE_MODELS, index=0
        )
        if st.button("Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF file.")
                return
            with st.spinner("Processing..."):
                raw_text, total_bytes = get_pdf_text(pdf_docs)
                text_chunks, auto_chunk = get_text_chunks(raw_text, total_bytes)
                st.info(f"Computed chunk size: {auto_chunk} characters, generated {len(text_chunks)} chunks.")
                get_vector_store(text_chunks)
                st.success("Indexing complete! You can now ask questions.")
    user_question = st.text_input("Ask a question based on the uploaded PDFs:")
    if user_question and 'selected_model' in st.session_state:
        user_input(user_question)

if __name__ == "__main__":
    main()
