async function getTodos() {
  const url = `${basePath}/api/todos/`;
  const response = await axios.get(url);

  return response.data;
}

function handleTodoListClick(target, onSuccess) {
  const todoID = target.parentElement.id.replace('todo-', '');
  if (target.type === 'checkbox') {
    updateTodo(todoID, target.checked, onSuccess);
  } else if (target.classList.contains('delete-todo')) {
    deleteTodo(todoID, onSuccess);
  }
}

function deleteTodo(todoID, onSuccess) {
  const url = `${basePath}/api/todos/${todoID}/`;

  axios.delete(url).then(onSuccess);
}

function updateTodo(todoID, completed, onSuccess) {
  const url = `${basePath}/api/todos/${todoID}/`;

  axios
    .patch(url, {
      completed,
    })
    .then(onSuccess);
}

function createTodo(title, onSuccess) {
  const url = `${basePath}/api/todos/`;
  const owner = window.localStorage.getItem('currentUserID');

  axios.post(url, { title, owner }).then(onSuccess).catch(console.log);
}
