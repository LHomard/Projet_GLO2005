<script setup>
import { ref } from 'vue'
import CardFilters from '@/components/Cards/CardFilter.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  filters: {
    type: Boolean,
    default: false,
  },
  confirmButton: {
    type: Boolean,
    default: false,
  },
  confirmLabel: {
    type: String,
    default: 'Add card to my deck',
  },
})

const emit = defineEmits(['close', 'select-card', 'add-card'])

const searchQuery = ref('')
const cardInPlay = ref([])
const selectedCard = ref(null)
const showFilters = ref(false)

const appliedFilters = ref({
  sort_by: 'name',
  order: 'asc',
  rarity: '',
  min_price: '',
  max_price: '',
})

async function getData() {
  if (!searchQuery.value.trim()) {
    cardInPlay.value = []
    selectedCard.value = null
    return
  }

  const params = new URLSearchParams({
    search: searchQuery.value,
    sort_by: appliedFilters.value.sort_by,
    order: appliedFilters.value.order,
    rarity: appliedFilters.value.rarity,
  })

  if (appliedFilters.value.min_price !== '') {
    params.append('min_price', appliedFilters.value.min_price)
  }

  if (appliedFilters.value.max_price !== '') {
    params.append('max_price', appliedFilters.value.max_price)
  }

  const url = `http://localhost:5000/api/cards?${params.toString()}`

  try {
    const response = await fetch(url)

    if (!response.ok) {
      if (response.status === 404) {
        cardInPlay.value = []
        selectedCard.value = null
        return
      }
      throw new Error(`Response Status: ${response.status}`)
    }

    const result = await response.json()
    cardInPlay.value = result.cards || []
    selectedCard.value = null
  } catch (e) {
    console.error(e.message)
    cardInPlay.value = []
    selectedCard.value = null
  }
}

const onCardClick = (card) => {
  if (props.confirmButton) {
    selectedCard.value = card
    return
  }

  emit('select-card', card)
}

const confirmAddCard = () => {
  if (!selectedCard.value) return
  emit('add-card', selectedCard.value)
}

const applyFilters = async (filters) => {
  appliedFilters.value = { ...filters }
  await getData()
}

const resetFilters = async () => {
  appliedFilters.value = {
    sort_by: 'name',
    order: 'asc',
    rarity: '',
    min_price: '',
    max_price: '',
  }
  await getData()
}
</script>

<template>
  <div
    class="fixed inset-0 bg-black/80 backdrop-blur-sm flex justify-center items-center z-50 p-4"
    @click.self="$emit('close')"
  >
    <div class="bg-[#303F54] border border-white/10 rounded-xl shadow-2xl w-full max-w-2xl flex flex-col max-h-[90vh]">
      <div class="p-6 pb-0 flex justify-between items-center">
        <label class="text-white font-bold text-xl">{{ title }}</label>
        <button @click="$emit('close')" class="text-white/50 hover:text-white">✕</button>
      </div>

      <div class="p-6 pb-2 flex gap-3 items-center">
        <input
          v-model="searchQuery"
          @keyup="getData"
          type="text"
          class="bg-slate-900/50 border border-white/10 text-white text-sm rounded-lg w-full px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type a card name..."
        />

        <button
          v-if="filters"
          type="button"
          @click="showFilters = !showFilters"
          class="px-4 py-3 bg-white/10 hover:bg-white/20 rounded-lg text-white transition whitespace-nowrap"
        >
          Filters
        </button>
      </div>

      <CardFilters
        v-if="filters"
        :visible="showFilters"
        @apply="applyFilters"
        @reset="resetFilters"
      />

      <div class="p-6 pt-2 overflow-y-auto custom-scrollbar">
        <div v-if="cardInPlay.length > 0" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div
            v-for="card in cardInPlay"
            :key="card.id"
            @click="onCardClick(card)"
            class="group cursor-pointer"
          >
            <img
              :src="card.image"
              :alt="card.name"
              class="w-32 h-auto rounded-lg shadow-md transition-transform"
              :class="
                selectedCard?.id === card.id
                  ? 'ring-4 ring-blue-500 scale-105'
                  : 'hover:scale-105'
              "
            />
          </div>
        </div>

        <div v-else-if="searchQuery" class="text-center py-10 text-white/30">
          No cards found...
        </div>
      </div>

      <div
        v-if="confirmButton"
        class="p-6 pt-3 flex justify-end gap-3 border-t border-white/10"
      >
        <button
          type="button"
          :disabled="!selectedCard"
          @click="confirmAddCard"
          class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 rounded-lg transition text-white disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ confirmLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
</style>