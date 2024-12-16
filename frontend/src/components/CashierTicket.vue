<template>
  <div class="cashier-ticket">
    <h3>Билет №{{ ticket.ticket_id }}</h3>
    <p>Номер поезда: {{ ticket.train_number }}</p>
    <p>Дата: {{ ticket.date }}</p>
    <p>Имя покупателя: {{ ticket.buyer_name }}</p>
    <p>Имя пассажира: {{ ticket.passenger_name }}</p>
    <p>Паспорт пассажира: {{ ticket.passenger_passport }}</p>
    <div class="buttons">
      <button @click="handleAction(actionCallback)">{{ actionText }}</button>
      <button v-if="rejectText" @click="handleAction(rejectCallback)" class="reject">{{ rejectText }}</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "CashierTicket",
  props: {
    ticket: {
      type: Object,
      required: true,
    },
    actionText: {
      type: String,
      required: true,
    },
    rejectText: {
      type: String,
    },
    actionCallback: {
      type: Function,
    },
    rejectCallback: {
      type: Function,
      required: true,
    },
  },
  methods: {
    handleAction(callback) {
      callback(this.ticket.ticket_id);
    },
  },
};
</script>

<style scoped>
.cashier-ticket {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  background-color: #fff;
}

.buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

button.reject {
  background-color: #ff4c4c;
}

button:hover {
  opacity: 0.9;
}
</style>