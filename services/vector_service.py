from langchain.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from core.config import settings
from core.database import MongoDB
import os

# Global variable to store the vectorstore
vectorstore = None

def initialize_vectorstore():
    """Initialize the vector store with data from MongoDB"""
    global vectorstore
    
    try:
        # Get documents from MongoDB
        data = MongoDB.get_documents()
        
        # Create embeddings model
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.GOOGLE_API_KEY
        )
        
        # Prepare data for vector store
        texts = [doc["text"] for doc in data]
        metadatas = [{"url": doc["url"]} for doc in data]
        
        # Create and persist vector store
        vectorstore = Chroma.from_texts(
            texts, 
            embeddings, 
            metadatas=metadatas, 
            persist_directory=settings.VECTOR_DB_PATH
        )
        vectorstore.persist()
        
        print(f"Vector store initialized with {len(texts)} documents")
        return vectorstore
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        raise

def get_vectorstore():
    """Get the vector store singleton"""
    global vectorstore
    if vectorstore is None:
        vectorstore = initialize_vectorstore()
    return vectorstore

def refresh_vectorstore():
    """Refresh the vector store with updated data from MongoDB"""
    global vectorstore
    vectorstore = None
    return initialize_vectorstore()