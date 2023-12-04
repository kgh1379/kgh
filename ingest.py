import streamlit as st
import openai

from langchain.document_loaders import NotionDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import faiss

# Load OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

loader = NotionDirectoryLoader("notion_content")
documents = loader.load()

#Split the Notion content into smaller chunks
markdown_splitter = RecursiveCharacterTextSplitter(
    separators=["#","##", "###", "\\n\\n","\\n", "."],
    chunk_size =1500,
    chunk_overlap=100
)
docs = markdown_splitter.split_documents(documents)

# Initialize OpenAI embedding model

embeddings = OpenAIEmbeddings()

# Convert all chunks into vectors embeddings using Open AI embeddings
# Store all vectors in FAISS index and save to local folder
db = FAISS.from_documtns(docs, embeddings)
db.save_local("faiss_index")

print('Local FAISS index has been successfully saved.')
