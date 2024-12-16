<template>
  <div class="train-card">
    <!-- Информация о поезде -->
    <div class="train-info">
      <div class="train-route-info>">
        <router-link
            :to="{ path: '/train-route', query: { train_id: train.train_id, date: train.corrected_date } }"
            class="route-link"
        >
          <p>{{ train.train_number }}: {{ train.start_station }} - {{ train.end_station }}</p>
        </router-link>
      </div>
      <div class="train-route">
        <h2>{{ train.departure_station }} - {{ train.arrival_station }}</h2>
        <p>{{ train.departure_date }} {{ train.departure_time }} - {{ train.arrival_date }} {{ train.arrival_time }}</p>
      </div>
      <div class="train-details">
        <span>Время в пути: {{ train.travel_time }}</span>
      </div>
    </div>

    <!-- Кнопка для показа билетов -->
    <button @click="toggleSeatsPage">
      {{ showSeatsPage ? "Скрыть билеты" : "Посмотреть билеты" }}
    </button>

    <!-- Встроенный компонент SeatsPage -->
    <SeatsPage
        v-if="showSeatsPage"
        :train="train"
        @close="showSeatsPage = false"
    />
  </div>
</template>

<script>
import SeatsPage from "@/components/seats.vue";

export default {
  name: "TrainCard",
  props: {
    train: {
      type: Object,
      required: true,
    },
  },
  created() {
    this.calculateTravelTime();
    this.calculateCorrectedDate();

  },
  data() {
    return {
      showSeatsPage: false,
    };
  },
  methods: {
    toggleSeatsPage() {
      this.showSeatsPage = !this.showSeatsPage;
    },
    calculateTravelTime() {
      try {
        // Парсим даты и времена
        const departureDateTime = new Date(`${this.train.departure_date.split('.').reverse().join('-')}T${this.train.departure_time}`);
        const arrivalDateTime = new Date(`${this.train.arrival_date.split('.').reverse().join('-')}T${this.train.arrival_time}`);

        // Вычисляем разницу во времени
        const diffInMs = arrivalDateTime - departureDateTime;
        if (diffInMs < 0) {
          throw new Error("Дата и время прибытия меньше даты и времени отправления.");
        }
        const hours = Math.floor(diffInMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffInMs % (1000 * 60 * 60)) / (1000 * 60));

        // Обновляем travel_time у объекта train
        this.train.travel_time = `${hours} ч ${minutes} мин`;
      } catch (error) {
        console.error("Ошибка при расчёте времени в пути:", error);
        this.train.travel_time = "Не удалось рассчитать";
      }
    },
    calculateCorrectedDate() {
      try {
        const departureDate = new Date(this.train.departure_date.split('.').reverse().join('-'));
        // Вычитаем day_in из даты отправления
        const correctedDate = new Date(departureDate);
        correctedDate.setDate(correctedDate.getDate() - this.train.day_in);

        // Форматируем дату обратно в строку
        this.train.corrected_date = correctedDate.toISOString().split('T')[0].split('-').reverse().join('.');
      } catch (error) {
        console.error("Ошибка при вычислении скорректированной даты:", error);
        this.train.corrected_date = "Не удалось рассчитать";
      }
    },
  },
  components: {
    SeatsPage,
  },
  watch: {
    train: {
      handler() {
        this.calculateTravelTime();
        this.calculateCorrectedDate();
      },
      deep: true,
    },
  },
};
</script>



<style scoped>
.train-card {
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
  margin: 50px;
}

.train-card:hover {
  transform: scale(1.02);
}

.train-info {
  margin-bottom: 15px;
}

.train-route {
  font-weight: bold;
  font-size: 1.2em;
}

.train-details {
  margin-top: 10px;
  font-size: 0.9em;
}

button {
  align-self: flex-end;
  padding: 10px 20px;
  background-color: #ff4c4c;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e04343;
}

.route-link {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.route-link:hover {
  text-decoration: none;
  color: black;
}
</style>
