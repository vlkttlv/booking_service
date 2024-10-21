<template>
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

      <div class="login">
       Еще нет аккаунта?<RouterLink to="/Register">Зарегистрироваться</RouterLink>
       </div>
    </div>

  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: '',
      };
    },
    methods: {
      handleSubmit() {
        // Здесь вы можете добавить логику для обработки регистрации
        // Например, отправка данных на сервер
        if (this.email && this.password) {
          this.message = 'Вы успешно зарегистрировались!';
          // Здесь можно сделать запрос на сервер для сохранения пользователя
        }
      },
    },
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
  </style>