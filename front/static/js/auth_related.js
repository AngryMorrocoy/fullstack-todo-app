const basePath = window.location.origin;

const localStorageUtils = {
  login: (resData) => {
    window.localStorage.setItem('currentUserID', resData.user.pk);
  },
  logout: () => window.localStorage.removeItem('currentUserID'),
};

// The type must be login or logout
function authFunc(method, username, password) {
  const url = `${basePath}/auth/${method}/`;
  axios
    .post(url, {
      username,
      password,
    })
    .then((res) => {
      localStorageUtils[method](res.data);
      document.location.reload();
    })
    .catch((err) => {
      console.log(err);
    });
}

function registerUser({ username, password1, password2 }, onSuccess, onError) {
  const url = `${basePath}/auth/registration/`;
  axios
    .post(url, {
      username,
      password1,
      password2,
    })
    .then(onSuccess)
    .catch(onError);
}
