from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mysql%40123@db/task1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), default='Pending')

import time

def wait_for_db():
    retries = 5
    while retries:
        try:
            with app.app_context():
                db.create_all()
            print("Database is ready.")
            return
        except Exception as e:
            print(f"Database not ready, retrying... ({retries} attempts left)")
            time.sleep(5)
            retries -= 1
    print("Could not connect to the database.")


@app.route("/")
def home():
    return "Homeeee"

@app.route("/create-task", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], due_date=data['due_date'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "description": new_task.description, "due_date": new_task.due_date, "status": new_task.status}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ "id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date, "status": task.status } for task in tasks])

@app.route("/task/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date, "status": task.status})

@app.route("/task/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully."})

if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", debug=True)
