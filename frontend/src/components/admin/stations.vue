<template>
  <MainHeader />
  <div class="admin-stations">
    <h1>Управление станциями</h1>
    <button class="add-station-btn" @click="openAddModal">Добавить станцию</button>

    <table class="station-table">
      <thead>
      <tr>
        <th>ID</th>
        <th>Название</th>
        <th>Город</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="station in stations" :key="station.station_id">
        <td>{{ station.station_id}}</td>
        <td>{{ station.name }}</td>
        <td>{{ station.city }}</td>
        <td>
          <button @click="openEditModal(station)">Редактировать</button>
          <button @click="deleteStation(station.station_id)">Удалить</button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления/редактирования станции -->

    <Modal v-if="showModal" @close="closeModal">
      <template #default>
        <h2>{{ editStation ? "Редактировать станцию" : "Добавить станцию" }}</h2>
        <form @submit.prevent="submitStation">
          <label>
            ID:
            <input v-model="form.station_id" type="number" :disabled="editStation" required />
          </label>
          <label>
            Название:
            <input v-model="form.name" type="text" required />
          </label>
          <label>
            Город:
            <input v-model="form.city" type="text" required />
          </label>
          <label>
            Код доступа:
            <input v-model="form.admin_code" type="password" required />
          </label>
          <button type="submit">{{ editStation ? "Сохранить изменения" : "Добавить" }}</button>
        </form>
      </template>
    </Modal>

  </div>
</template>

<script>
import axios from "axios";
import MainHeader from "@/components/header.vue";
import Modal from "@/components/admin/modalStation.vue"

export default {
  name: "AdminStations",
  components: { MainHeader, Modal },
  data() {
    return {
      stations: [],
      showModal: false,
      editStation: null,
      form: {
        station_id: "",
        name: "",
        city: "",
        admin_code: "", // Добавляем поле для кода доступа
      },
    };
  },
  async created() {
    await this.fetchStations();
    console.log(this.stations)
  },
  methods: {
    async fetchStations() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/stations/all");
        this.stations = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке станций:", error);
      }
    },
    openAddModal() {
      this.showModal = true;
      this.editStation = null;
      this.resetForm();
    },
    openEditModal(station) {
      this.showModal = true;
      this.editStation = station;
      this.form = { ...station, admin_code: "" }; // Сбрасываем admin_code при редактировании
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    resetForm() {
      this.form = { station_id: "", name: "", city: "", admin_code: "" };
    },
    async submitStation() {
      const token = localStorage.getItem("token");
      try {
        console.log(this.form)

        if(this.editStation) {
          await axios.put("http://127.0.0.1:5000/admin/stations/update",  this.form, {
            headers: {Authorization: `Bearer ${token}`},
          });
        }
        else {
          await axios.post("http://127.0.0.1:5000/admin/stations/add",  this.form, {
            headers: {Authorization: `Bearer ${token}`},
          });
        }

        alert(this.editStation ? "Станция обновлена" : "Станция добавлена");
        this.closeModal();
        await this.fetchStations();
      } catch (error) {
        console.error(
            this.editStation
                ? "Ошибка при обновлении станции"
                : "Ошибка при добавлении станции",
            error
        );
      }
    },
    async deleteStation(station_id) {
      const admin_code = prompt("Введите код доступа для удаления станции:");
      if (!admin_code) return;

      const token = localStorage.getItem("token");

      if (!confirm("Вы уверены, что хотите удалить станцию?")) return;
      console.log(station_id, " ", admin_code)
      try {
        await axios.delete("http://127.0.0.1:5000/admin/stations/delete", {
          headers: {Authorization: `Bearer ${token}`},
          data: {station_id, admin_code},
        });
        alert("Станция удалена");
        await this.fetchStations();
      } catch (error) {
        console.error("Ошибка при удалении станции:", error);
      }
    },
  },
};
</script>

<style scoped>
.admin-stations {
  padding: 50px;
}

.station-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.5); /* Полупрозрачный фон */
  opacity: 0.75;
}

.station-table th,
.station-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  background: white;
}

.station-table th {
  background-color: #f4f4f4;
}

button {
  margin-right: 5px;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-station-btn {
  margin-bottom: 20px;
  padding: 15px 30px; /* Увеличиваем размеры кнопки */
  font-size: 16px; /* Увеличиваем размер шрифта */
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
}

.add-station-btn:hover {
  background-color: #45a049;
}

h1 {
  color: white; /* Белый цвет для заголовка */
  text-align: center;
  font-size: 2em; /* Увеличиваем размер шрифта */
  margin-bottom: 30px;
}

.form-modal {
  display: flex;
  flex-direction: column;
  gap: 15px; /* Расстояние между полями */
}

label {
  display: flex;
  flex-direction: column;
  font-size: 16px;
}

input {
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  padding: 10px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.modal-overlay {
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
  border-radius: 10px;
  width: 400px;
}
</style>

