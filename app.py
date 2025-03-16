from fastapi import FastAPI
from api import chat
from core.config import settings
from services.vector_service import initialize_vectorstore
from services.chatbot_service import initialize_chatbot
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Include routers
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    # Initialize services on startup
    initialize_vectorstore()
    initialize_chatbot()

@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} API is running"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)