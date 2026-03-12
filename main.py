import os
import sys
import asyncio

# הוספת תיקיית src לנתיב המערכת כדי למנוע בעיות Import
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import app_settings
from src.services.rag_service import RAGService
from src.ui.app import demo


def main():
    print("🚀 Starting RAG Event-Driven Pipeline...")

    # 1. אתחול הגדרות (המרה מתבצעת אוטומטית בעת הייבוא בגלל ה-Singleton)
    # app_settings כבר אותחל בייבוא, כאן אנחנו רק מוודאים וולידציה
    print("⚙️  Step 1: Loading environment variables and AI models (Cohere & OpenAI)...")

    # 2. אתחול שירות ה-RAG
    # שים לב: וודא ששם האינדקס תואם למה שהגדרת ב-Pinecone Console
    INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "my-rag-index")
    rag_service = RAGService(index_name=INDEX_NAME)

    # 3. שלב ה-Ingestion (טעינה ואינדוקס)
    # במידה ואתה מריץ את האפליקציה בפעם הראשונה או שהמידע השתנה
    DATA_PATH = ["./data_source"]

    print(f"📂 Step 2: Scanning data source: {DATA_PATH}...")
    try:
        # פונקציית ה-ingest מתוך ה-RAGService מחברת את ה-Loader וה-Vector Store
        rag_service.ingest(DATA_PATH)
        print("✅ Step 3: Indexing complete. All documents are now in Pinecone.")
    except Exception as e:
        print(f"❌ Error during ingestion: {str(e)}")
        print("💡 Continuing to UI (assuming index already exists)...")

    # 4. הרצת הממשק
    print("\n🌐 Step 4: Launching Gradio UI...")
    print(f"--- Interface is being served on http://localhost:7860 ---")

    # הרצת ה-UI (מתוך src/ui/app.py)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  # שנה ל-True אם תרצה לינק זמני חיצוני
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Process stopped by user.")