<template>
  <div class="modal">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">X</button>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "Modal",
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  display: flex;
  flex-direction: column; /* Режим столбца */
  gap: 15px; /* Отступы между элементами */
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

button {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}
</style>
