from llama_index.core.workflow import Context, StartEvent
from src.workflows.events import QueryValidatedEvent
from src.workflows.state import RAGState


async def validate_input_query(ctx: Context, ev: StartEvent) -> QueryValidatedEvent:
    """
    בודק את תקינות השאילתה הנכנסת.
    מצפה לקבל 'query' בתוך ה-StartEvent.
    """
    query = ev.get("query")
    if not query or len(query) < 5:
        raise ValueError("השאילתה קצרה מדי או ריקה. אנא פרט יותר.")

    # שמירת השאילתה ב-State הגלובלי של הריצה
    await ctx.store.set("state", RAGState(query=query))

    print(f"🔍 InputGuard: Query validated: '{query[:30]}...'")
    return QueryValidatedEvent(query=query)