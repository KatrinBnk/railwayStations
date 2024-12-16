<template>
  <div class="search-container">
    <!-- колонка левая -->
    <div class="search">
      <h1>Найти станцию</h1>
      <div class="search-forms">
        <div class="search-box">
          <input v-model="stationName" type="text" placeholder="Поиск станции по имени" />
          <button @click="searchByName">Найти</button>
        </div>
        <div class="search-box">
          <input v-model="stationCode" type="text" placeholder="Поиск станции по коду" />
          <button @click="searchByCode">Найти</button>
        </div>
        <div class="search-box">
          <input v-model="stationCity" type="text" placeholder="Поиск станции по городу" />
          <button @click="searchByCity">Найти</button>
        </div>
      </div>
    </div>

    <!-- колонка правая -->
    <div class="search-results" v-if="results.length > 0 || errorMessage">
      <h2>Результаты поиска</h2>
      <div v-if="searchType">
        <p class="search-type-message">Вы осуществили поиск по: <strong>{{ searchType }}</strong></p>
      </div>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <div v-else>
        <div class="result-item" v-for="(result, index) in results" :key="index">
          <p><strong>Город:</strong> {{ result.city }}</p>
          <p><strong>Станция:</strong> {{ result.name }}</p>
          <p><strong>Код станции:</strong> {{ result.station_code }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { searchStationByName, searchStationByCode, searchStationByCity } from '@/api/stations';

export default {
  name: 'StationSearch',
  data() {
    return {
      stationName: '',
      stationCode: '',
      stationCity: '',
      results: [],
      errorMessage: '',
      searchType: '',
    };
  },
  methods: {
    async searchByName() {
      if (this.stationName.trim() !== '') {
        try {
          const response = await searchStationByName(this.stationName);
          this.results = response;
          this.errorMessage = '';
          this.searchType = `имени: ${this.stationName}`;
        } catch (error) {
          if (error.response && error.response.status === 404) {
            this.errorMessage = 'По вашему запросу ничего не было найдено';
            this.results = [];
            this.searchType = `имени: ${this.stationName}`;
          } else {
            console.error('Ошибка при поиске по имени:', error);
          }
        }
      }
    },
    async searchByCode() {
      if (this.stationCode.trim() !== '') {
        try {
          const response = await searchStationByCode(this.stationCode);
          this.results = response;
          this.errorMessage = '';
          this.searchType = `коду: ${this.stationCode}`;
        } catch (error) {
          if (error.response && error.response.status === 404) {
            this.errorMessage = 'По вашему запросу ничего не было найдено';
            this.results = [];
            this.searchType = `коду: ${this.stationCode}`;
          } else {
            console.error('Ошибка при поиске по коду:', error);
          }
        }
      }
    },
    async searchByCity() {
      if (this.stationCity.trim() !== '') {
        try {
          const response = await searchStationByCity(this.stationCity);
          this.results = response;
          this.errorMessage = '';
          this.searchType = `городу: ${this.stationCity}`;
        } catch (error) {
          if (error.response && error.response.status === 404) {
            this.errorMessage = 'По вашему запросу ничего не было найдено';
            this.results = [];
            this.searchType = `городу: ${this.stationCity}`;
          } else {
            console.error('Ошибка при поиске по городу:', error);
          }
        }
      }
    },
  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  gap: 30px;
  padding: 40px;
  background-color: #2D3E50;
  color: #ffffff;
  min-height: 100vh;
  height: auto;
}

.search {
  flex: 1;
  max-width: 40%;
  margin-top: 0;
}

.search-results {
  flex: 1;
  background-color: #E0E0E0;
  padding: 40px;
  border-radius: 15px;
  color: #000;
  margin-top: 21px;
}

h1 {
  text-align: center;
  font-size: 2em;
  background: #C4C4C4;
  padding: 20px;
  border-radius: 15px;
  color: #000;
  margin-bottom: 30px;
}

.search-forms {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  gap: 10px;
  align-items: center;
}

input[type="text"] {
  padding: 15px;
  border-radius: 25px;
  border: 1px solid #ccc;
  flex-grow: 1;
  font-size: 1em;
  background: #D9D9D9;
}

button {
  padding: 15px 30px;
  background-color: #D9D9D9;
  color: #2D3E50;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1em;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #f0f0f0;
  transform: scale(1.05);
}

.error-message {
  color: red;
  font-weight: bold;
}

.search-type-message {
  margin-bottom: 10px;
  font-weight: bold;
  color: #333333;
}

.result-item {
  background-color: #D9D9D9;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  color: #000;
}

.result-item:hover {
  background-color: #D8D8D8;
  transform: scale(1.02);
  opacity: 1;
}

h2 {
  font-size: 1.9em;
  margin-top: 0;
  font-weight: bold;
  color: black;
}

.search-results{
  opacity: 0.8;
}
</style>
