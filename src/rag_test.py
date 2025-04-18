import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import streamlit as st

from dotenv import load_dotenv
import os
import pypdf

load_dotenv()
# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


    
pdf_paths = ["report-to-members-2023.pdf","universal_guide_to_benefits.pdf","MCGuideandUSAAPlatMC.pdf"]
# Load data from a text file
#loader = TextLoader("data.txt")
all_data = []
for pdf_path in pdf_paths:
    loader = PyPDFLoader(pdf_path)
    data_file = loader.load()
    all_data.extend(data_file)

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = text_splitter.split_documents(all_data)

# Create embeddings using Google Gemini
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Store embeddings in a vector store (FAISS)
vectorstore = FAISS.from_documents(all_splits, embeddings)

# Initialize the Gemini chat model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# Create a retrieval-based question answering chain
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Function to process user queries
st.set_page_config(layout="wide", page_title="Chatbot", page_icon=":robot_face:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt := st.chat_input("Ask me usaa question"):
    st.chat_message("User:").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = qa_chain({"query": prompt})
    with st.chat_message("Assistant:"):
        st.markdown(response["result"])
    st.session_state.messages.append({"role": "assistant", "content": response["result"]})
