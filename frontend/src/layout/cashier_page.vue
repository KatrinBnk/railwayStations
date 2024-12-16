<template>
  <MainHeader />
  <div class="cashier-page">
    <header class="header-cashier-page">
      <h1>Страница кассира</h1>
      <div class="buttons">
        <button :class="{ active: mode === 'returns' }" @click="setMode('returns')">Запросы на возврат</button>
        <button :class="{ active: mode === 'bookings' }" @click="setMode('bookings')">Подтверждение бронирования</button>
      </div>
    </header>

    <div v-if="mode === 'returns'" class="returns">
      <h2>Запросы на возврат</h2>
      <input v-model="searchQuery" type="text" placeholder="Поиск по паспорту" @input="filterTickets" />
      <div class="tickets">
        <CashierTicket
            v-for="ticket in filteredTickets"
            :key="ticket.ticket_id"
            :ticket="ticket"
            actionText="Одобрить возврат"
            :actionCallback="approveReturn"
            :rejectCallback="rejectReturn"
        />
      </div>
    </div>

    <div v-if="mode === 'bookings'" class="bookings">
      <h2>Подтверждение бронирования</h2>
      <input v-model="searchQuery" type="text" placeholder="Поиск по паспорту" @input="filterTickets" />
      <div class="tickets">
        <CashierTicket
            v-for="ticket in filteredTickets"
            :key="ticket.ticket_id"
            :ticket="ticket"
            actionText="Подтвердить бронирование"
            rejectText="Отказать в бронировании"
            :actionCallback="confirmBooking"
            :rejectCallback="rejectBooking"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CashierTicket from "@/components/CashierTicket.vue";
import MainHeader from "@/components/header.vue";

export default {
  name: "CashierPage",
  components: {
    CashierTicket,
    MainHeader,
  },
  data() {
    return {
      mode: "returns",
      tickets: [],
      filteredTickets: [],
      searchQuery: "",
    };
  },
  methods: {
    async setMode(mode) {
      this.mode = mode;
      this.searchQuery = "";
      await this.fetchTickets();
    },
    async fetchTickets() {
      const endpoint =
          this.mode === "returns"
              ? "http://127.0.0.1:5000/return_requests"
              : "http://127.0.0.1:5000/booking_requests";

      const token = localStorage.getItem("token");

      try {
        const response = await axios.get(endpoint, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.tickets = response.data;
        this.filteredTickets = this.tickets;
      } catch (error) {
        console.error("Ошибка при загрузке билетов:", error);
        alert("Не удалось загрузить билеты.");
      }
    },
    filterTickets() {
      const query = this.searchQuery.toLowerCase();
      this.filteredTickets = this.tickets.filter((ticket) =>
          ticket.buyer_passport.toLowerCase().includes(query)
      );
    },
    async approveReturn(ticketId) {
      await this.handleAction(ticketId, "confirm_return", "Возврат подтвержден!");
    },
    async confirmBooking(ticketId) {
      await this.handleAction(ticketId, "confirm_booking", "Бронирование подтверждено!");
    },
    async rejectReturn(ticketId) {
      await this.handleAction(ticketId, "confirm_return", "Возврат отклонен!", false);
    },
    async rejectBooking(ticketId) {
      await this.handleAction(ticketId, "confirm_booking", "Бронирование отклонено!", false);
    },
    async handleAction(ticketId, endpoint, successMessage, confirmed = true) {
      const token = localStorage.getItem("token");

      try {
        await axios.post(
            `http://127.0.0.1:5000/${endpoint}`,
            { ticket_id: ticketId, confirmed }, // Передаем поле confirmed
            { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(successMessage);
        await this.fetchTickets();
      } catch (error) {
        console.error(`Ошибка при выполнении действия (${endpoint}):`, error);
        alert("Не удалось выполнить действие.");
      }
    }
  },
  async created() {
    await this.fetchTickets();
  },
};
</script>

<style scoped>
.cashier-page {
  padding: 20px 50px;
}

.header-cashier-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  color: #D9D9D9;
  font-size: 20px;
}

.buttons {
  display: flex;
  gap: 10px;
}
h2{
  color: #D9D9D9;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

button.active {
  background-color: #4caf50;
  color: #D9D9D9;
}

.tickets {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

input[type="text"] {
  margin-bottom: 20px;
  padding: 10px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
