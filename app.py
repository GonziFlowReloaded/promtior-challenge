from fastapi import FastAPI
from api import chat
from core.config import settings
from services.vector_service import initialize_vectorstore
from services.chatbot_service import initialize_chatbot
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    # Initialize services on startup
    initialize_vectorstore()
    initialize_chatbot()

@app.get("/")
async def index(request: Request):
    """Render of chatbot interface"""
    
    return templates.TemplateResponse("chat.html", 
                                      {"request": request,
                                       "title": settings.PROJECT_NAME,
                                       })

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)