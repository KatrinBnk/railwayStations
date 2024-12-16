<template>
  <div class="ticket-list">
    <h1>Мои билеты</h1>

    <!-- Вы пассажир -->
    <div v-if="Object.keys(passengerTickets).some((key) => passengerTickets[key].length)" class="category">
      <h2>Вы пассажир</h2>
      <div v-if="passengerTickets['выкуплен'].length" class="sub-category">
        <h3>Выкупленные</h3>
        <div class="ticket-container">
          <TicketCard
              v-for="ticket in passengerTickets['выкуплен']"
              :key="ticket.ticket_id"
              :ticket="ticket"
              @ticket-updated="fetchTickets"
          />
        </div>
      </div>
      <div v-if="passengerTickets['забронирован'].length" class="sub-category">
        <h3>Забронированные</h3>
        <div class="ticket-container">
          <TicketCard
              v-for="ticket in passengerTickets['забронирован']"
              :key="ticket.ticket_id"
              :ticket="ticket"
              @ticket-updated="fetchTickets"
          />
        </div>
      </div>
      <div v-if="passengerTickets['запрос на возврат'].length" class="sub-category">
        <h3>Запрос на возврат</h3>
        <div class="ticket-container">
          <TicketCard
              v-for="ticket in passengerTickets['запрос на возврат']"
              :key="ticket.ticket_id"
              :ticket="ticket"
              @ticket-updated="fetchTickets"
          />
        </div>
      </div>
    </div>

    <!-- Вы покупатель -->
    <div v-if="Object.keys(buyerTickets).some((key) => buyerTickets[key].length)" class="category">
      <h2>Вы покупатель</h2>
      <div v-if="buyerTickets['выкуплен'].length" class="sub-category">
        <h3>Выкупленные</h3>
        <div class="ticket-container">
          <TicketCard
              v-for="ticket in buyerTickets['выкуплен']"
              :key="ticket.ticket_id"
              :ticket="ticket"
              @ticket-updated="fetchTickets"
          />
        </div>
      </div>
      <div v-if="buyerTickets['забронирован'].length" class="sub-category">
        <h3>Забронированные</h3>
        <div class="ticket-container">
          <TicketCard
              v-for="ticket in buyerTickets['забронирован']"
              :key="ticket.ticket_id"
              :ticket="ticket"
              @ticket-updated="fetchTickets"
          />
        </div>
      </div>
      <div v-if="buyerTickets['запрос на возврат'].length" class="sub-category">
        <h3>Запрос на возврат</h3>
        <div class="ticket-container">
          <TicketCard
              v-for="ticket in buyerTickets['запрос на возврат']"
              :key="ticket.ticket_id"
              :ticket="ticket"
              @ticket-updated="fetchTickets"
          />
        </div>
      </div>
    </div>

    <p v-if="!Object.keys(passengerTickets).some((key) => passengerTickets[key].length) &&
             !Object.keys(buyerTickets).some((key) => buyerTickets[key].length)">
      Билеты не найдены.
    </p>
  </div>
</template>

<script>
import axios from "axios";
import TicketCard from "@/components/ticket.vue";

export default {
  name: "TicketList",
  components: {
    TicketCard,
  },
  data() {
    return {
      tickets: [],
      passengerTickets: {},
      buyerTickets: {},
    };
  },
  async created() {
    await this.fetchTickets();
  },
  methods: {
    async fetchTickets() {
      try {
        const token = localStorage.getItem("token"); // Получение токена авторизации
        const response = await axios.get("http://127.0.0.1:5000/tickets", {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.tickets = response.data;

        // Разделяем билеты по ролям и статусам
        this.passengerTickets = this.categorizeTickets("passenger");
        this.buyerTickets = this.categorizeTickets("buyer");
      } catch (error) {
        console.error("Ошибка при загрузке билетов:", error);
        alert("Не удалось загрузить билеты.");
      }
    },
    categorizeTickets(role) {
      const categories = { выкуплен: [], забронирован: [], "запрос на возврат": [] };

      this.tickets
          .filter((ticket) => ticket.role === role || ticket.role === "buyer and passenger")
          .forEach((ticket) => {
            if (categories[ticket.status]) {
              categories[ticket.status].push(ticket);
            }
          });

      return categories;
    },
  },
};
</script>
<style scoped>
.ticket-list {
  padding: 20px 50px 50px;
}

.category {
  margin-bottom: 30px;
}

.sub-category {
  margin-bottom: 20px;
}

.ticket-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.ticket-container > * {
  flex: 0 1 calc(33.333% - 20px); /* Три элемента в строке с отступами */
  box-sizing: border-box; /* Учитываем padding и border */
}

h1 {
  color: #D9D9D9;
  text-align: start;
  margin-bottom: 30px;
}

h2 {
  color: #D9D9D9;
  margin-bottom: 20px;
}

h3 {
  color: #D9D9D9;
  margin-bottom: 10px;
}
</style>