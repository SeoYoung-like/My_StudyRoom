const loginInput = document.querySelector("#login-form input");
const loginForm = document.querySelector("#login-form");
const h1 = document.querySelector("#greeting");

const HIDDEN_CLASSNAME = "hidden";

function onLoginSubmit(event) {
  event.preventDefault();
  loginForm.classList.add(HIDDEN_CLASSNAME);
  const username = loginInput.value;
  h1.innerText = `Hello ${username}`;
  h1.classList.remove(HIDDEN_CLASSNAME);
}

loginForm.addEventListener("submit", onLoginSubmit);