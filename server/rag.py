from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import pickle
from dotenv import load_dotenv

load_dotenv()

def ingestion():
    # Load Data
    loader = UnstructuredFileLoader("context.txt")
    raw_documents = loader.load()

    # Split text
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)

    # Load Data to vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open(f"vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

ingestion()