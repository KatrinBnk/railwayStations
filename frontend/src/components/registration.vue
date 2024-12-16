<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 v-if="role === 'passenger'">Добро пожаловать!</h2>
      <div v-else-if="role === 'staff'" class="staff-message">
        Уважаемый сотрудник, для регистрации в системе обратитесь к администратору вашей станции.
      </div>
      <form v-if="role === 'passenger'" @submit.prevent="handleSubmit">
        <div v-for="(value, key) in form" :key="key" :class="{'input-group': true, 'error': errors[key]}">
          <input
              :type="key === 'password' ? 'password' : 'text'"
              v-model="form[key]"
              :placeholder="placeholders[key]"
          />
        </div>
        <button type="submit">Зарегистрироваться</button>
      </form>
      <p v-if="serverMessage" class="error-message">{{ serverMessage }}</p>
    </div>
  </div>
</template>

<script>
import { registerRequest } from "@/api/auth";
import { useRouter, useRoute } from 'vue-router';

export default {
  name: "RegisterForm",
  data() {
    return {
      form: {
        first_name: "",
        last_name: "",
        middle_name: "",
        passport: "",
        email: "",
        password: "",
      },
      errors: {
        first_name: false,
        last_name: false,
        middle_name: false,
        passport: false,
        email: false,
        password: false,
      },
      placeholders: {
        first_name: "Введите ваше имя...",
        last_name: "Введите вашу фамилию...",
        middle_name: "Введите ваше отчество...",
        passport: "Введите номер вашего паспорта...",
        email: "Введите вашу почту...",
        password: "Введите ваш пароль...",
      },
      serverMessage: null,
      role: null,
    };
  },
  created() {
    const route = useRoute();
    this.role = route.query.role;
  },
  methods: {
    async handleSubmit() {
      // Сбрасываем ошибки перед отправкой
      for (const key in this.errors) {
        this.errors[key] = !this.form[key];
      }

      if (Object.values(this.errors).some(error => error)) {
        this.serverMessage = "Заполните все поля.";
        return;
      }

      try {
        const response = await registerRequest(this.form);
        const { token } = response.data;
        // Сохраняем токен в localStorage
        localStorage.setItem('token', token);
        localStorage.setItem('role', "passenger")
        this.serverMessage = null;
        this.$router.push('/');
      } catch (error) {
        // Обработка ошибок сервера
        this.serverMessage = error.response?.data?.error || "Произошла ошибка. Повторите попытку.";
      }
    },
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    return { router, route };
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
  width: 400px;
  text-align: center;
  align-items: center;
}

h2 {
  color: #34495e;
  margin-bottom: 30px;
  font-size: 24px;
}

.staff-message {
  color: #34495e;
  font-size: 18px;
}

.input-group {
  margin-bottom: 10px;
  margin-right: 20px;
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
  margin-top: 20px;
}

button:hover {
  background-color: #2c3e50;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 15px;
}
</style>
