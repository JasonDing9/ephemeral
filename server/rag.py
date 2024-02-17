from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.vectorstores.faiss import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_together import TogetherEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import pickle
import nltk
import openai
import os
from dotenv import load_dotenv
import together

load_dotenv()
os.environ['TOGETHER_API_KEY'] = os.environ['TOGETHER_API']
# together.api_key = os.environ['TOGETHER_API']

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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