from pyvis.network import Network

# יצירת רשת תרשים חדשה
# height/width מגדירים את גודל הקנבס, unique=True מונע כפילויות של nodes
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

# הגדרות עיצוב לצמתים (Nodes) לפי סוגים
shape_step = "box"
shape_event = "ellipse"
color_step = "#40E0D0" # Turquoise
color_event = "#FF7F50" # Coral
color_start = "#32CD32" # LimeGreen
color_stop = "#FF4500" # OrangeRed

# --- הוספת צמתים (Nodes) ---

# התחלה וסיום
net.add_node("START", label="StartEvent", color=color_start, shape=shape_step)
net.add_node("STOP", label="StopEvent", color=color_stop, shape=shape_step)

# שלבים לוגיים (Steps) - צבע Turquoise
steps = [
    ("Router", "src.workflows.steps.router"),
    ("Retrieval", "src.workflows.steps.retrieval"),
    ("StructuredQuery", "src.workflows.steps.structured_query"),
    ("Generator", "src.workflows.steps.generator"),
    ("InputGuard", "src.workflows.steps.input_guard")
]
for node_id, label in steps:
    net.add_node(node_id, label=label, color=color_step, shape=shape_step, level=1)

# אירועים (Events) - צבע Coral
events = [
    ("RetrievalEvent", ""),
    ("StructuredQueryEvent", ""),
    ("InputValidatedEvent", "")
]
for node_id, label in events:
    net.add_node(node_id, label=node_id, color=color_event, shape=shape_event)


# --- הוספת קשרים (Edges) ---

# Start Flow
net.add_edge("START", "InputGuard")
net.add_edge("InputGuard", "InputValidatedEvent")
net.add_edge("InputValidatedEvent", "Router")

# Router Decisions
net.add_edge("Router", "RetrievalEvent", label="Semantic Path")
net.add_edge("Router", "StructuredQueryEvent", label="Structured Path")

# Paths Flow
net.add_edge("RetrievalEvent", "Retrieval")
net.add_edge("StructuredQueryEvent", "StructuredQuery")

# Completion
net.add_edge("Retrieval", "Generator")
net.add_edge("StructuredQuery", "Generator")
net.add_edge("Generator", "STOP")


# --- הגדרות אינטראקציה ---
net.toggle_physics(True) # מאפשר לתרשים "להסתדר" לבד
net.show_buttons(filter_=['physics']) # מוסיף כפתורי שליטה ב-HTML

# --- שמירה כקובץ HTML ---
output_file = "workflow_diagram.html"
net.save_graph(output_file)
print(f"✅ Workflow diagram saved to: {output_file}")