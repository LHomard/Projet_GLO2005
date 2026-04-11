<script setup>
import { ref } from 'vue'
import CustomSelect from '@/components/Cards/CustomSelect.vue'

const sortOptions = [
  { value: 'name', label: 'Nom' },
  { value: 'price', label: 'Prix' },
  { value: 'cmc', label: 'CMC' },
  { value: 'rarity', label: 'Rareté' },
  { value: 'release_date', label: 'Date' },
]

const orderOptions = [
  { value: 'asc', label: 'Croissant' },
  { value: 'desc', label: 'Décroissant' },
]

const rarityOptions = [
  { value: '', label: 'Toutes' },
  { value: 'common', label: 'Common' },
  { value: 'uncommon', label: 'Uncommon' },
  { value: 'rare', label: 'Rare' },
  { value: 'mythic', label: 'Mythic' },
]
const emit = defineEmits(['apply', 'reset'])

const showFilters = ref(false)
defineProps({ visible: Boolean })

const filters = ref({
  sort_by: 'name',
  order: 'asc',
  rarity: '',
  min_price: '',
  max_price: '',
})

const applyFilters = () => {
  emit('apply', { ...filters.value })
  showFilters.value = false
}

const resetFilters = () => {
  filters.value = { sort_by: 'name', order: 'asc', rarity: '', min_price: '', max_price: '' }
  emit('reset')
  showFilters.value = false
}
</script>

<template>
  <div>
    <Transition name="slide-down">
      <div
        v-if="visible"
        class="mx-8 mb-6 p-6 bg-white/5 border border-white/10 rounded-2xl backdrop-blur text-white flex flex-wrap gap-4"
      >
        <div class="flex flex-col gap-1">
          <label class="text-sm text-white/60">Trier par</label>
          <CustomSelect v-model="filters.sort_by" :options="sortOptions" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm text-white/60">Ordre</label>
          <CustomSelect v-model="filters.order" :options="orderOptions" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm text-white/60">Rareté</label>
          <CustomSelect v-model="filters.rarity" :options="rarityOptions" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm text-white/60">Prix min ($)</label>
          <input
            v-model="filters.min_price"
            type="number"
            placeholder="0"
            class="bg-white/10 rounded-lg px-3 py-2 text-white w-28"
          />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm text-white/60">Prix max ($)</label>
          <input
            v-model="filters.max_price"
            type="number"
            placeholder="1000"
            class="bg-white/10 rounded-lg px-3 py-2 text-white w-28"
          />
        </div>

        <div class="flex items-end gap-2">
          <button
            @click="applyFilters"
            class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 rounded-lg transition"
          >
            Appliquer
          </button>
          <button
            @click="resetFilters"
            class="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition"
          >
            Réinitialiser
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.slide-down-enter-from,
.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.slide-down-enter-to,
.slide-down-leave-from {
  max-height: 300px;
  opacity: 1;
}
</style>
