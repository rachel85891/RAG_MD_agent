from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.base.base_query_engine import BaseQueryEngine

def create_query_engine(index: VectorStoreIndex) -> BaseQueryEngine:
    """
    יוצר Query Engine מוגדר אישית עם Retriever ו-Response Synthesizer.
    שולף את 3 ה-Nodes הרלוונטיים ביותר (top_k=3).
    """

    # 1. הגדרת ה-Retriever - אחראי על שליפת המידע מה-Vector Store
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3,
    )

    # 2. הגדרת ה-Response Synthesizer - אחראי על יצירת התשובה מהמידע שנשלף
    response_synthesizer = get_response_synthesizer(
        response_mode="compact"  # משלב את המידע בצורה יעילה בתוך ה-Prompt
    )

    # 3. בניית ה-Query Engine הסופי
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )

    return query_engine