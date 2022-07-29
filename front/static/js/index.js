async function getTodos() {
  const url = `${basePath}/api/todos/`;
  const response = await axios.get(url);

  return response.data;
}

const todoMethods = {
  edit: updateTodo,
  delete: deleteTodo,
};

function handleTodoListClick(target) {
  const method = target.getAttribute('todo-method');
  if (!method) return;

  const todoID = Number(target.getAttribute('todo-id'));
  const completed = target.checked;

  todoMethods[method]({ todoID, completed });
}

function deleteTodo({ todoID }) {
  const url = `${basePath}/api/todos/${todoID}/`;

  axios.delete(url).then(() => {
    const todoStore = Alpine.store('todos');
    todoStore.todos = todoStore.todos.filter((todo) => todo.id !== todoID);
  });
}

function updateTodo({ todoID, completed }) {
  const url = `${basePath}/api/todos/${todoID}/`;

  axios
    .patch(url, {
      completed,
    })
    .then((res) => {
      const todoStore = Alpine.store('todos');
      todoStore.todos = todoStore.todos.map((todo) => {
        if (todo.id === todoID) return res.data;
        return todo;
      });
    });
}

function createTodo({ title, completed }, onSuccess) {
  const url = `${basePath}/api/todos/`;
  const owner = window.localStorage.getItem('currentUserID');

  axios
    .post(url, { title, completed, owner })
    .then((res) => {
      onSuccess();
      Alpine.store('todos').todos.push(res.data);
    })
    .catch(console.log);
}

document.addEventListener('alpine:init', () => {
  Alpine.store('todos', {
    async init() {
      this.todos = await getTodos();
    },
    filter: '',
    todos: [],
    get filterTodos() {
      if (this.filter === 'all') return this.todos;
      return this.filter === 'active' ? this.leftTodos : this.completedTodos;
    },
    get leftTodos() {
      return this.todos.filter((todo) => !todo.completed);
    },
    get completedTodos() {
      return this.todos.filter((todo) => todo.completed);
    },
  });

  Alpine.store('darkmode', {
    on: window.localStorage.getItem('theme') || true,
    toggle() {
      this.on = !this.on;
      window.localStorage.setItem('dark-theme', this.on);
    },
  });
});
