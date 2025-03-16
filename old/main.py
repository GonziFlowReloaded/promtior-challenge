from pymongo import MongoClient
from langchain.schema import SystemMessage, HumanMessage
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def load_data_from_mongo(db_name="scraper_db", collection_name="pages"):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[db_name]
    collection = db[collection_name]
    return list(collection.find({}, {"_id": 0, "url": 1, "text": 1}))

def create_vectorstore(data, persist_directory="chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=os.getenv("GOOGLE_API_KEY"))


    texts = [doc["text"] for doc in data]
    metadatas = [{"url": doc["url"]} for doc in data]
    vectorstore = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory=persist_directory)
    vectorstore.persist()
    return vectorstore

def create_chatbot():
    chatbot = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=os.getenv("GOOGLE_API_KEY")  # ✅ Corrección en la clave API
    )
    return chatbot

def chatbot_response(chatbot, user_input, vectorstore):
    retriever = vectorstore.as_retriever()  # ✅ Corrección en la búsqueda
    docs = retriever.invoke(user_input)
    
    context = "\n".join([f"URL: {doc.metadata['url']}\nTexto: {doc.page_content}" for doc in docs])

    messages = [
        SystemMessage(content="You are an Assistance of Promtior."),
        SystemMessage(content=f"Here is relevant information about Promtior:\n{context}"),
        HumanMessage(content=user_input)
    ]

    return chatbot.invoke(messages).content

if __name__ == "__main__":
    data = load_data_from_mongo()
    vectorstore = create_vectorstore(data)
    chatbot = create_chatbot()
    
    while True:
        user_input = input("Pregunta: ")
        if user_input.lower() in ["salir", "exit"]:
            break
        response = chatbot_response(chatbot, user_input, vectorstore)
        print("Chatbot:", response)
