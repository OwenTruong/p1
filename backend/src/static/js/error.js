const errorNameEl = document.getElementById('error_name');
const errorMessageEl = document.getElementById('error_message');

if (errorNameEl.textContent.includes('403')) {
  localStorage.removeItem('loggedIn');
}
