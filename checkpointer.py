from dotenv import load_dotenv
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver   # ✅ new import
import os

load_dotenv()  # loads .env with MONGODB_URI etc.


def get_mongo_checkpointer() -> MongoDBSaver:
    """
    Return a MongoDBSaver instance that LangGraph can use as a checkpointer.
    """
    client = MongoClient(os.getenv("MONGODB_URI"))
    return MongoDBSaver(
        client=client,
        db_name=os.getenv("MONGODB_DB", "chatbot"),
        checkpoint_collection_name=os.getenv("MONGODB_COLLECTION", "conversations"),
        # ttl=None  # optionally set a TTL in seconds
    )
