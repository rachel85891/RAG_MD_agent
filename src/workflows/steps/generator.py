from llama_index.core.workflow import Context, StopEvent
from src.workflows.events import ValidationPassedEvent
from src.workflows.state import RAGState
from llama_index.core import Settings


async def generate_final_response(ctx: Context, ev: ValidationPassedEvent) -> StopEvent:
    """
    מייצר תשובה סופית באמצעות ה-LLM המוגדר ב-Settings.
    """
    state: RAGState = await ctx.store.get("state")

    # בניית הקונטקסט מה-Nodes
    context_str = "\n\n".join([n.node.get_content() for n in state.retrieved_nodes])

    prompt = (
        f"Context information is below:\n"
        f"---------------------\n{context_str}\n---------------------\n"
        f"Given the context information and not prior knowledge, "
        f"answer the query: {state.query}\n"
        f"Answer:"
    )

    # שימוש ב-LLM הגלובלי שהגדרת ב-AppSettings
    response = await Settings.llm.acomplete(prompt)

    state.llm_response = str(response)
    await ctx.store.set("state", state)

    print("✨ Generator: Final response created.")
    return StopEvent(result=state.llm_response)