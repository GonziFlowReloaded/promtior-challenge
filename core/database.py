from pymongo import MongoClient
from core.config import settings
from typing import List, Dict, Any

class MongoDB:
    client = None
    db = None
    collection = None
    
    @classmethod
    def connect(cls):
        """Connect to MongoDB database"""
        if cls.client is None:
            cls.client = MongoClient(settings.MONGO_URI)
            cls.db = cls.client[settings.MONGO_DB_NAME]
            cls.collection = cls.db[settings.MONGO_COLLECTION_NAME]
    
    @classmethod
    def get_documents(cls) -> List[Dict[str, Any]]:
        """Get all documents from the collection"""
        cls.connect()
        return list(cls.collection.find({}, {"_id": 0, "url": 1, "text": 1}))
    
    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            cls.client = None

# Initialize connection on import
MongoDB.connect()