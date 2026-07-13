const form = document.getElementById('form-register');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');

async function postRequest(path, payload, successCallback = undefined) {
  try {
    const response = await fetch(path, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
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

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (passwordInput.value != confirmPasswordInput.value) {
    alert('Password and Confirm Password field do not match!');
  } else if (passwordInput.value.length < 8) {
    alert('Password length must be 8 or bigger');
  } else if (/\d/.test(passwordInput.value) === false) {
    alert('Password must contain at least one number');
  } else {
    const payload = {
      username: usernameInput.value,
      password: passwordInput.value,
    };
    console.log('Now registering');
    await postRequest('/api/auth/register', payload, async () => {
      console.log('Now logging in');
      await postRequest('/api/auth/login', payload, async () => {
        localStorage.setItem('loggedIn', true);
        window.location.replace('/protected');
      });
    });
  }
});
