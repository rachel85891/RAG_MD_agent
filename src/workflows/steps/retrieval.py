from llama_index.core.workflow import Context
from src.workflows.events import QueryValidatedEvent, RetrievalDoneEvent
from src.workflows.state import RAGState


async def retrieve_context(ctx: Context, ev: QueryValidatedEvent) -> RetrievalDoneEvent:
    """
    מבצע שליפה מה-Vector Store (Pinecone) על בסיס השאילתה המאומתת.
    """
    # שליפת השירות מה-Context (נניח שהזרקנו אותו באתחול ה-Workflow)
    rag_service = await ctx.get_data("rag_service")

    # ב-LlamaIndex, ה-Query Engine מחזיר אובייקט Response שמכיל source_nodes
    # לצורך הדוגמה, נניח שאנחנו משתמשים ב-Retriever ישירות
    index = rag_service.query_engine._index  # גישה לאינדקס הקיים
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(ev.query)

    # עדכון ה-State
    state: RAGState = await ctx.get_data("state")
    state.retrieved_nodes = nodes
    await ctx.set_data("state", state)

    print(f"📚 Retrieval: Found {len(nodes)} relevant nodes.")
    return RetrievalDoneEvent(nodes=nodes)