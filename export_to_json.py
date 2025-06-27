import sqlite3
import json

db_path = "data/web_graph.db"
output_path = "web_graph.json"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch nodes
cursor.execute("SELECT url, title, meta_description, h1_text, status_code, mime_type, first_seen_depth, last_updated FROM nodes")
nodes = [
    {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "h1_text": h1_text,
        "status_code": status_code,
        "mime_type": mime_type,
        "first_seen_depth": first_seen_depth,
        "last_updated": last_updated
    }
    for (url, title, meta_description, h1_text, status_code, mime_type, first_seen_depth, last_updated) in cursor.fetchall()
]

# Fetch edges
cursor.execute("SELECT parent_url, child_url, depth, discovered_at FROM edges")
edges = [
    {
        "parent_url": parent_url,
        "child_url": child_url,
        "depth": depth,
        "discovered_at": discovered_at
    }
    for (parent_url, child_url, depth, discovered_at) in cursor.fetchall()
]

# Combine into one dictionary
graph = {
    "nodes": nodes,
    "edges": edges
}

# Write to JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)

print(f"Exported to {output_path}")

conn.close() 