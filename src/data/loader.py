import os
from typing import List
from llama_index.core import SimpleDirectoryReader, Document

def load_markdown_docs(input_dirs: List[str]) -> List[Document]:
    """
    טוען קבצי Markdown מנתיבים מרובים ומוסיף metadata של שם הכלי (שם התיקייה).
    """
    all_documents = []

    for path in input_dirs:
        if not os.path.isdir(path):
            print(f"Warning: Path {path} is not a valid directory. Skipping.")
            continue

        # פונקציית עזר להוספת metadata לכל קובץ
        def get_metadata(file_path: str) -> dict:
            return {"tool_name": os.path.basename(os.path.dirname(file_path))}

        reader = SimpleDirectoryReader(
            input_dir=path,
            required_exts=[".md"],
            file_metadata=get_metadata,
            recursive = True
        )

        all_documents.extend(reader.load_data())

    return all_documents