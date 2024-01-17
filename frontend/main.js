import { displayProfilPage, displayAvatar} from './modules/profilPage.js';
import { registerUser }  from './modules/register.js';
import { login } from './modules/login.js'

var path = window.location.pathname;
console.log(path);
if (!isUserLoggedIn())
  history.pushState({}, '', '/login');
else if (path === '/')
  history.pushState({}, '', '/home');
else
  history.pushState({}, '', path);

window.onload = function() {
  var path = window.location.pathname;
  switch(path) {
    case "/home":
      displayAvatar();
      hideDivs(['div_register_form', 'div_login_form']);
      showDivs(['top_box', 'game_launcher', 'friend_list'])
      break;
    case "/profil":
      displayAvatar();
      displayProfilPage();
      hideDivs(['div_register_form', 'div_login_form', 'game_launcher', 'friend_list']);
      showDivs(['top_box'])
      break;
    case "/login":
      showDivs(['div_register_form', 'div_login_form']);
      hideDivs(['top_box', 'game_launcher', 'friend_list', 'profil_page']);
      break;
  }
  console.log("load")
}

window.onpopstate = function(event) {
  var path = window.location.pathname;
  switch(path) {
    case "/home":
      displayAvatar();
      hideDivs(['div_register_form', 'div_login_form']);
      showDivs(['top_box', 'game_launcher', 'friend_list'])
      break;
    case "/profil":
      displayAvatar();
      displayProfilPage();
      hideDivs(['div_register_form', 'div_login_form', 'game_launcher', 'friend_list']);
      showDivs(['top_box'])
      break;
    case "/login":
      showDivs(['div_register_form', 'div_login_form']);
      hideDivs(['top_box', 'game_launcher', 'friend_list', 'profil_page']);
      break;
  }
  console.log("load")
 }

const loginBtn = document.getElementById('login_button');
loginBtn.addEventListener('click', async function (){
  event.preventDefault();
  await login();
  if (isUserLoggedIn()) {
    history.pushState({}, '', '/home');
    displayAvatar();
    hideDivs(['div_register_form', 'div_login_form']);
    showDivs(['top_box', 'game_launcher', 'friend_list'])
  }
  document.getElementById('login_form').reset();
})

const logoutBtn = document.getElementById('logout_button');
logoutBtn.addEventListener('click', () => {
  history.pushState({}, '', '/login');
  localStorage.removeItem('jwt_token');
  hideDivs(['top_box',  'game_launcher', 'friend_list', 'profil_page']);
  showDivs(['div_register_form', 'div_login_form']);
});

const profilBtn = document.getElementById('profil_button');
profilBtn.addEventListener('click', () => {
  history.pushState({}, '', '/profil');
  displayProfilPage();
  hideDivs(['game_launcher', 'friend_list']);
  showDivs(['profil_page']);
});

const registerBtn = document.getElementById('register_button')
  registerBtn.addEventListener('click', () => {
  event.preventDefault();
  registerUser();
  document.getElementById('register_form').reset();
});

function hideDivs(divIds) {
  divIds.forEach(function (divId) {
      var targetDiv = document.getElementById(divId);
      if (targetDiv) {
          targetDiv.style.display = 'none';
      }
  });
}

function showDivs(divIds) {
  divIds.forEach(function (divId) {
      var targetDiv = document.getElementById(divId);
      if (targetDiv) {
          targetDiv.style.display = 'block';
      }
  });
}

function isUserLoggedIn() {
  const jwtToken = localStorage.getItem('jwt_token');
  if (jwtToken !== null) {
    console.log("user connected")
    return (true)
  }
  console.log("user not  connected")
  return (false)
}


 