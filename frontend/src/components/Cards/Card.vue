<script setup>
const props = defineProps({ card: Object })
</script>

<template>
  <div class="flex justify-center items-center h-85">
    <div v-if="card" class="flex justify-center items-center min-h-screen">
      <img :src="props.card.image" :alt="props.card.name" class="rounded-xl shadow-2xl w-48" />
    </div>
    <div v-else class="text-white">Loading...</div>
  </div>
</template>

<style scoped>

</style>
