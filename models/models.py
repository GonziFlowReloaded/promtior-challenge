from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

class DocumentModel(BaseModel):
    url: str
    text: str

class DocumentsResponse(BaseModel):
    documents: List[DocumentModel]

class StatusResponse(BaseModel):
    message: str