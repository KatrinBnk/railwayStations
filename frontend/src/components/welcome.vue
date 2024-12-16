<template>
  <div class="welcome-container">
    <img src="@/assets/img/main_font.png" alt="Фон" class="background-image" />
    <div class="text-content">
      <div class="welcome-message">
        Добро пожаловать!
      </div>
      <div class="info-message">
        Сейчас вы находитесь в системе, которая поможет вам найти идеальный поезд для путешествия
      </div>
      <div class="info-message-small">
        Выбирая поезд для своего путешествия, вы выбираете не только комфорт, но и сокращение выбросов CO2.
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
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.background-image {
  position: absolute;
  width: 100%;
  height: auto;
  margin-top: 250px;
  object-fit: cover;
  z-index: 1;
  background-position: top left;
  background-size: cover;
}

.text-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  max-width: 500px;
}

.welcome-message {
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 1.8em;
  font-weight: bold;
}

.info-message {
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 15px;
  border-radius: 20px;
  font-size: 1.1em;
}

.info-message-small {
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 1em;
  max-width: 80%;
}
</style>
