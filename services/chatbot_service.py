from langchain.schema import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from services.vector_service import get_vectorstore

# Global variable to store the chatbot
chatbot = None

def initialize_chatbot():
    """Initialize the chatbot with Google Generative AI"""
    global chatbot
    
    try:
        chatbot = ChatGoogleGenerativeAI(
            model=settings.CHAT_MODEL,
            api_key=settings.GOOGLE_API_KEY
        )
        print("Chatbot initialized successfully")
        return chatbot
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        raise

def get_chatbot():
    """Get the chatbot singleton"""
    global chatbot
    if chatbot is None:
        chatbot = initialize_chatbot()
    return chatbot

def process_chat_query(query: str):
    """Process a chat query using the chatbot and vector store"""
    # Get the chatbot and vector store
    bot = get_chatbot()
    vector_store = get_vectorstore()
    
    # Get relevant documents
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(query)
    
    # Build context from retrieved documents
    context = "\n".join([f"URL: {doc.metadata['url']}\nTexto: {doc.page_content}" for doc in docs])
    
    # Create message list for the chatbot
    messages = [
        SystemMessage(content="You are an Assistance of Promtior."),
        SystemMessage(content=f"Here is relevant information about Promtior:\n{context}"),
        HumanMessage(content=query)
    ]
    
    # Get response from chatbot
    return bot.invoke(messages).content