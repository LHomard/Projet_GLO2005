<script setup>
const emit = defineEmits(['open']);
</script>

<template>
  <button class="card-placeholder" @click="$emit('open')">
    Add card in play
  </button>
</template>

<style scoped>
.card-placeholder {
    width: 63mm;
    height: 88mm;
    border: 2px dotted #555;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'rastera', monospace;
    font-size: 14px;
    text-align: center;
    background-color: transparent;
    margin: 10px;
    color: #7f7f7f;
  }

.card-placeholder:hover {
  border: 2px solid #7f7f7f;
}
</style>
