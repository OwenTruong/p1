const form = document.getElementById('form-login');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (passwordInput.value.length < 8) {
    alert('Password length must be 8 or bigger');
  } else if (/\d/.test(passwordInput.value) === false) {
    alert('Password must contain at least one number');
  } else {
    try {
      const payload = {
        username: usernameInput.value,
        password: passwordInput.value,
      };
      const response = await fetch(form.action, {
        method: form.method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.status >= 200 && response.status <= 299) {
        window.location.replace('/protected');
      } else {
        const json = await response.json();
        console.log(json);
        alert(`Invalid login: ${json.detail}`);
      }
    } catch (error) {
      alert('Unable to login');
      console.error(error);
    }
  }
});
