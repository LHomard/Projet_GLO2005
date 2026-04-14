<script setup>
import { ref, onMounted } from 'vue'
import Card from '@/components/Cards/Card.vue'
import CardSearchBar from '@/components/Cards/CardSearchBar.vue'
import InfoCardModal from '@/components/Cards/InfoCardModal.vue'
import FilterBar from '@/components/Cards/FilterBar.vue'

const cards = ref([])
const page = ref(1)
const hasMore = ref(true)
const loading = ref(false)
const selected = ref({ id: null })
const activeFilters = ref({})
const showFilters = ref(false)
const searchQuery = ref('')

const fetchCards = async (reset = false) => {
  if (reset) {
    cards.value = []
    page.value = 1
    hasMore.value = true
  }

  loading.value = true
  const params = new URLSearchParams({
    page: page.value,
    search: searchQuery.value,
    ...activeFilters.value,
  })
  for (const [key, val] of params.entries()) {
    if (!val) params.delete(key)
  }

  const res = await fetch(`http://localhost:5000/api/cards?${params}`)
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

const onApplyFilters = (filters) => {
  activeFilters.value = filters
  fetchCards(true)
}

const onResetFilters = () => {
  activeFilters.value = {}
  fetchCards(true)
}

const onResetFilterSearch = () => {
  activeFilters.value = {}
  searchQuery.value = ''
  fetchCards(true)
}

const onSearch = (value) => {
  searchQuery.value = value
  fetchCards(true)
}
</script>

<template>
  <div>
    <div class="relative flex justify-center items-center py-6 gap-4">
      <CardSearchBar v-model="searchQuery" @search="onSearch" />
      <button
        @click="showFilters = !showFilters"
        class="px-4 py-2 bg-white/10 text-white rounded-full hover:bg-white/20 transition"
      >
        Filters
      </button>
    </div>
    <FilterBar :visible="showFilters" @apply="onApplyFilters" @reset="onResetFilters" />

    <template v-if="cards.length">
      <div class="flex justify-around gap-4 flex-wrap mx-8">
        <div v-for="card in cards" :key="card.id">
          <Card :card="card" @select="selected.id = $event" />
        </div>
        <InfoCardModal :cardId="selected.id" @close="selected.id = null" />
      </div>
    </template>

    <template v-else-if="loading">
      <div class="grid grid-cols-7 gap-4 mx-8">
        <div
          v-for="n in 21"
          :key="n"
          class="w-full h-65 rounded-xl bg-white/10 animate-pulse"
        ></div>
      </div>
    </template>

    <template v-else>
      <div class="w-full flex flex-col items-center justify-center py-20 text-white/70">
        <div class="text-2xl mb-4">No cards found</div>

        <div class="text-sm opacity-70 mb-6">Try another search or adjust your filters</div>

        <button
          @click="onResetFilterSearch"
          class="px-4 py-2 bg-white/10 rounded-full hover:bg-white/20 transition"
        >
          Reset filters
        </button>
      </div>
    </template>

    <div class="flex justify-center py-8">
      <button
        v-if="hasMore"
        @click="loadMore"
        :disabled="loading"
        class="px-6 py-3 bg-white/10 text-white rounded-full hover:bg-white/20 transition disabled:opacity-50"
      >
        {{ loading ? 'Loading...' : 'Load More' }}
      </button>
    </div>
  </div>
</template>