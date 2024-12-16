<template>
  <div class="auth-container">
    <!-- Карточка пассажира -->
    <div class="auth-card">
      <h3>Я - Пассажир!</h3>
      <img class="image-container" src="@/assets/img/passenger_login.png" alt="Пассажир" />
      <div class="crd-btn">
        <button class="register_btn" @click="register('passenger')">Зарегистрироваться</button>
        <button class="login_btn" @click="login()">Войти в профиль</button>
      </div>
    </div>

    <!-- Карточка сотрудника -->
    <div class="auth-card">
      <h3>Я - Сотрудник!</h3>
      <img class="image-container" src="@/assets/img/staff_login.png" alt="Сотрудник" />
      <div class="crd-btn">
        <button class="register_btn" @click="register('staff')">Зарегистрироваться</button>
        <button class="login_btn" @click="login()">Войти в профиль</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  name: "Authorization",
  data() {
    return {};
  },
  created() {
    if (localStorage.getItem('token')) {
      this.$router.push('/');
    }
  },
  methods: {
    register(role) {
      this.$router.push({
        path: '/register',
        query: { role: role }
      });
    },
    login() {
      this.$router.push({
        path: '/login',
      });
    },
  },
  setup() {
    const router = useRouter();
    return { router };
  },
};
</script>

<style scoped>

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 170px;
  background-color: #2c3e50;
  padding: 218px 170px 250px;

  font-family: Inter,serif;
}

.auth-card {
  background-color: #ecf0f1;
  border-radius: 20px;
  width: 435px;
  height: 100%;
  padding-left: 40px;
  padding-right: 40px;
  text-align: center;
}

.auth-card h3 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 400;
  text-align: center;
  color: black;
}

.image-container {
  overflow: hidden;
  border-radius: 20px;
}

.image-container img {
  width: 345px;
  height: 345px;
  display: block;
}

.crd-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.register_btn {
  background-color: #34495e;
  color: #ecf0f1;
  border: none;
  padding: 15px 30px;
  width: 230px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 400;
  text-align: center;
  margin-bottom: 5px;
  margin-right: 40px;
}

.login_btn {
  background-color: #34495e;
  color: #ecf0f1;
  border: none;
  padding: 15px 30px;
  width: 230px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 400;
  text-align: center;
  margin-right: 150px;
  margin-bottom: 10px;
}

button:hover {
  background-color: #2c3e50;
}

button:first-of-type {
  margin-bottom: 10px;
}
</style>
