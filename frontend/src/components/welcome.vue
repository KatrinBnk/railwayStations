<template>
  <div class="welcome-container">
    <div class="background-image"></div>
    <div class="text-content">
      <div class="welcome-message">
        Добро пожаловать!
      </div>
      <div class="info-message">
        Сейчас вы находитесь в системе, которая поможет вам найти идеальный поезд для путешествия. Выбирая поезд для своего путешествия, вы выбираете не только комфорт, но и сокращение выбросов CO2.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WelcomeBlock",
};
</script>

<style scoped>
.welcome-container {
  position: relative;
  width: 100%;
  height: 100vh; /* Высота контейнера равна высоте экрана */
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/main_font');
  background-size: cover;
  background-position: center;
  z-index: 1; /* Задний план */
}

.text-content {
  position: relative;
  z-index: 2; /* Передний план */
  text-align: center;
  color: #fff; /* Белый текст */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.welcome-message {
  background: rgba(0, 0, 0, 0.6); /* Полупрозрачный фон */
  padding: 15px 30px;
  border-radius: 15px;
  font-size: 2em;
  font-weight: bold;
}

.info-message {
  background: rgba(0, 0, 0, 0.6); /* Полупрозрачный фон */
  padding: 20px;
  border-radius: 15px;
  max-width: 600px;
  font-size: 1.2em;
}
</style>
