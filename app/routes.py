from flask import Blueprint, request, jsonify
from .models import Task
from . import db

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return "Homeeee"

# API endpoint to "create a new task" 
@routes.route("/create-task", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], due_date=data['due_date'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "description": new_task.description, "due_date": new_task.due_date, "status": new_task.status}), 201

# API endpoint to "get all tasks"
@routes.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ "id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date, "status": task.status } for task in tasks])

# API endpoint to "update an existing task"
@routes.route("/task/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date, "status": task.status})

# API endpoint to "delete a task"
@routes.route("/task/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully."})
