<script setup>
  import { ref, onMounted } from 'vue'
  import Card from "@/components/Cards/Card.vue"
  import CardSearchBar from "@/components/Cards/CardSearchBar.vue"

  const cards = ref([])
  const page = ref(1)
  const hasMore = ref(true)
  const loading = ref(false)

  const fetchCards = async () => {
    loading.value = true
    const res = await fetch(`http://localhost:5000/api/cards?page=${page.value}`)
    const data = await res.json()
    cards.value = [...cards.value, ...data.cards]
    hasMore.value = data.has_more
    loading.value = false
  }

  onMounted(() => fetchCards())

  const loadMore = () => {
    page.value++
    fetchCards()
  }
</script>

<template>
  <div>
    <div class="flex justify-center py-6">
      <CardSearchBar />
    </div>
    <div class="flex justify-around gap-4 flex-wrap mx-8">
      <div v-for="card in cards" :key="card.id">
        <Card :card="card" />
      </div>
    </div>
    <div class="flex justify-center py-8">
      <button
        v-if="hasMore"
        @click="loadMore"
        :disabled="loading"
        class="px-6 py-3 bg-white/10 text-white rounded-full hover:bg-white/20 transition duration-200 disabled:opacity-50"
      >
        {{ loading ? 'Loading...' : 'Load More' }}
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>
