const form = document.getElementById('form-register');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');
const errorParagraph = document.getElementById('error');

console.log('hello world');

form.addEventListener('submit', async (e) => {
  event.preventDefault();
  const formData = new FormData(form);

  if (passwordInput.value != confirmPasswordInput.value) {
    event.preventDefault();
    alert('Password and Confirm Password field do not match!');
  } else {
    try {
      const response = await fetch(form.action, {
        method: form.method,
        body: formData,
      });
      window.location.replace('/protected');
    } catch (error) {
      alert('Unable to register');
      console.error(error);
    }
  }
});
