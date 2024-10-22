<!-- <script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->



<!-- <html>
    <head><base href="https://nabroniroval.com/">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Набронировал - Поиск отелей</title>
    
    </head>
    <body>
      <header>
        <div class="logo">Набронировал</div>
        <div class="user-actions">
          <button id="my-bookings">Мои брони</button>
          <button id="login-register">Вход / Регистрация</button>
        </div>
      </header>
    
      <div class="search-container">
        <form id="hotel-search">
          <input type="text" id="search" placeholder="Введите название города или отеля">
          
          <div class="date-range">
            <input type="date" id="check-in" required>
            <input type="date" id="check-out" required>
          </div>
          
          <div class="price-range">
            <input type="number" id="min-price" placeholder="Мин. цена">
            <input type="number" id="max-price" placeholder="Макс. цена">
          </div>
          
          <div class="services">
            <label><input type="checkbox" name="service" value="wifi"> Wi-Fi</label>
            <label><input type="checkbox" name="service" value="parking"> Парковка</label>
            <label><input type="checkbox" name="service" value="breakfast"> Завтрак</label>
            <label><input type="checkbox" name="service" value="pool"> Бассейн</label>
            <label><input type="checkbox" name="service" value="gym"> Спортзал</label>
            <label><input type="checkbox" name="service" value="restaurant"> Ресторан</label>
          </div>
          
          <button type="submit" class="search-button">Найти отели</button>
        </form>
      </div>
    
    </body>
    </html> -->
<template>
  <body>
    <header>
      <a class="navbar-brand" href="#" @click="onClickLogo">
      <div class="logo">Набронировал</div>
      </a>
        <nav class="user-actions">
          <RouterLink to="/Register">Вход/Регистрация</RouterLink>
          <RouterLink to="/Login">Мои брони (логин)</RouterLink>
        </nav>
    </header>
  <main>
    <RouterView />
  </main>
  </body>
</template>
<script>
export default {
  methods: {
    onClickLogo() {
      this.$router.push('/'); // Переход на домашнюю страницу
    }
  }
};
</script>
<style>

  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f0f0;
  }
  header {
    background-color: #003366;
    color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .logo {
    font-size: 1.5rem;
    font-weight: bold;
  }
  .user-actions {
        display: flex;
        gap: 1rem;
      }
  .user-actions button {
    background-color: transparent;
    border: 1px solid white;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
  }
  .user-actions button:hover {
    background-color: white;
    color: #003366;
  }
</style>
