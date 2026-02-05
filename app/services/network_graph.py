import json
import os

DB_FILE = "scam_graph.json"


def load_graph():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_graph(graph):
    with open(DB_FILE, "w") as f:
        json.dump(graph, f, indent=4)


def log_upi(phone: str, upi: str):
    """
    Detect syndicate if same UPI appears in multiple calls.
    """

    graph = load_graph()

    if upi not in graph:
        graph[upi] = []

    if phone not in graph[upi]:
        graph[upi].append(phone)

    save_graph(graph)

    if len(graph[upi]) > 1:
        return "🚨 SYNDICATE DETECTED"
    else:
        return "✅ New Scammer Logged"
    


    
