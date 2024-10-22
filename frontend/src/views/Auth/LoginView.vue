<template>

<!-- <div class="auth-container">
    <h1>Войти в аккаунт</h1>
    <form id="login-form">
      <input type="email" id="email" placeholder="Email" required>
      <input type="password" id="password" placeholder="Пароль" required>
      <button type="submit">Войти</button>
    </form>
    <div class="register">
       Еще нет аккаунта?<RouterLink to="/Register"> Зарегистрироваться</RouterLink>
    </div>
  </div> -->






    <div class="login">
      <h1>Войти в аккаунт</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Электронная почта:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Пароль:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
          />
        </div>
        <button type="submit">Войти</button>
      </form>
      <p v-if="message">{{ message }}</p>

      <div class="register">
       Еще нет аккаунта? <RouterLink to="/Register">Зарегистрироваться</RouterLink>
      </div>
    </div>
  </template>
  
  <!-- document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Here you would typically send this data to your backend or API for authentication
    console.log('Login attempt:', { email, password });
    
    // For demonstration purposes, we'll just show an alert
    alert('Попытка входа выполнена! Проверьте консоль для деталей.');
    
    // In a real application, you would handle the server response here
    // For example:
    // if (response.success) {
    //   window.location.href = 'https://nabroniroval.com/dashboard';
    // } else {
    //   showErrorMessage(response.error);
    // }
  });

  function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.color = 'red';
    errorDiv.style.marginTop = '1rem';
    errorDiv.textContent = message;
    document.querySelector('.auth-container').appendChild(errorDiv);
  } -->


  <script>
  import axios from 'axios';
  async function handleSubmit() {
            const url = "http://localhost:8000/v1/auth/register";
            const formData = new FormData();
            formData.append('email', document.getElementById("email").value);
            formData.append('password', document.getElementById("password").value);

            await fetch(url, {
                method: 'POST',
                body: formData,
            }).then(response => {
                if (response.status === 201) {
                    window.location.href = "/pages/login"
                }
            });
        }

  

  export default {
    data() {
      return {
        email: '',
        password: '',
      };
    },
    methods: {
      handleSubmit
    }
  };

  

</script>
  
  <style scoped>
  .login {
    max-width: 400px;
    margin: auto;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    align-items: center;
    display: block;
    margin-top: 50px;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  label {
    margin-bottom: .5em;
    color: #333333;
    display: block;
  }
  
  input {
    border: 1px solid #CCCCCC;
    padding: .5em;
    width: 100%;
    box-sizing: border-box;
  }
  
  button {
    padding: .5em;
    color: white;
    background-color: #007BFF;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  p {
    margin-top: 1em;
    color: rgb(0, 0, 0);
  }
  .register {
    margin-top: 10px;
  }
  </style>





<!-- body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.auth-container {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  width: 300px;
}
.logo {
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #003366;
  margin-bottom: 1rem;
}
form {
  display: flex;
  flex-direction: column;
}
input {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  background-color: #ff6600;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
button:hover {
  background-color: #e55c00;
}
.forgot-password {
  text-align: right;
  margin-top: 0.5rem;
}
.forgot-password a {
  color: #003366;
  text-decoration: none;
  font-size: 0.9rem;
}
.register {
  text-align: center;
  margin-top: 1rem;
}
.register a {
  color: #003366;
  text-decoration: none;
} -->