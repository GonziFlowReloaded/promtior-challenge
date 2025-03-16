from fastapi import APIRouter, HTTPException, Depends
from models.models import ChatRequest, ChatResponse, DocumentsResponse, DocumentModel, StatusResponse
from services.chatbot_service import process_chat_query
from services.vector_service import refresh_vectorstore
from core.database import MongoDB

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat request and return a response"""
    try:
        response = process_chat_query(request.query)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/documents", response_model=DocumentsResponse)
async def get_documents():
    """Get all documents from the database"""
    try:
        data = MongoDB.get_documents()
        documents = [DocumentModel(url=doc["url"], text=doc["text"]) for doc in data]
        return DocumentsResponse(documents=documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documents: {str(e)}")

@router.post("/refresh", response_model=StatusResponse)
async def refresh_data():
    """Refresh the vector store with updated data from MongoDB"""
    try:
        refresh_vectorstore()
        return StatusResponse(message="Data refreshed successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing data: {str(e)}")