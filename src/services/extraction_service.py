import os
from typing import List
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.program.openai import OpenAIPydanticProgram
from src.schemas.extraction import ExtractedProjectData
from llama_index.core import Settings


class ExtractionService:
    def __init__(self):
        self.llm = Settings.llm
        # הגדרת התוכנית לחילוץ מידע מובנה
        self.program = OpenAIPydanticProgram.from_defaults(
            output_cls=ExtractedProjectData,
            prompt_template_str=(
                "You are an expert data extractor. Extract all decisions, rules, and warnings "
                "from the following text. If a certain category is not found, return an empty list. "
                "Ensure that 'source_file' is set to '{source_file}'.\n"
                "Text to analyze:\n"
                "-------------------\n"
                "{text}\n"
                "-------------------\n"
            ),
            llm=self.llm,
            verbose=True
        )

    async def extract_from_text(self, text: str, source_name: str) -> ExtractedProjectData:
        """חילוץ מידע מובנה מטקסט נתון"""
        try:
            extracted_data = await self.program.acall(
                text=text,
                source_file=source_name
            )
            return extracted_data
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            return ExtractedProjectData()

    async def process_documents(self, documents) -> ExtractedProjectData:
        """עיבוד רשימת מסמכים ואיחוד התוצאות לאובייקט אחד"""
        combined_data = ExtractedProjectData()

        for doc in documents:
            source = doc.metadata.get("file_name", "unknown_source")
            print(f"🔍 Extracting data from: {source}...")

            result = await self.extract_from_text(doc.text, source)

            # מיזוג התוצאות
            combined_data.decisions.extend(result.decisions)
            combined_data.rules.extend(result.rules)
            combined_data.warnings.extend(result.warnings)

        return combined_data