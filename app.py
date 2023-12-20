from flask import Flask, request, jsonify
from models import Task

app = Flask(__name__)
tasks = [Task(1, 'Task 1', 'Description 1'), Task(2, 'Task 2', 'Description 2', True)]
API_KEY = 'your_api_key'  # I was instructed to replace this with my actual key but do I have to or can I use API_KEY for this exercise? Will test to find out

def authenticate():
    if request.headers.get('Authorization') != API_KEY:
        return jsonify({'error': 'Authentication failed'}), 401

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    auth_response = authenticate()
    if auth_response:
        return auth_response

    if request.method == 'GET':
        return jsonify([task.__dict__ for task in tasks])

    elif request.method == 'POST':
        data = request.json
        new_task = Task(len(tasks) + 1, data['title'], data['description'])
        tasks.append(new_task)
        return jsonify(new_task.__dict__), 201

@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_task(task_id):
    auth_response = authenticate()
    if auth_response:
        return auth_response

    task = next((t for t in tasks if t.id == task_id), None)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'GET':
        return jsonify(task.__dict__)

    elif request.method == 'PUT':
        data = request.json
        task.title, task.description, task.completed = (
            data.get('title', task.title),
            data.get('description', task.description),
            data.get('completed', task.completed),
        )
        return jsonify(task.__dict__)

    elif request.method == 'DELETE':
        tasks.remove(task)
        return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
