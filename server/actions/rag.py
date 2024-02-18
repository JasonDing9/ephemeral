from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import pickle
from dotenv import load_dotenv
import os.path

load_dotenv()

def ingestion(file="context.txt", name="context"):
    # Load Data
    loader = UnstructuredFileLoader(file)
    raw_documents = loader.load()

    # Split text
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)

    # Load Data to vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open(f"{name}-vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

def query(query, file="context-vectorstore.pkl"):
    with open(file, "rb") as f:
        vectorstore = pickle.load(f)
    
    docs = vectorstore.similarity_search(query)
    return docs[0].page_content

if not os.path.isfile("contacts-vectorstore.pkl"):
    ingestion("actions/contacts.txt", "contacts")
if not os.path.isfile("links-vectorstore.pkl"):
    ingestion("actions/links.txt", "links")