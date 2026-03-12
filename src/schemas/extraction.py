from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class BaseExtraction(BaseModel):
    """מחלקה בסיסית המשותפת לכל רכיבי החילוץ"""
    source_file: str = Field(..., description="שם הקובץ ממנו חולץ המידע")
    observed_at: datetime = Field(default_factory=datetime.now, description="תאריך וזמן חילוץ המידע")


class Decision(BaseExtraction):
    """חילוץ החלטות מתוך הטקסט"""
    title: str = Field(..., description="כותרת קצרה וקולעת של ההחלטה")
    summary: str = Field(..., description="תמצית הלוגיקה שמאחורי ההחלטה")
    tags: List[str] = Field(default_factory=list, description="רשימת תגיות רלוונטיות (למשל: תקציב, כוח אדם, טכנולוגי)")


class Rule(BaseExtraction):
    """חילוץ חוקים או הנחיות מחייבות"""
    rule_text: str = Field(..., description="הטקסט המלא של החוק או ההנחיה")
    scope: str = Field(..., description="היקף תחולת החוק (למי הוא תקף ומתי)")


class Warning(BaseExtraction):
    """חילוץ אזהרות או נקודות תורפה"""
    sensitive_area: str = Field(..., description="האזור או הנושא שבו זוהתה רגישות")
    message: str = Field(..., description="תיאור האזהרה")
    severity: str = Field(..., description="רמת חומרה: High או Low")


class ExtractedProjectData(BaseModel):
    """האובייקט המרכז את כל המידע המובנה שחולץ ממסמך או סשן"""
    decisions: List[Decision] = Field(default_factory=list)
    rules: List[Rule] = Field(default_factory=list)
    warnings: List[Warning] = Field(default_factory=list)

    metadata: Optional[dict] = Field(default_factory=dict, description="מידע נוסף על תהליך החילוץ")