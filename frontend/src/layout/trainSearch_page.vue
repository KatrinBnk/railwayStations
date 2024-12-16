<template>
  <div class="train-search-container">
    <MainHeader />
    <div class="train-search">
    <SearchHeader
        v-model:departure="departure"
        v-model:destination="destination"
        v-model:travelDate="travelDate"
        @update:departureCode="departureCode = $event"
        @update:destinationCode="destinationCode = $event"
        @search="searchTrain"
    />
    <div v-if="trains.length" class="results">
      <TrainCard
          v-for="train in trains"
          :key="train.train_id"
          :train="train"
      />
    </div>
    </div>
  </div>
</template>

<script>
import MainHeader from "@/components/header.vue";
import SearchHeader from "@/components/trainHeader.vue";
import TrainCard from "@/components/trainCard.vue";
import axios from "axios";
import { searchStationByCode } from "@/api/stations.js";

export default {
  name: "TrainSearch",
  components: {
    SearchHeader,
    TrainCard,
    MainHeader,
  },
  data() {
    return {
      departure: "",
      destination: "",
      travelDate: "",
      trains: [],
      departureCode: null,
      destinationCode: null,
    };
  },
  created() {
    const { departure_station_id, arrival_station_id, date } = this.$route.query;

    if (departure_station_id) {
      this.departureCode = departure_station_id;
      this.fetchStationNameByCode(departure_station_id, "departure");
    }

    if (arrival_station_id) {
      this.destinationCode = arrival_station_id;
      this.fetchStationNameByCode(arrival_station_id, "destination");
    }

    if (date) {
      this.travelDate = this.parseDate(date);
    }
  },
  methods: {
    async fetchStationNameByCode(code, type) {
      try {
        console.log(`Получение названия для кода: ${code}, тип: ${type}`);
        const stations = await searchStationByCode(code); // Ожидаем массив
        console.log("Полученная станция:", stations);

        if (stations && stations.length > 0) {
          const station = stations[0]; // Берем первый элемент массива
          if (type === "departure") {
            this.departure = station.name;
            console.log("Установлено departure:", this.departure);
          } else if (type === "destination") {
            this.destination = station.name;
            console.log("Установлено destination:", this.destination);
          }
        } else {
          console.warn(`Станция с кодом ${code} не найдена`);
          if (type === "departure") {
            this.departure = "Неизвестная станция";
          } else if (type === "destination") {
            this.destination = "Неизвестная станция";
          }
        }
      } catch (error) {
        console.error(`Ошибка при получении названия станции (${type}):`, error);
        if (type === "departure") {
          this.departure = "Ошибка загрузки станции";
        } else if (type === "destination") {
          this.destination = "Ошибка загрузки станции";
        }
      }
    },
    parseDate(formattedDate) {
      const [day, month, year] = formattedDate.split(".");
      return `${year}-${month}-${day}`;
    },
    formatTravelDate(date) {
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
    async searchTrain() {
      if (!this.departureCode || !this.destinationCode || !this.travelDate) {
        alert("Пожалуйста, заполните все поля корректно!");
        console.log(this.departureCode, " ", this.destinationCode, " ", this.travelDate);
        return;
      }

      try {
        const formattedDate = this.formatTravelDate(this.travelDate);
        const trains = await this.fetchTrains(
            this.departureCode,
            this.destinationCode,
            formattedDate
        );
        this.trains = trains;

        this.updateQueryParams();
      } catch (error) {
        console.error("Ошибка при поиске поездов:", error);
        alert("Не удалось найти поезда. Попробуйте еще раз.");
      }
    },
    async fetchTrains(departureCode, destinationCode, date) {
      try {
        const response = await axios.get("http://127.0.0.1:5000/trains/search", {
          params: {
            departure_station_id: departureCode,
            arrival_station_id: destinationCode,
            date: date,
          },
        });
        console.log("Ответ API:", response.data);

        const trains = response.data.map((train) => ({
          ...train,
          departure_station_id: departureCode, // Добавляем код отправления
          arrival_station_id: destinationCode, // Добавляем код прибытия
        }));

        return trains;
      } catch (error) {
        console.error("Ошибка при выполнении запроса на поиск поездов:", error);
        throw error;
      }
    },
    updateQueryParams() {
      const formattedDate = this.formatTravelDate(this.travelDate);

      this.$router.replace({
        name: "TrainSearch",
        query: {
          departure_station_id: this.departureCode,
          arrival_station_id: this.destinationCode,
          date: formattedDate,
        },
      });
    },
  },
};
</script>

<style >

body {
  background-image: url('C:/pyprogects/railwayStations/frontend/src/assets/img/train_background.png'); /* Укажите путь к изображению */
  background-size: cover; /* Заполняет весь фон, сохраняя пропорции */
  background-position: center; /* Центрируем изображение */
  background-repeat: no-repeat; /* Изображение не повторяется */
  background-attachment: fixed; /* Фон остается зафиксированным при прокрутке */
  box-sizing: border-box; /* Гарантируем корректный расчет отступов */
  min-height: 100vh; /* Устанавливаем минимальную высоту, чтобы фон всегда занимал весь экран */
}

</style>
