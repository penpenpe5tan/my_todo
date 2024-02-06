from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 簡単なデータベース代わりに使うリスト
todos = [
    {"id": 1, "title": "Flaskを学ぶ", "completed": False},
    {"id": 2, "title": "Next.jsを学ぶ", "completed": False},
]

@app.route('/todos', methods=['GET', 'POST'])
def manage_todos():
    if request.method == 'GET':
        return jsonify(todos)
    else:  # POST
        data = request.json
        todos.append({"id": len(todos) + 1, "title": data['title'], "completed": False})
        return jsonify(todos[-1]), 201

@app.route('/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
def update_todo(todo_id):
    todo = next((item for item in todos if item["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    if request.method == 'PUT':
        data = request.json
        todo.update(data)
        return jsonify(todo)
    else:  # DELETE
        todos.remove(todo)
        return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)