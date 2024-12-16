<template>

  <MainHeader />

  <header class="header">
    <button v-if="role === 'staff'" @click="goToStaffPage">
      Страница кассира
    </button>
    <button v-if="role === 'admin'" @click="goToAdminPage">
      Страница администратора
    </button>
    <button @click="logout">
      Выйти из системы
    </button>
  </header>

  <MyTickets />

  <!-- Что должно быть в профиле?
  - просмотр билетов (если пользователь пассажир)
  - если же пользователь кассир, то у него должна быть ссылка на вкладку: Заявки на возврат, подтверждение покупки
  -->

</template>


<script>
import MainHeader from "@/components/header.vue";
import MyTickets from "@/components/myTickets.vue";
export default {
  name: "ProfilePage",
  components: {
    MainHeader,
    MyTickets
  },
  data() {
    return {
      role: null
    };
  },
  created() {
    this.role = localStorage.getItem('role');
  },
  methods: {
    logout() {
      localStorage.clear(); // Очищаем все данные из локального хранилища
      this.$router.push('/'); // Перенаправление на главную страницу
    },
    goToStaffPage() {
      this.$router.push('/cashier'); // Перенаправление на страницу сотрудника
    },
    goToAdminPage() {
      this.$router.push('/admin'); // Перенаправление на страницу сотрудника
    },
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding: 20px 50px 0;
  margin-bottom: 20px;
}
.header button {
  padding: 10px 15px;
  background-color: red;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 17px;
}

.header button:hover {
  background-color: purple;
}

</style>