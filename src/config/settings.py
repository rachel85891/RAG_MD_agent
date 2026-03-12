import os
from threading import Lock
from dotenv import load_dotenv

# ייבוא הרכיבים הרלוונטיים מ-LlamaIndex
from llama_index.core import Settings
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.openai import OpenAI

class AppSettings:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AppSettings, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        טוען הגדרות מ-.env ומגדיר את ה-Global Settings של LlamaIndex.
        """
        # טעינת משתני הסביבה מקובץ .env
        load_dotenv()

        # שליפת מפתחות API
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")

        # וולידציה בסיסית למפתחות קריטיים
        if not self.cohere_api_key or not self.openai_api_key:
            raise ValueError(
                "Missing API Keys! Please ensure COHERE_API_KEY and "
                "OPENAI_API_KEY are set in your .env file."
            )

        # 1. הגדרת מודל ה-Embedding של Cohere (אופטימלי לעברית)
        Settings.embed_model = CohereEmbedding(
            api_key=self.cohere_api_key,
            model_name="embed-multilingual-v3.0",
            input_type="search_query"
        )

        # 2. הגדרת ה-LLM של OpenAI (מודל gpt-4o-mini המהיר והחסכוני)
        Settings.llm = OpenAI(
            api_key=self.openai_api_key,
            model="gpt-4o-mini",
            temperature=0.1 # ערך נמוך לתשובות עקביות ומדויקות ב-RAG
        )

        # הגדרות עיבוד טקסט גלובליות
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50

        print("✅ LlamaIndex Global Settings initialized with Cohere & OpenAI.")

# יצירת מופע גלובלי לשימוש בכל חלקי המערכת
app_settings = AppSettings()