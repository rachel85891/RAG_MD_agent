from typing import List, Optional
from pydantic import BaseModel, Field
from llama_index.core.schema import NodeWithScore

class RAGState(BaseModel):
    """
    מייצג את מצב הריצה של ה-Workflow.
    משמש לאחסון נתונים מצטברים בין הצעדים השונים.
    """
    query: str = Field(..., description="שאילתת המשתמש המקורית")
    retrieved_nodes: List[NodeWithScore] = Field(default_factory=list, description="הצמתים שנשלפו מה-Vector Store")
    llm_response: Optional[str] = Field(None, description="התשובה הסופית מה-LLM")
    retry_count: int = Field(default=0, description="מונה ניסיונות חוזרים במקרה של כשל באימות")
    is_valid: bool = Field(default=False, description="האם השאילתה/תשובה עברה וולידציה")

    class Config:
        arbitrary_types_allowed = True