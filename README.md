# 🤖 MD-Agent: RAG workflow-based documentation analyst

MD-Agent הוא סוכן AI מתקדם (AI Agent) שנועד לנתח ולהשיב על שאלות מתוך קבצי תיעוד טכניים (Markdown). הפרויקט משלב טכנולוגיות RAG (Retrieval-Augmented Generation) מודרניות עם ארכיטקטורה מבוססת אירועים (Event-Driven Workflow) וניתוב חכם בין חיפוש סמנטי לחילוץ נתונים מובנים.

## 🚀 מטרת הפרויקט
המטרה היא לספק ממשק אחד, חכם ואמין, המאפשר למפתחים ולמנהלי מוצר "לשוחח" עם התיעוד הטכני של הפרויקט. המערכת יודעת לא רק למצוא טקסטים דומים, אלא לענות על שאלות מורכבות הדורשות דיוק כמותי, רשימתי או מבוסס זמן.

## 🏗️ ארכיטקטורה (High Level)
המערכת בנויה לפי עקרונות SOLID ומחולקת לשתי שכבות עיקריות:

1.  **Ingestion & Extraction (Offline):** קריאת קבצי ה-Markdown, הפיכתם לוקטורים (סמנטיים) ושמירתם ב-Vector DB (Pinecone). במקביל, ה-LLM סורק את הקבצים ומחלץ נתונים מובנים (Decisions, Rules, Warnings) לקובץ JSON.
2.  **Query Workflow (Online):** השאילתה של המשתמש עוברת דרך **Router** חכם שמחליט:
    * **מסלול סמנטי:** חיפוש ב-Vector store לתשובות כלליות ("איך עושים...").
    * **מסלול מובנה:** שליפה מה-JSON המובן לשאלות מדויקות ("תן לי רשימה של...").

## 🛠️ איך להריץ?

### 1. דרישות קדם
* Python 3.10+
* מפתחות API עבור: OpenAI (LLM), Cohere (Embeddings), Pinecone (Vector DB).

### 2. התקנה
```bash
# שכפול הפרויקט
git clone <your-repo-url>
cd MD_agent

# יצירת סביבה וירטואלית והפעלתה
python -m venv venv
source venv/bin/bin/activate # ב-Windows: venv\Scripts\activate

# התקנת ספריות
pip install -r requirements.txt
```

### 3. הגדרות
צור קובץ .env בשורש הפרויקט והוסף את המפתחות שלך (השתמש ב-.env.example כתבנית):
```Plaintext
OPENAI_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_NAME=your_index_name
```

### 4. טעינת נתונים (Ingestion)
הכנס את קבצי ה-Markdown שלך לתיקיות המתאימות תחת data_source/ (למשל cursor/, claude/), ואז הרץ את תהליך הטעינה:
```bash
python -m src.data.ingestion_service
```

### 5. הרצת ממשק המשתמש (UI)
הרץ את קובץ ה-Main כדי לפתוח את ממשק ה-Gradio:
```bash
python main.py
```
הפקודה תציג כתובת URL מקומית (למשל http://127.0.0.1:7860). פתח אותה בדפדפן.

## דוגמאות לשאלות שה-Agent יודע לענות 🙋
הסוכן משתמש בניתוב חכם כדי לענות על מגוון שאלות:
 ###  שאלות כלליות (חיפוש סמנטי)
* "איך מוגדר ה-flow של ה-Auth בפרויקט?"
* "האם יש הנחיות ספציפיות לשימוש ב-hooks של React?"
* "מהי מטרת התיקייה src/core?"
 ###  שאלות מורכבות/כמותיות (שליפה מובנית)
* "תן לי רשימה של כל ההחלטות הטכניות שהתקבלו בפרויקט."
* "מה ההנחיה העדכנית לגבי שימוש ב-RTL בממשק?"
* "אילו אזהרות סומנו בחומרה גבוהה (High Severity)?"
* "מהן כל ההחלטות הקשורות ל-Database?"

### 📊 ויזואליזציה של ה-Workflow
הפרויקט כולל כלי ליצירת תרשים זרימה אינטראקטיבי המציג את כל הצעדים (Steps) והאירועים (Events) במערכת.

**איך לצפות בתרשים:**
1. וודאי שהתקנת את הספרייה: `pip install pyvis`
2. הריצי את הסקריפט:
   ```bash
   python visualize_workflow.py