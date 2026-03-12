import os
from typing import List

from dateutil.utils import today
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
                "You are a specialized Technical Analyst. Your goal is to parse developer documentation "
                "and extract structured insights into the following categories:\n\n"

                "1. **Decisions**: Look for architectural choices, database selections, or logic definitions. "
                "Keywords: 'decided', 'selected', 'using', 'we will use', 'choice'.\n"

                "2. **Rules**: Look for mandatory constraints or coding standards. "
                "Keywords: 'must', 'should', 'always', 'required', 'convention', 'RTL', 'naming'.\n"

                "3. **Warnings**: Look for risks, sensitive areas, or things to avoid. "
                "Keywords: 'be careful', 'warning', 'do not touch', 'sensitive', 'risk', 'high severity'.\n\n"

                "GUIDELINES:\n"
                "- If a piece of information is ambiguous, lean towards including it.\n"
                "- Capture the essence of the instruction in the summary/message fields.\n"
                "- Use the current date for 'observed_at' if not specified.\n"
                "- The source file for all extracted items must be: '{source_file}'.\n\n"

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
                source_file=source_name,
                current_date=today
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