import json
import os
from pathlib import Path
from typing import Optional
from src.schemas.extraction import ExtractedProjectData

class StructuredStore:
    def __init__(self, file_path: str = "storage/extracted_data.json"):
        self.file_path = Path(file_path)
        # וודא שתיקיית האחסון קיימת
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, data: ExtractedProjectData):
        """שמירת נתונים מובנים לקובץ JSON (דריסה או עדכון)"""
        # אם נרצה לשמר נתונים קיימים, נטען אותם קודם
        existing_data = self.load()

        if existing_data:
            existing_data.decisions.extend(data.decisions)
            existing_data.rules.extend(data.rules)
            existing_data.warnings.extend(data.warnings)
            final_to_save = existing_data
        else:
            final_to_save = data

        with open(self.file_path, "w", encoding="utf-8") as f:
            # שימוש ב-model_dump_json של Pydantic לטיפול בתאריכים
            f.write(final_to_save.model_dump_json(indent=4))

        print(f"💾 Data successfully saved to {self.file_path}")

    def load(self) -> Optional[ExtractedProjectData]:
        """טעינת הנתונים מהקובץ"""
        if not self.file_path.exists():
            return None

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data_dict = json.load(f)
                return ExtractedProjectData.model_validate(data_dict)
        except Exception as e:
            print(f"⚠️ Failed to load store: {e}")
            return None

    def clear(self):
        """מחיקת המאגר המקומי"""
        if self.file_path.exists():
            self.file_path.unlink()