from llama_index.core.workflow import Context, step, StopEvent
from src.data.structured_store import StructuredStore
from src.workflows.events import StructuredQueryEvent
from llama_index.core import Settings


async def process_structured_query(ctx: Context, ev: StructuredQueryEvent) -> StopEvent:
    """
    טוען את ה-JSON ומבצע סינון חכם בעזרת ה-LLM על הנתונים הקיימים.
    """
    store = StructuredStore()
    data = store.load()

    if not data:
        return StopEvent(result="לא נמצא מידע מובנה במערכת (ה-Store ריק).")

    # המרת הנתונים לטקסט לצורך עיבוד ע"י ה-LLM (או ביצוע סינון קוד ידני)
    # כאן נשתמש ב-LLM כדי שיעבור על ה-JSON ויחזיר רק מה שרלוונטי
    data_json = data.model_dump_json()

    analysis_prompt = (
        f"The following is a JSON dataset of decisions, rules, and warnings:\n{data_json}\n"
        f"User Query: {ev.query}\n"
        "Please filter and summarize the relevant data from the JSON to answer the user's request. "
        "If dates are mentioned, pay attention to the 'observed_at' field."
    )

    response = await Settings.llm.acomplete(analysis_prompt)
    return StopEvent(result=str(response))