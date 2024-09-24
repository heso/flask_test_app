import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
DATABASE_FILE = os.getenv("DB_NAME")

app = Flask(__name__)
def load_tasks():
    try:
        with open(DATABASE_FILE,
                  "r") as file:
            return json.load(file)
    except (FileNotFoundError,
            json.JSONDecodeError):
        return []
def save_tasks(tasks):
    with open(DATABASE_FILE, "w") as file:
        json.dump(tasks,
                  file,
                  indent=4)
@app.route("/tasks",
           methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    tasks = load_tasks()
    task = next((task for task in tasks if task["id"] == task_id), None)
    return jsonify(task)
@app.route("/tasks", methods=["POST"])
def create_task():
    tasks = load_tasks()
    new_task = {
        'id': len(tasks) + 1, "title": request.form["title"], "description": request.form.get("description", ""), "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), \
        201
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    task = next((task for task in tasks if task["id"] == task_id), None)
    task["title"] = request.form.get("title",
                                     task["title"])
    task["description"] = request.form.get("description", task["description"])
    task["done"] = request.form.get("done", "false").lower() == "true"
    save_tasks(tasks)
    return \
        jsonify(task)
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task
                     for task in tasks
                     if task["id"] != task_id]
    save_tasks(updated_tasks)
    return jsonify({"result": True})
if __name__ == "__main__":
    app.run(debug=True)
