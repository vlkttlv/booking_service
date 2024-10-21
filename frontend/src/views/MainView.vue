<template>

    <html>
    <body>
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
    </html>
    </template>
    
    <style scoped>
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
  .search-container {
    max-width: 800px;
    margin: 2rem auto;
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
  }
  input[type="text"], input[type="date"], input[type="number"] {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .date-range, .price-range {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
  }
  .date-range input, .price-range input {
    width: 48%;
  }
  .services {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  .search-button {
    background-color: #ff6600;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    width: 100%;
  }
  .search-button:hover {
    background-color: #e55c00;
  }
    </style>