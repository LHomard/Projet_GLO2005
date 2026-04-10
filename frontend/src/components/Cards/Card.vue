<script setup>
const props = defineProps({ card: Object })
defineEmits(['select'])
</script>

<template>
  <div v-if="props.card">
    <img
      :src="props.card.image"
      :alt="props.card.name"
      class="rounded-xl shadow-2xl w-48 cursor-pointer"
      @click="$emit('select', props.card.id_oracle)"
    />
  </div>
  <div v-else class="text-white">Loading...</div>
</template>
