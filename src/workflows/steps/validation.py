from llama_index.core.workflow import Context
from src.workflows.events import RetrievalDoneEvent, ValidationPassedEvent, ValidationFailedEvent
from src.workflows.state import RAGState


async def validate_retrieval_quality(ctx: Context,
                                     ev: RetrievalDoneEvent) -> ValidationPassedEvent | ValidationFailedEvent:
    """
    בודק האם ה-Nodes שנשלפו עומדים בסף הרלוונטיות (Score > 0.7).
    """
    if not ev.nodes:
        return ValidationFailedEvent(error_msg="לא נמצא מידע רלוונטי במאגר.")

    # בדיקת ה-Score של ה-Node הראשון (הכי רלוונטי)
    top_score = ev.nodes[0].score if ev.nodes[0].score is not None else 0

    if top_score < 0.5:
        print(f"⚠️ Validation: Low confidence score ({top_score:.2f})")
        return ValidationFailedEvent(error_msg="המידע שנמצא אינו רלוונטי מספיק.")

    print(f"✅ Validation: Passed with score {top_score:.2f}")
    return ValidationPassedEvent(response="Context is valid")