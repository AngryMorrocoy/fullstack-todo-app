const basePath = window.location.origin;

// The type must be login or logout
function authFunc(method, username, password) {
  const url = `${basePath}/auth/${method}/`;
  console.log(url)
  axios
    .post(url, {
      username,
      password,
    })
    .then((res) => {
      // console.log(res);
      document.location.reload();
    })
    .catch((err) => {
      console.log(err);
    });
}
