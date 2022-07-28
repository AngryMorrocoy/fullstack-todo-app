async function getTodos() {
  const url = `${basePath}/api/todos/`;
  const response = await axios.get(url);

  console.log(response);

  return response.data;
}

function handleTodoListClick(target) {
  const todoID = target.parentElement.id.replace('todo-', '');
  if (target.type === 'checkbox') {
    updateTodo(todoID, target.checked);
  } else if (target.classList.contains('delete-todo')) {
    deleteTodo(todoID);
  }
}

function deleteTodo(todoID) {
  const url = `${basePath}/api/todos/${todoID}/`;

  axios
    .delete(url)
    .then(() => document.querySelector(`#todo-${todoID}`).remove());
}

function updateTodo(todoID, newCompleted) {
  const url = `${basePath}/api/todos/${todoID}/`;

  axios
    .patch(url, {
      completed: newCompleted,
    })
    .then();
}
