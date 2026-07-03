import json
import os
import uuid
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title", "").strip()
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
        
    tasks = load_tasks()
    new_task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    
    return jsonify(new_task), 201

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [t for t in tasks if t.get("id") != task_id]
    
    if len(tasks) == initial_length:
        return jsonify({"error": "Task not found"}), 404
        
    save_tasks(tasks)
    return jsonify({"message": "Task deleted successfully"}), 200

@app.route("/tasks/<task_id>", methods=["PATCH"])
def toggle_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t.get("id") == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    data = request.get_json()
    if "completed" in data:
        task["completed"] = data["completed"]
        save_tasks(tasks)
        return jsonify(task), 200
        
    return jsonify({"error": "No valid fields to update"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
