from llama_index.core.workflow import Context
from src.workflows.events import QueryValidatedEvent, RetrievalDoneEvent
from src.workflows.state import RAGState


async def retrieve_context(ctx: Context, ev: QueryValidatedEvent) -> RetrievalDoneEvent:
    """
    מבצע שליפה מה-Vector Store (Pinecone) על בסיס השאילתה המאומתת.
    """
    # שליפת השירות מה-Context (נניח שהזרקנו אותו באתחול ה-Workflow)
    rag_service = await ctx.store.get("rag_service")

    #  גישה בטוחה ל-Retriever
    # במקום rag_service.query_engine._index, אנחנו ניגשים ל-retriever ישירות
    if hasattr(rag_service.query_engine, "retriever"):
        retriever = rag_service.query_engine.retriever
    else:
        # במידה ואין retriever מובנה, נשתמש במנוע השאילתות כ-retriever
        retriever = rag_service.query_engine

    nodes = retriever.retrieve(ev.query)

    # עדכון ה-State
    state: RAGState = await ctx.store.get("state")
    state.retrieved_nodes = nodes
    await ctx.store.set("state", state)

    print(f"📚 Retrieval: Found {len(nodes)} relevant nodes.")
    return RetrievalDoneEvent(nodes=nodes)