import os
from typing import List
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import BaseNode

def index_nodes_to_pinecone(
        nodes: List[BaseNode],
        index_name: str,
        api_key: str = None
) -> VectorStoreIndex:
    """
    מקבל רשימת Nodes ומאנדקס אותם ב-Pinecone Vector Store.
    """
    # אתחול Pinecone
    pc = Pinecone(api_key=api_key or os.environ.get("PINECONE_API_KEY"))
    pinecone_index = pc.Index(index_name)

    # הגדרת ה-Vector Store עבור LlamaIndex
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # הגדרת הקונטקסט לאחסון
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # יצירת האינדקס והעלאת ה-Nodes
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context
    )

    return index