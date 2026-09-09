import json
from flask import Flask, render_template, request, jsonify
import uninformed
import informed

app = Flask(__name__)

# JSON ဖိုင်ထဲက မြေပုံ Data များကို ဖတ်ယူခြင်း
with open("map_data.json", "r", encoding="utf-8") as f:
    MAP_DATA = json.load(f)

NODES = MAP_DATA["nodes"]
GRAPH = MAP_DATA["graph"]

# Algorithm တစ်ခုစီအတွက် ရှင်းလင်းချက် (Concept Notes)
CONCEPT_NOTES = {
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "main_idea": "Explores nodes level-by-level starting from the source node.",
        "node_selection": "Selects the oldest unvisited node in frontier (FIFO queue).",
        "information_used": "Uses tree depth without considering path costs."
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "main_idea": "Explores as deep as possible along each branch before backtracking.",
        "node_selection": "Selects the most recently added node in frontier (LIFO stack).",
        "information_used": "Uses search depth."
    },
    "ucs": {
        "name": "Uniform-Cost Search (UCS)",
        "main_idea": "Expands nodes in order of cumulative path cost from the start node.",
        "node_selection": "Selects node with lowest cumulative path cost g(n).",
        "information_used": "Uses actual road distances g(n)."
    },
    "ids": {
        "name": "Iterative Deepening Search (IDS)",
        "main_idea": "Combines DFS's spatial memory efficiency with BFS's level completeness.",
        "node_selection": "Selects nodes according to depth-limited search iteration.",
        "information_used": "Uses search tree depth limits."
    },
    "greedy": {
        "name": "Greedy Best-First Search",
        "main_idea": "Expands the node estimated to be closest to the goal.",
        "node_selection": "Selects node with lowest heuristic value h(n).",
        "information_used": "Uses straight-line distance heuristic h(n)."
    },
    "astar": {
        "name": "A* Search",
        "main_idea": "Balances actual cost from start and estimated cost to goal.",
        "node_selection": "Selects node with lowest total score f(n) = g(n) + h(n).",
        "information_used": "Uses both actual road distance g(n) and heuristic h(n)."
    }
}

@app.route("/")
def index():
    return render_template("index.html", cities=sorted(list(NODES.keys())))

@app.route("/get_map_data")
def get_map_data():
    return jsonify(MAP_DATA)

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    start = data.get("source")
    goal = data.get("destination")
    algo = data.get("algorithm")

    if algo == "bfs":
        path, cost, expanded = uninformed.bfs(GRAPH, start, goal)
    elif algo == "dfs":
        path, cost, expanded = uninformed.dfs(GRAPH, start, goal)
    elif algo == "ucs":
        path, cost, expanded = uninformed.ucs(GRAPH, start, goal)
    elif algo == "ids":
        path, cost, expanded = uninformed.ids(GRAPH, start, goal)
    elif algo == "greedy":
        path, cost, expanded = informed.greedy_bfs(GRAPH, NODES, start, goal)
    elif algo == "astar":
        path, cost, expanded = informed.a_star(GRAPH, NODES, start, goal)
    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    return jsonify({
        "path": path,
        "cost": cost,
        "expanded_nodes": expanded,
        "concept": CONCEPT_NOTES.get(algo, {})
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)