import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState('');


  useEffect(() => {
    axios.get('http://localhost:5000/todos').then((response) => {
      setTodos(response.data);
    });
  }, []);

  const addTodo = () => {
    axios.post('http://localhost:5000/todos', { title: newTodo }).then((response) => {
      setTodos([...todos, response.data]);
      setNewTodo('');
    });
  };

  const startEditing = (todo) => {
    setEditingId(todo.id);
    setEditText(todo.title);
  };

  const fetchTodos = async () => {
    const response = await axios.get('http://127.0.0.1:5000/todos');
    setTodos(response.data); // 状態を更新してUIをリフレッシュ
  };
  
  const updateTodo = async (todoId, title) => {
    await axios.put(`http://127.0.0.1:5000/todos/${todoId}`, { title: editText, completed: false });
    // ToDoリストを再取得またはローカルで状態を更新してUIを更新
    fetchTodos();
    setEditingId(null);
    setEditText('');
  };
  
  const deleteTodo = async (todoId) => {
    await axios.delete(`http://127.0.0.1:5000/todos/${todoId}`);
    fetchTodos(); // ToDoリストを再取得
  };
  

  return (
    <div>
      <h1>ToDoリスト</h1>
      <input
        type="text"
        value={newTodo}
        onChange={(e) => setNewTodo(e.target.value)}
      />
      <button onClick={addTodo}>追加</button>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
          {editingId === todo.id ? (
            <input
              type="text"
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
            />
          ) : (
            todo.title
          )}
          {editingId === todo.id ? (
            <button onClick={() => updateTodo(todo.id)}>修正</button>
          ) : (
            <button onClick={() => startEditing(todo)}>編集</button>
          )}
          <button onClick={() => deleteTodo(todo.id)}>削除</button>
        </li>
        ))}
      </ul>
    </div>
  );
}