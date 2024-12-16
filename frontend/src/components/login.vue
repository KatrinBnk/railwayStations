<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>Рады снова видеть вас!</h2>
      <form @submit.prevent="handleSubmit">
        <div :class="{'input-group': true, 'error': errors.email}">
          <input
              type="email"
              v-model="form.email"
              placeholder="Введите вашу почту..."
          />
        </div>
        <div :class="{'input-group': true, 'error': errors.password}">
          <input
              type="password"
              v-model="form.password"
              placeholder="Введите ваш пароль..."
          />
        </div>
        <button type="submit">Войти в профиль</button>
      </form>
      <p v-if="serverMessage" class="error-message">{{ serverMessageText }} <a v-if="showAuthLink" href="#" @click.prevent="navigateToAuth">{{ authLinkText }}</a></p>
    </div>
  </div>
</template>

<script>
import { loginRequest } from "@/api/auth";
import { useRouter } from 'vue-router';

export default {
  name: "LoginForm",
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      errors: {
        email: false,
        password: false,
      },
      serverMessage: null,
      serverMessageText: '',
      showAuthLink: false,
      authLinkText: '',
    };
  },
  computed: {
  },
  methods: {
    navigateToAuth() {
      if (typeof this.$router.push === 'function') {
        this.$router.push('/auth');
      } else {
        console.error('Router is not properly initialized');
      }
      this.$router.push('/auth');
    },
    async handleSubmit() {
      // Сбрасываем ошибки перед отправкой
      this.errors.email = !this.form.email;
      this.errors.password = !this.form.password;

      if (!this.form.email || !this.form.password) {
        this.serverMessage = "Заполните все поля.";
        return;
      }
      try {
        const response = await loginRequest(this.form);
        const { token, role } = response.data;
        // Сохраняем токен и роль в localStorage
        localStorage.setItem('token', token);
        localStorage.setItem('role', role);
        this.serverMessage = null; // Очистка сообщения
        // Перенаправление на главную страницу
        this.$router.push('/');
      } catch (error) {
        const status = error.response?.status;
        const errorMessage = error.response?.data?.error;

        if (status === 404) {
          this.serverMessageText = errorMessage;
          this.showAuthLink = true;
          this.authLinkText = 'Пожалуйста, зарегистрируйтесь';
        } else if (status === 500) {
          this.serverMessageText = 'Произошла ошибка на сервере. Пожалуйста, повторите вход позднее.';
          this.showAuthLink = false;
        } else {
          this.serverMessageText = errorMessage;
          this.showAuthLink = true;
          this.authLinkText = 'Перейдите на страницу регистрации';
        }
      }
    },
  },
  setup() {
    const router = useRouter();
    return {router};
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #2c3e50;
}

.auth-box {
  background-color: #ecf0f1;
  padding: 40px;
  border-radius: 20px;
  width: 500px;
  text-align: center;
  align-items: center;
}

h2 {
  color: #34495e;
  margin-bottom: 30px;
  font-size: 24px;
}

.input-group {
  margin: 20px 40px 20px 0;
}

.input-group input {
  width: 100%;
  padding: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 30px;
  font-size: 16px;
  background-color: #b0bec5;
  color: #2c3e50;
}

.input-group.error input {
  border-color: red;
}

button {
  background-color: #34495e;
  color: #ecf0f1;
  border: none;
  padding: 15px;
  width: 70%;
  border-radius: 30px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #2c3e50;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 15px;
}

.error-message a {
  color: red;
  text-decoration: underline;
  cursor: pointer;
}
</style>
