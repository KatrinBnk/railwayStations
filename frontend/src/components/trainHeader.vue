<template>
  <div class="search-header">
    <h1 class="title">
      <span class="red_txt">Купить</span> билет,
      <span class="red_txt">посмотреть</span> расписание
    </h1>
    <div class="search-box">
      <input
          v-model="localDeparture"
          list="departure-options"
          @input="validateStationInput('departure')"
          @change="selectStation('departure')"
          type="text"
          placeholder="Откуда..."
      />
      <datalist id="departure-options">
        <option
            v-for="station in departureOptions"
            :key="station.station_code"
            :value="station.name"
        ></option>
      </datalist>

      <input
          v-model="localDestination"
          list="destination-options"
          @input="validateStationInput('destination')"
          @change="selectStation('destination')"
          type="text"
          placeholder="Куда..."
      />
      <datalist id="destination-options">
        <option
            v-for="station in destinationOptions"
            :key="station.station_code"
            :value="station.name"
        ></option>
      </datalist>

      <input
          v-model="localTravelDate"
          type="date"
          placeholder="Дата поездки..."
          @input="$emit('update:travelDate', localTravelDate)"
      />
      <button :disabled="!isFormValid" @click="emitSearch">Найти</button>
    </div>
  </div>
</template>

<script>
import { searchStationByName } from "@/api/stations.js";

export default {
  name: "SearchHeader",
  props: {
    departure: String,
    destination: String,
    travelDate: String,
  },
  data() {
    return {
      localDeparture: this.departure || "",
      localDestination: this.destination || "",
      localTravelDate: this.travelDate || "",
      departureOptions: [],
      destinationOptions: [],
    };
  },
  computed: {
    isFormValid() {
      return this.localDeparture && this.localDestination && this.localTravelDate;
    },
  },
  watch: {
    departure: {
      immediate: true,
      handler(newValue) {
        this.localDeparture = newValue;
      },
    },
    destination: {
      immediate: true,
      handler(newValue) {
        this.localDestination = newValue;
      },
    },
    travelDate: {
      immediate: true,
      handler(newValue) {
        this.localTravelDate = newValue;
      },
    },
  },
  methods: {
    async validateStationInput(type) {
      const stationName =
          type === "departure" ? this.localDeparture : this.localDestination;

      if (stationName.length < 2) {
        return;
      }

      try {
        const stations = await searchStationByName(stationName);

        if (stations && stations.length > 0) {
          if (type === "departure") {
            this.departureOptions = stations;
          } else {
            this.destinationOptions = stations;
          }
        }
      } catch (error) {
        console.error(`Ошибка при поиске станции (${type}):`, error);
      }
    },
    selectStation(type) {
      const stationName =
          type === "departure" ? this.localDeparture : this.localDestination;

      const matchingStation = (type === "departure"
              ? this.departureOptions
              : this.destinationOptions
      ).find((station) => station.name === stationName);

      if (matchingStation) {
        if (type === "departure") {
          this.$emit("update:departureCode", matchingStation.station_id);
        } else {
          this.$emit("update:destinationCode", matchingStation.station_id);
        }
      } else {
        console.error(`Станция "${stationName}" не найдена.`);
      }
    },
    emitSearch() {
      this.$emit("update:travelDate", this.localTravelDate); // Передача даты
      this.$emit("search");
    },
  },
};
</script>


<style scoped>
.search-header {
  text-align: center;
  margin-top: 50px;
}

.search-box {
  display: flex;
  gap: 15px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 15px;
  margin: 50px;
}
.red_txt{
  color: red;
  background: #D9D9D9;
  padding: 10px;
  opacity: 0.75;
}
.title{
  display:inline;
  color: #D9D9D9;
}

input[type="text"],
input[type="date"] {
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #ccc;
  flex-grow: 1;
  font-size: 1em;
}

button {
  padding: 15px 30px;
  background-color: #ff4c4c;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1em;
}
</style>
