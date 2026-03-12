import gradio as gr
import asyncio
import os
from src.services.rag_service import RAGService

# 1. אתחול השירות (Instance)
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "my-rag-index")
rag_service = RAGService(index_name=INDEX_NAME)


def handle_query(question: str):
    """
    פונקציית מעטפת שמריצה את ה-Workflow האסינכרוני בצורה סינכרונית עבור Gradio
    """
    if not question.strip():
        return "נא להזין שאלה."

    try:
        # יצירת לופ אירועים חדש להרצת הפעולה האסינכרונית
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # הרצת ה-Workflow וקבלת התוצאה
        # שימי לב: אנחנו קוראים למופע rag_service ולא למחלקה RAGService
        response = loop.run_until_complete(rag_service.query(question))

        loop.close()
        return response
    except Exception as e:
        return f"שגיאה בהרצת השאילתה: {str(e)}"


# בניית הממשק
with gr.Blocks(title="RAG Knowledge Base", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 RAG Knowledge Agent")
    gr.Markdown("המערכת משתמשת ב-Event-Driven Workflow לניתוח השאילתה שלך.")

    with gr.Row():
        input_text = gr.Textbox(
            label="השאלה שלך",
            placeholder="הקלד כאן...",
            lines=2
        )

    submit_btn = gr.Button("שלח שאילתה", variant="primary")
    output_text = gr.Textbox(label="תשובת המערכת (מבוססת Workflow)", interactive=False)

    submit_btn.click(
        fn=handle_query,
        inputs=[input_text],
        outputs=[output_text]
    )

if __name__ == "__main__":
    # אם מריצים ישירות את הקובץ הזה, נוודא שיש אינדקס (אופציונלי)
    # rag_service.ingest(["./data_source"])
    demo.launch(server_name="0.0.0.0", server_port=7860)