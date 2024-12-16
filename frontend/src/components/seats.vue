<template>
  <div class="seats-page">
    <!-- Список типов вагонов -->
    <div class="wagon-types">
      <div
          v-for="(wagons, type) in groupedWagons"
          :key="type"
          class="wagon-type-card"
          :class="{ active: selectedType === type }"
          @click="selectType(type)"
      >
        <h2>{{ type }}</h2>
        <p>Мест: {{ wagons.reduce((total, wagon) => total + wagon.available_seats.length, 0) }}</p>
        <p>Цена от: {{ Math.min(...wagons.map(wagon => wagon.price)) }} руб.</p>
      </div>
    </div>
    <!-- Список вагонов -->
    <div v-if="selectedType" class="wagon-list">
      <h2>Вагоны {{ selectedType }}</h2>
      <div
          v-for="wagon in groupedWagons[selectedType]"
          :key="wagon.wagon_number"
          class="wagon-card"
      >
        <h3 @click="toggleWagon(wagon.wagon_number)">
          Вагон № {{ wagon.wagon_number }}
        </h3>
        <div v-if="expandedWagons.includes(wagon.wagon_number)" class="seat-list">
          <div
              v-for="seat in wagon.available_seats"
              :key="seat.number_seat"
              class="seat-card"
          >
            <p>Место: №{{ seat.number_seat }}</p>
            <p>Тип: {{ seat.type_seat }}</p>
            <button v-if="isAuth" @click="openModal(seat, wagon)">Купить</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Введите данные для билета</h3>
        <form @submit.prevent="submitBooking">
          <label for="firstName">Имя:</label>
          <input id="firstName" v-model="bookingData.firstName" required />

          <label for="lastName">Фамилия:</label>
          <input id="lastName" v-model="bookingData.lastName" required />

          <label for="middleName">Отчество:</label>
          <input id="middleName" v-model="bookingData.middleName" />

          <label for="passport">Паспорт:</label>
          <input id="passport" v-model="bookingData.passport" required />

          <label for="isPaid">Оплатить сразу:</label>
          <input id="isPaid" type="checkbox" v-model="bookingData.isPaid" />

          <div v-if="isCashier">
            <label for="staffCode">Код доступа:</label>
            <input id="staffCode" v-model="bookingData.staffCode" required />
          </div>

          <button type="submit">Подтвердить</button>
          <button type="button" @click="closeModal">Отмена</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SeatsPage",
  props: {
    train: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      wagons: [],
      expandedWagons: [],
      selectedType: null,
      showModal: false,
      selectedSeat: null,
      selectedWagon: null,
      bookingData: {
        firstName: "",
        lastName: "",
        middleName: "",
        passport: "",
        isPaid: false,
        staffCode: "", // поле для кода доступа кассира
      },
      isAuth: false,
    };
  },
  computed: {
    groupedWagons() {
      return this.wagons.reduce((groups, wagon) => {
        if (!groups[wagon.type_wagon]) {
          groups[wagon.type_wagon] = [];
        }
        groups[wagon.type_wagon].push(wagon);
        return groups;
      }, {});
    },
    isCashier() {
      return localStorage.getItem('role') === 'staff'; // Проверка, является ли пользователь кассиром
    }
  },
  created() {
    this.fetchSeats();
    this.authUser();
  },
  methods: {
    authUser(){
      const user = localStorage.getItem("token");
      if (!user) {
        console.log("User not auth")
        this.isAuth = false
      } else{
        this.isAuth = true;
      }
    },
    async fetchSeats() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/seats", {
          params: {
            train_id: this.train.train_id,
            departure_station_id: this.train.departure_station_id,
            arrival_station_id: this.train.arrival_station_id,
            date: this.train.departure_date,
          },
        });

        this.wagons = response.data.available_seats.reduce((acc, seat) => {
          const wagonIndex = acc.findIndex(w => w.wagon_number === seat.wagon_number);

          if (wagonIndex !== -1) {
            acc[wagonIndex].available_seats.push(seat);
          } else {
            acc.push({
              wagon_number: seat.wagon_number,
              type_wagon: seat.type_wagon,
              price: response.data.price,
              available_seats: [seat],
            });
          }
          return acc;
        }, []);
      } catch (error) {
        console.error("Ошибка при загрузке мест:", error);
      }
    },
    toggleWagon(wagonNumber) {
      if (this.expandedWagons.includes(wagonNumber)) {
        this.expandedWagons = this.expandedWagons.filter(num => num !== wagonNumber);
      } else {
        this.expandedWagons.push(wagonNumber);
      }
    },
    selectType(type) {
      this.selectedType = type;
    },
    openModal(seat, wagon) {
      this.selectedSeat = seat;
      this.selectedWagon = wagon;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedSeat = null;
      this.selectedWagon = null;
      this.resetBookingData();
    },
    resetBookingData() {
      this.bookingData = {
        firstName: "",
        lastName: "",
        middleName: "",
        passport: "",
        isPaid: false,
        staffCode: "", // сбросить код доступа
      };
    },
    async submitBooking() {
      try {
        const payload = {
          train_id: this.train.train_id,
          number_wagon: this.selectedWagon.wagon_number,
          seat_number: this.selectedSeat.number_seat,
          departure_station_id: this.train.departure_station_id,
          arrival_station_id: this.train.arrival_station_id,
          date: this.train.departure_date,
          is_paid: this.bookingData.isPaid,
          passenger_first_name: this.bookingData.firstName,
          passenger_last_name: this.bookingData.lastName,
          passenger_middle_name: this.bookingData.middleName,
          passenger_passport: this.bookingData.passport,
          code_sell: this.bookingData.staffCode, // для кассиров
        };

        const token = localStorage.getItem("token");

        let url = "http://127.0.0.1:5000/booking"; // По умолчанию для обычных пользователей
        if (this.isCashier) {
          url = "http://127.0.0.1:5000/sell_ticket"; // Для кассиров
        }

        const response = await axios.post(url, payload, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        alert(response.data.message);
        this.closeModal();
        this.fetchSeats(); // Обновить данные о доступных местах
      } catch (error) {
        console.error("Ошибка при бронировании:", error);
        alert("Не удалось забронировать билет.");
      }
    },
  },
};
</script>

<style scoped>

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px; /* Можно настроить ширину */
}

form {
  display: flex;
  flex-direction: column; /* Режим столбца */
  gap: 15px; /* Отступ между элементами */
}

label {
  font-weight: bold;
  margin-bottom: 5px; /* Отступ снизу у меток */
}

input[type="text"], input[type="password"], input[type="checkbox"] {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%; /* Поля ввода растягиваются на всю ширину контейнера */
}

button {
  padding: 10px;
  margin-top: 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%; /* Кнопки растягиваются на всю ширину */
}

button:hover {
  background-color: #45a049;
}

input[type="checkbox"] {
  width: auto; /* Для чекбокса задаем авто-ширину */
}


.seats-page {
  padding: 20px;
  text-align: center;
}

.wagon-types {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.wagon-type-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 15px;
  width: 250px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.wagon-type-card.active {
  background-color: #4caf50;
  color: white;
  border-color: #4caf50;
}

.wagon-type-card:hover {
  background-color: #f1f1f1;
}

.wagon-list {
  margin-top: 20px;
}

.wagon-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.seat-list {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.seat-card {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  text-align: center;
  background-color: #f9f9f9;
  width: 120px;
}

button {
  padding: 10px;
  margin-top: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}
</style>
