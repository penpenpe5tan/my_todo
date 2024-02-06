from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS


from config import * #設定ファイルの名前
conf = config() #設定ファイルから読み込み

app = Flask(__name__)
app.config['DEBUG'] = conf.debug
CORS(app)

# MySQLデータベース設定
app.config['MYSQL_HOST'] = conf.host
app.config['MYSQL_USER'] = conf.user
app.config['MYSQL_PASSWORD'] = conf.password
app.config['MYSQL_DB'] = conf.db
mysql = MySQL(app)


    
@app.route('/todos', methods=['GET'])
def get_todos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos")
    rv = cur.fetchall()
    todos = [{'id': row[0], 'title': row[1], 'completed': row[2]} for row in rv]
    cur.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO todos (title, completed) VALUES (%s, %s)", (data['title'], False))
    mysql.connection.commit()
    cur.close()
    return jsonify({'title': data['title'], 'completed': False})

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todos SET title = %s, completed = %s WHERE id = %s", (data['title'], data['completed'], todo_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'id': todo_id, 'title': data['title'], 'completed': data['completed']})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Todo deleted'})