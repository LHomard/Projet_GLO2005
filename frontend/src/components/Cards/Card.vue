<script setup>
const props = defineProps({ card: Object })
defineEmits(['select'])
</script>

<template>
  <div v-if="props.card">
    <img
      :src="props.card.image"
      :alt="props.card.name"
      class="rounded-xl shadow-2xl w-48 cursor-pointer transition-transform duration-300 ease-in-out hover:-translate-y-2 hover:scale-105 hover:shadow-[0_16px_48px_rgba(0,0,0,0.7)]"
      @click="$emit('select', props.card.id_printing)"
    />
  </div>
  <div v-else class="text-white">Loading...</div>
</template>
