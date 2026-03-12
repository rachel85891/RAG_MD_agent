import os
from typing import List
from llama_index.core.node_parser import SentenceSplitter
from src.data.loader import load_markdown_docs
from src.data.vector_store import index_nodes_to_pinecone
from src.config.settings import app_settings
from src.core.engine import create_query_engine
from src.workflows.rag_workflow import RAGWorkflow
from llama_index.core.workflow import Context

class RAGService:
    def __init__(self, index_name: str):
        # הגדרת המודלים (Cohere & LLM) פעם אחת בזמן האתחול
        self.index_name = index_name
        self.query_engine = None
        self.index = None

    def ingest(self, paths: List[str]) -> None:


        #מבצע את כל תהליך ה-Pipeline: טעינה, פירוק ל-Nodes ואינדוקס.

        # 1. טעינת מסמכים
        documents = load_markdown_docs(paths)

         #2. פירוק ל-Nodes (Chunks) - חיוני לפני אינדוקס

        parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = parser.get_nodes_from_documents(documents)

        # 3. אינדוקס ב-Pinecone
        index = index_nodes_to_pinecone(nodes, self.index_name)

        # 4. יצירת מנוע השאילתות ושמירתו בזיכרון
        self.query_engine = create_query_engine(index)
        print(f"Successfully indexed {len(nodes)} nodes to {self.index_name}")

    async def query(self, question: str) -> str:

        #מבצע שאילתה ומחזירה תשובה טקסטואלית.
        if not self.index and not self.query_engine:
            return "שגיאה: המערכת טרם עברה אינדוקס (Ingest). נא להריץ אינדוקס ראשוני."

        workflow = RAGWorkflow(timeout=60, verbose=True)

        ctx = Context(workflow)
        await ctx.set_data("rag_service", self)

        print(f"🌀 Starting Workflow for query: {question}")
        try:
            # הרצת ה-Workflow
            result = await workflow.run(query=question, ctx=ctx)
            return str(result)
        except Exception as e:
            return f"שגיאה במהלך הרצת ה-Workflow: {str(e)}"
"""
import os
from typing import List
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from src.data.loader import load_markdown_docs
from src.data.vector_store import index_nodes_to_pinecone  # הפונקציה המקומית שלנו
from src.config.settings import app_settings
from src.core.engine import create_query_engine


class RAGService:
    _instance = None
    PERSIST_DIR = "./storage"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RAGService, cls).__new__(cls)
        return cls._instance

    def __init__(self, index_name: str = "default"):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.index_name = index_name
        self.query_engine = None
        self._initialized = True

        # ניסיון טעינה אוטומטית מהדיסק אם קיים
        if os.path.exists(self.PERSIST_DIR):
            print("📦 Loading existing index from storage...")
            storage_context = StorageContext.from_defaults(persist_dir=self.PERSIST_DIR)
            index = load_index_from_storage(storage_context)
            self.query_engine = create_query_engine(index)

    def ingest(self, paths: List[str]) -> None:
        documents = load_markdown_docs(paths)
        parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = parser.get_nodes_from_documents(documents)

        index = index_nodes_to_pinecone(nodes, self.index_name)

        # שמירה לדיסק כדי שה-UI יוכל לקרוא את זה
        index.storage_context.persist(persist_dir=self.PERSIST_DIR)

        self.query_engine = create_query_engine(index)
        print(f"✅ Ingestion complete and persisted to {self.PERSIST_DIR}")

    def query(self, question: str) -> str:
        if not self.query_engine:
            return "נא להריץ אינדוקס ראשוני (Ingest). המנוע לא מוכן."

        response = self.query_engine.query(question)
        return str(response)


# מופע גלובלי
rag_service = RAGService()
"""