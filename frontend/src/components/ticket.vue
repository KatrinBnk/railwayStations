<template>
  <div class="ticket-card">
    <div class="ticket-info">
      <h2>Номер поезда: {{ ticket.train_number }}</h2>
      <p>Дата поездки: {{ ticket.date }}</p>
      <p>Станция отправления: {{ ticket.departure_station_name }} ({{ ticket.departure_time }})</p>
      <p>Станция прибытия: {{ ticket.arrival_station_name }} ({{ ticket.arrival_time }})</p>
      <p>Стоимость билета: {{ ticket.price }} руб.</p>
      <p>Статус билета: {{ ticket.status }}</p>
    </div>
    <button
        v-if="(ticket.role === 'buyer' || ticket.role === 'buyer and passenger') &&
             (ticket.status === 'забронирован' || ticket.status === 'выкуплен')"
        @click="submitReturnRequest"
    >
      Заявка на возврат
    </button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TicketCard",
  props: {
    ticket: {
      type: Object,
      required: true,
    },
  },
  methods: {
    async submitReturnRequest() {
      try {
        const token = localStorage.getItem("token"); // Получение токена авторизации

        if (!token) {
          alert("Вы не авторизованы.");
          return;
        }

        const response = await axios.post(
            "http://127.0.0.1:5000/return",
            { ticket_id: this.ticket.ticket_id },
            { headers: { Authorization: `Bearer ${token}` } }
        );

        alert(response.data.message);
        this.$emit("ticket-updated"); // Оповещение родителя об изменении статуса
      } catch (error) {
        console.error("Ошибка при отправке заявки на возврат:", error);
        const errorMessage =
            error.response?.data?.error || "Не удалось отправить заявку на возврат.";
        alert(errorMessage);
      }
    },
  },
};
</script>

<style scoped>
.ticket-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  margin: 15px 0;
  background-color: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  opacity: 0.75;
}

.ticket-info {
  margin-bottom: 15px;
}

button {
  padding: 10px 20px;
  background-color: #ff4c4c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e04343;
}
</style>
