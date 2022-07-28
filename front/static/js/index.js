async function getTodos() {
  const url = `${basePath}/api/todos/`;
  const response = await axios.get(url);

  console.log(response);

  return response.data;
}

function handleTodoListClick(target) {
  if (target.type !== 'checkbox') return;
  const todoID = target.parentElement.id;

  const url = `${basePath}/api/todos/${todoID}/`;

  axios
    .patch(url, {
      completed: target.checked,
    })
    .then(console.log);
}
