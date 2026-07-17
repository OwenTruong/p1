const logoutBtn = document.getElementById('nav_list__logout');
const loginLink = document.getElementById('nav_list__login');
const registerLink = document.getElementById('nav_list__register');
const protectedLink = document.getElementById('nav_list__protected');

const isLoggedIn = localStorage.getItem('loggedIn');

console.log('Is logged in: ', isLoggedIn);

if (isLoggedIn) {
  loginLink.classList.add('hidden');
  registerLink.classList.add('hidden');
  protectedLink.classList.remove('hidden');
  logoutBtn.classList.remove('hidden');
} else {
  loginLink.classList.add('hidden');
  registerLink.classList.remove('hidden');
  protectedLink.classList.add('hidden');
  logoutBtn.classList.add('hidden');
}

async function postRequest(
  path,
  payload = undefined,
  successCallback = undefined,
) {
  try {
    const response = await fetch(path, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      ...(payload ? { body: JSON.stringify(payload) } : {}),
    });

    if (response.status >= 200 && response.status <= 299) {
      if (successCallback) await successCallback();
    } else {
      const json = await response.json();
      console.log(json);
      alert(`Invalid registration: ${json.detail}`);
    }
  } catch (err) {
    alert('Unable to register');
    console.error(err);
  }
}

logoutBtn.addEventListener('click', async (e) => {
  e.preventDefault();

  console.log('Now logging out');
  await postRequest('/api/auth/logout', undefined, () => {
    localStorage.removeItem('loggedIn');
    window.location.replace('/');
  });
});
