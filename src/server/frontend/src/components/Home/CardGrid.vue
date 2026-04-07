<script setup>
  import { ref, onMounted } from 'vue'
  import HomeCard from "@/components/Home/HomeCard.vue"

  const sets = ref([])

  onMounted(async () => {
    const res = await fetch('http://localhost:5000/api/sets')
    sets.value = await res.json()
  })
</script>

<template>
  <div class="carousel">
    <div class="grid py-20">
      <HomeCard v-for="set in sets" :key="set.id" :set="set" />
    </div>
    <div aria-hidden class="grid py-20">
      <HomeCard v-for="set in sets" :key="set.id" :set="set" />
    </div>
  </div>
</template>

<style scoped>
  .grid {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    animation: spin 150s infinite linear;
  }

  .carousel {
    display: flex;
    overflow-x: auto;
    gap: 13rem;
    padding-right: 1rem;
  }

  .carousel::-webkit-scrollbar {
    display: none;
  }

  @keyframes spin {
    from {translate: 0;}
    to { translate: -100%;}
  }
</style>
