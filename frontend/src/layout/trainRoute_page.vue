<template>
  <MainHeader />

  <div class="train-route">
    <div class="train-route__header">
    <h2>Маршрут поезда №{{ this.train }}</h2>
    <p v-if="date">Дата отправления: {{ date }}</p>
    </div>
    <table v-if="route.length" class="route-table">
      <thead>
      <tr>
        <th>№</th>
        <th>Станция</th>
        <th>Дата прибытия</th>
        <th>Время прибытия</th>
        <th>Дата отправления</th>
        <th>Время отправления</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(station, index) in route" :key="index">
        <td>{{ index + 1 }}</td>
        <td>{{ station.station_name }}</td>
        <td>{{ station.arrival_date || '-' }}</td>
        <td>{{ station.arrival_time || '-' }}</td>
        <td>{{ station.departure_date || '-' }}</td>
        <td>{{ station.departure_time || '-' }}</td>
      </tr>
      </tbody>
    </table>
    <p v-else>Маршрут не найден.</p>
  </div>
</template>

<script>
import axios from "axios";
import MainHeader from "@/components/header.vue";

export default {
  name: "TrainRoute",
  components: {MainHeader},
  data() {
    return {
      route: [],
      date: null,
      train: null
    };
  },
  computed: {
    trainId() {
      return this.$route.query.train_id; // Извлекаем train_id из query
    },
  },
  async created() {
    await this.fetchTrainRoute();
  },
  methods: {
    async fetchTrainRoute() {
      try {
        const date = this.$route.query.date;
        const response = await axios.get(`http://127.0.0.1:5000/trains/train_id=${this.trainId}`, {
          params: { date },
        });

        this.route = response.data.route;
        this.date = response.data.date;
        this.train = response.data.train_number
      } catch (error) {
        console.error("Ошибка при загрузке маршрута поезда:", error);
        alert("Не удалось загрузить маршрут поезда.");
      }
    },
  },
};
</script>

<style scoped>
.train-route {
  padding: 20px;
  font-size: 20px;
}

.train-route__header{
  color: #D9D9D9;
}

.route-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: white; /* Устанавливаем белый фон для таблицы */
  border-radius: 8px; /* Добавляем закругление углов */
  overflow: hidden; /* Скрываем части за пределами */
  opacity: 0.75;
}

.route-table th,
.route-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.route-table th {
  background-color: #f4f4f4; /* Серый фон для заголовков */
}

.route-table tr:nth-child(even) {
  background-color: #f9f9f9; /* Светлый фон для чётных строк */
}

.route-table tr:hover {
  background-color: #f1f1f1; /* Светлый фон при наведении */
}

</style>
