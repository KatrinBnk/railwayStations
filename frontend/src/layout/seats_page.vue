<template>
  <div class="train-search-container">
    <MainHeader />
    <SearchHeader
        v-model:departure="departure"
        v-model:destination="destination"
        v-model:travelDate="travelDate"
        @update:departureCode="departureCode = $event"
        @update:destinationCode="destinationCode = $event"
        @search="searchTrain"
    />

    <div v-if="selectedTrain" class="seats-container">
      <Seats
          :train="selectedTrain"
          @back="clearSelectedTrain"
      />
    </div>

    <div v-else-if="trains.length" class="results">
      <TrainCard
          v-for="train in trains"
          :key="train.train_id"
          :train="train"
          @select="selectTrain(train)"
      />
    </div>

    <div v-else>
      <p>Нет доступных поездов.</p>
    </div>
  </div>
</template>

<script>
import MainHeader from "@/components/header.vue";
import SearchHeader from "@/components/trainHeader.vue";
import TrainCard from "@/components/trainCard.vue";
import Seats from "@/components/seats.vue";
import axios from "axios";
import { searchStationByCode } from "@/api/stations.js";

export default {
  name: "TrainSearch",
  components: {
    SearchHeader,
    TrainCard,
    MainHeader,
    Seats,
  },
  data() {
    return {
      departure: "",
      destination: "",
      travelDate: "",
      trains: [],
      departureCode: null,
      destinationCode: null,
      selectedTrain: null, // Выбранный поезд
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
        const stations = await searchStationByCode(code);
        if (stations && stations.length > 0) {
          const station = stations[0];
          if (type === "departure") {
            this.departure = station.name;
          } else if (type === "destination") {
            this.destination = station.name;
          }
        }
      } catch (error) {
        console.error(`Ошибка при получении названия станции (${type}):`, error);
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

        const trains = response.data.map((train) => ({
          ...train,
          departure_station_id: departureCode,
          arrival_station_id: destinationCode,
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
    selectTrain(train) {
      this.selectedTrain = train;
    },
    clearSelectedTrain() {
      this.selectedTrain = null;
    },
  },
};
</script>
