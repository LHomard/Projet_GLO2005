<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import HomeCard from "@/components/Home/HomeCard.vue"

const sets = ref([])
const carouselRef = ref(null)
let animationFrame = null

const startScrolling = () => {
  if (!carouselRef.value) return


  carouselRef.value.scrollLeft += 1

  if (carouselRef.value.scrollLeft >= carouselRef.value.scrollWidth / 2) {
    carouselRef.value.scrollLeft = 0
  }

  animationFrame = requestAnimationFrame(startScrolling)
}

onMounted(async () => {
  const res = await fetch('http://localhost:5000/api/sets')
  sets.value = await res.json()

  startScrolling()
})

onUnmounted(() => {
  cancelAnimationFrame(animationFrame)
})


</script>

<template>
  <div
    class="carousel"
    ref="carouselRef"
    @mouseenter="pause"
    @mouseleave="resume"
    @touchstart="pause"
    @touchend="resume"
  >
    <div class="carousel-track">
      <div class="grid py-20">
        <HomeCard v-for="set in sets" :key="set.id" :set="set" />
      </div>
    </div>
  </div>
</template>

<style scoped>
  .carousel {
    width: 100%;
    overflow-x: auto;
    white-space: nowrap;
    display: flex;
    scroll-behavior: auto;
  }

  .carousel-track {
    display: flex;
    width: max-content;
    gap: 2rem;
  }

  .grid {
    display: flex;
    gap: 2rem;
    flex-shrink: 0;
  }

  .carousel::-webkit-scrollbar { height: 15px; }
  .carousel::-webkit-scrollbar-track { background-color: #C2D2E4; }
  .carousel::-webkit-scrollbar-thumb { background-color: #0A4C95; }
</style>
