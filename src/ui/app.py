import gradio as gr
import asyncio
import os


def create_ui(rag_service):
    """
    יוצר את ממשק המשתמש ומחבר אותו לשירות ה-RAG שכבר אותחל.
    """

    async def handle_query(question: str):
        # בדיקה אם השאלה ריקה - חייב להחזיר 2 ערכים!
        if not question or not question.strip():
            yield "נא להזין שאלה.", ""
            return

        if not rag_service.query_engine:
            yield "❌ שגיאה: המערכת טרם עברה אינדוקס.", ""
            return

        # שלב 1: עדכון סטטוס ראשוני
        status_log = "🤖 המערכת מנתחת את השאילתה שלך..."
        yield status_log, ""

        try:
            # הרצת השאילתה
            response = await rag_service.query(question)
            final_answer = str(response)

            # שלב 2: עדכון הצלחה
            yield status_log + "\n✅ ניתוח הושלם.", final_answer

        except Exception as e:
            # שגיאה - שוב, להחזיר 2 ערכים כדי למנוע את ה-ValueError
            yield f"❌ שגיאה בשרת: {str(e)}", ""

    # בניית הממשק
    with gr.Blocks(title="MD-Agent RAG", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🤖 MD-Agent: Hybrid RAG System")
        gr.Markdown("המערכת מחליטה אם לשלוף מידע מובנה (**JSON**) או טקסטואלי (**Pinecone**).")

        with gr.Row():
            with gr.Column(scale=2):
                # כאן הגדרנו את ה-input_text רק פעם אחת
                input_text = gr.Textbox(
                    label="מה תרצה לדעת?",
                    placeholder="למשל: 'כמה חוקים קיימים?' או 'איך מטפלים ב-RTL?'",
                    lines=3
                )
                with gr.Row():
                    submit_btn = gr.Button("שלח שאילתה", variant="primary")
                    clear_btn = gr.Button("נקה")

            with gr.Column(scale=1):
                status_box = gr.Textbox(label="סטטוס לוג", interactive=False)

        output_text = gr.Textbox(
            label="תשובת המערכת",
            interactive=False,
            lines=10,
            placeholder="התשובה תופיע כאן..."
        )

        # ריכוז הגדרות האירוע
        query_event_config = {
            "fn": handle_query,
            "inputs": [input_text],
            "outputs": [status_box, output_text]
        }

        submit_btn.click(**query_event_config)
        input_text.submit(**query_event_config)

        # ניקוי שדות
        def clear_fields():
            return "", "", ""

        clear_btn.click(fn=clear_fields, outputs=[input_text, status_box, output_text])

    return demo