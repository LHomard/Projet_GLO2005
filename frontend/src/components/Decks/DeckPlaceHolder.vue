<script setup>
const emit = defineEmits(['create']);
</script>

<template>
  <button class="deck-placeholder" @click="$emit('create')">
    <span class="plus-icon">+</span>
    <span class="text">Create a new deck</span>
  </button>
</template>

<style scoped>
.deck-placeholder {
  width: 20rem;
  height: 330px;
  border: 2px dotted #555;
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'rastera', monospace;
  font-size: 14px;
  text-align: center;
  background-color: #111827;
  color: #9ca3af;
  transition: box-shadow 0.3s ease;
}

.plus-icon {
  font-size: 28px;
  margin-bottom: 6px;
  line-height: 1;
}

.deck-placeholder:hover {
  border: 2px solid #7f7f7f;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

.plus-icon {
  font-size: 32px;
  font-weight: bold;
  transition: transform 0.2s ease;
}

.text {
  transition: transform 0.2s ease;
}

.deck-placeholder:hover .text {
  transform: scale(1.2);
}

.deck-placeholder:hover .plus-icon {
  transform: scale(1.2);
}
</style>