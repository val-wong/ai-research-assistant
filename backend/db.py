import os
import chromadb
from chromadb.config import Settings

def get_client():
    path = os.getenv("CHROMA_DIR", ".chroma")
    return chromadb.Client(Settings(persist_directory=path, is_persistent=True))

def get_collection():
    client = get_client()
    return client.get_or_create_collection("papers")
