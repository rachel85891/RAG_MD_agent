from llama_index.core.workflow import Context, step
from llama_index.core import Settings
from src.workflows.events import QueryValidatedEvent, StructuredQueryEvent, RetrievalEvent
from llama_index.core.workflow import Event

async def route_query(ctx: Context, ev: QueryValidatedEvent) -> StructuredQueryEvent | RetrievalEvent:
    """
    מנתב את השאילתה על בסיס סוג המידע המבוקש.
    """
    prompt = (
        f"Analyze the following user query: '{ev.query}'\n"
        "Determine if the user is asking for:\n"
        "1. Quantitative/List-based/Time-based data (e.g., 'How many decisions?', 'List all rules from last month', 'What warnings are high severity?').\n"
        "2. General knowledge/Contextual information (e.g., 'Explain the project logic', 'What is the background of...').\n"
        "Respond with ONLY the word 'STRUCTURED' for option 1 or 'VECTOR' for option 2."
    )

    response = await Settings.llm.acomplete(prompt)
    decision = str(response).strip().upper()

    if "STRUCTURED" in decision:
        print(f"🔀 Router: Routing to Structured Query (JSON)")
        #ctx.write_event(Event(msg="🔍 מזהה שאילתה כמותית - ניגש למאגר ה-JSON..."))
        print(Event(msg="🔍 מזהה שאילתה כמותית - ניגש למאגר ה-JSON..."))
        return StructuredQueryEvent(query=ev.query)
    else:
        print(f"🔀 Router: Routing to Vector Retrieval (Pinecone)")
        #ctx.write_event(Event(msg="📚 מזהה שאילתה תיאורית - מחפש במסמכים ב-Pinecone..."))
        print(Event(msg="📚 מזהה שאילתה תיאורית - מחפש במסמכים ב-Pinecone..."))
        return RetrievalEvent(query=ev.query)