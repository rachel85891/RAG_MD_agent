from llama_index.core.workflow import Event
from llama_index.core.schema import NodeWithScore
from typing import List

class QueryValidatedEvent(Event):
    """נשלח לאחר ששלב ה-Input Guard אישר שהשאילתה תקינה"""
    query: str

class RetrievalDoneEvent(Event):
    """נשלח לאחר סיום השליפה מ-Pinecone"""
    nodes: List[NodeWithScore]

class ValidationPassedEvent(Event):
    """נשלח כאשר התשובה של ה-LLM עברה את בקרת האיכות"""
    response: str

class ValidationFailedEvent(Event):
    """נשלח כאשר התשובה לא עומדת בסטנדרטים (מפעיל לולאת Retry)"""
    error_msg: str

class StructuredQueryEvent(Event):
    """אירוע לחיפוש בתוך ה-JSON המובנה"""
    query: str

class RetrievalEvent(Event):
    """אירוע לחיפוש וקטורי רגיל ב-Pinecone"""
    query: str