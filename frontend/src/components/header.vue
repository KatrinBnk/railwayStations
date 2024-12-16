<template>
  <header class="header-container">
    <div class="logo" @click="navigateToHome">
      <img src="@/assets/icons/logo.svg" alt="Logo">
    </div>
    <div class="header-actions">
      <div v-if="!isAuthenticated" class="login-section" @click="navigateToAuth">
        <span>Войти в профиль</span>
      </div>
      <div v-else class="user-section">
        <img src="@/assets/icons/user_icon.svg" alt="User Icon" @click="navigateToProfile" class="icon">
      </div>
      <div class="menu-section" @click="toggleMenu">
        <img src="@/assets/icons/menu_icon.svg" alt="Menu Icon" class="icon">
      </div>
    </div>
    <div v-if="showMenu" class="dropdown-menu">
      <ul>
        <li @click="navigateToStationSearch">Поиск станции</li>
        <li @click="navigateToTrainSearch">Поиск поезда</li>
        <li @click="navigateToTicketPurchase">Купить билет</li>
      </ul>
    </div>
  </header>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  name: "HeaderComponent",
  data() {
    return {
      isAuthenticated: false,
      showMenu: false,
    };
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem('token');
  },
  methods: {
    navigateToHome() {
      this.$router.push('/');
    },
    navigateToAuth() {
      this.$router.push('/auth');
    },
    navigateToProfile() {
      this.$router.push('/profile');
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    navigateToStationSearch() {
      this.showMenu = false;
      this.$router.push('/station-search');
    },
    navigateToTrainSearch() {
      this.showMenu = false;
      this.$router.push('/train-search');
    },
    navigateToTicketPurchase() {
      this.showMenu = false;
      this.$router.push('/train-search');
    },
  },
  setup() {
    const router = useRouter();
    return { router };
  },
};
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 80px 5px 40px;
  background-color: #0A1F4A;
  color: white;
}

.logo {
  cursor: pointer;
  opacity: 0.5;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.login-section, .user-section, .menu-section {
  display: flex;
  align-items: center;
  cursor: pointer;
  opacity: 0.5;
}

.login-section :hover, .user-section:hover, .menu-section:hover, .logo:hover {
  opacity: 1;
}

.icon{
  height: 100%;
  width: auto;
  opacity: 0.5;
}

.icon:hover{
  opacity: 1;
}

.login-section span {
  color: white;
  font-size: 30px;
  font-family: IBM Plex Mono,serif;
  font-weight: 400;
  margin-right: 10px;
  opacity: 0.5;
}

.login-section span:hover {
  opacity: 1;
}

.dropdown-menu {
  position: absolute;
  top: 60px;
  right: 20px;
  background-color: #42506B;
  color: #0A1F4A;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  z-index: 10;
  opacity: 0.8;
}

.dropdown-menu ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li {
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dropdown-menu li:hover {
  color: #929191;
  opacity: 1;
}
</style>
