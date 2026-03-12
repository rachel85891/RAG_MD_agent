from llama_index.core.workflow import Workflow, Context, StartEvent, StopEvent, step
from llama_index.core import Settings

# ייבוא הצעדים והאירועים
from src.workflows.events import (
    QueryValidatedEvent,
    RetrievalDoneEvent,
    ValidationPassedEvent,
    ValidationFailedEvent
)
from src.workflows.state import RAGState
from src.workflows.steps.input_guard import validate_input_query
from src.workflows.steps.retrieval import retrieve_context
from src.workflows.steps.validation import validate_retrieval_quality
from src.workflows.steps.generator import generate_final_response


class RAGWorkflow(Workflow):
    """
    מנוע ה-Workflow המרכזי המנהל את זרימת האירועים (Event-Driven RAG).
    כולל מנגנון לתיקון שאילתות (Query Expansion) במקרה של שליפה דלה.
    """

    # רישום הצעדים שיצרנו בקבצים נפרדים
    @step
    async def step_validate_input(self, ctx: Context, ev: StartEvent) -> QueryValidatedEvent:
        # קריאה לפונקציה המיובאת
        return await validate_input_query(ctx, ev)

    @step
    async def step_retrieve(self, ctx: Context, ev: QueryValidatedEvent) -> RetrievalDoneEvent:
        return await retrieve_context(ctx, ev)

    @step
    async def step_validate_quality(self, ctx: Context,
                                    ev: RetrievalDoneEvent) -> ValidationPassedEvent | ValidationFailedEvent:
        return await validate_retrieval_quality(ctx, ev)

    @step
    async def step_generate(self, ctx: Context, ev: ValidationPassedEvent) -> StopEvent:
        return await generate_final_response(ctx, ev)

    @step
    async def handle_retry_logic(self, ctx: Context, ev: ValidationFailedEvent) -> QueryValidatedEvent | StopEvent:
        """צעד התיקון נשאר כפי שהיה, הוא מובנה במחלקה"""
        state: RAGState = await ctx.get_data("state")

    @step
    async def handle_retry_logic(self, ctx: Context, ev: ValidationFailedEvent) -> QueryValidatedEvent | StopEvent:
        """
        צעד תיקון: אם הוולידציה נכשלה, ננסה להרחיב את השאילתה פעם אחת בלבד.
        """
        state: RAGState = await ctx.get_data("state")

        if state.retry_count >= 1:
            print(f"❌ Workflow: Max retries reached. Error: {ev.error_msg}")
            return StopEvent(result=f"מצטער, לא הצלחתי למצוא מידע רלוונטי במאגר. (שגיאה: {ev.error_msg})")

        # עדכון מונה הניסיונות
        state.retry_count += 1

        # שימוש ב-LLM לביצוע Query Expansion (ניסוח מחדש לחיפוש טוב יותר)
        expansion_prompt = (
            f"The original query '{state.query}' failed to find relevant documents. "
            f"Rewrite this query to be more descriptive and suitable for vector search. "
            f"Output only the new query text."
        )

        new_query = await Settings.llm.acomplete(expansion_prompt)
        print(f"🔄 Workflow: Retrying with expanded query: '{str(new_query)[:50]}...'")

        # עדכון השאילתה ב-State ושליחה מחדש לשלב השליפה
        state.query = str(new_query)
        await ctx.set_data("state", state)

        return QueryValidatedEvent(query=state.query)


# פונקציית עזר להרצת ה-Workflow מה-Gradio או ה-Main
async def run_rag_workflow(query: str, rag_service):
    wf = RAGWorkflow(timeout=60, verbose=True)

    # הזרקת שירותים ל-Context של הריצה
    ctx = Context(wf)
    await ctx.set_data("rag_service", rag_service)

    result = await wf.run(query=query, ctx=ctx)
    return result