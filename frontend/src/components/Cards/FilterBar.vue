<script setup>
import { ref } from 'vue'
import CustomSelect from '@/components/Cards/CustomSelect.vue'

const sortOptions = [
  { value: 'name', label: 'Name' },
  { value: 'price', label: 'Price' },
  { value: 'cmc', label: 'CMC' },
  { value: 'rarity', label: 'Rarity' },
  { value: 'release_date', label: 'Release Date' },
]

const orderOptions = [
  { value: 'asc', label: 'Ascending' },
  { value: 'desc', label: 'Descending' },
]

const rarityOptions = [
  { value: '', label: 'All' },
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
        class="mx-6 py-4 mb-6 bg-white/5 border border-white/10 rounded-2xl backdrop-blur gap-8 text-white flex flex-wrap justify-center items-start"
      >
        <div class="flex flex-col gap-2 min-w-[180px]">
          <label class="text-sm text-white/60">Filter By</label>
          <CustomSelect v-model="filters.sort_by" :options="sortOptions" />
        </div>

        <div class="flex flex-col gap-2 min-w-[180px]">
          <label class="text-sm text-white/60">Order</label>
          <CustomSelect v-model="filters.order" :options="orderOptions" />
        </div>

        <div class="flex flex-col gap-2 min-w-[180px]">
          <label class="text-sm text-white/60">Rarity</label>
          <CustomSelect v-model="filters.rarity" :options="rarityOptions" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-sm text-white/60">Min Price ($)</label>
          <input
            v-model="filters.min_price"
            type="number"
            placeholder="0"
            class="bg-white/10 rounded-lg px-3 py-2 text-white w-32"
          />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-sm text-white/60">Max Price ($)</label>
          <input
            v-model="filters.max_price"
            type="number"
            placeholder="1000"
            class="bg-white/10 rounded-lg px-3 py-2 text-white w-32"
          />
        </div>

        <div class="flex flex-col gap-2 min-w-[160px]">
          <label class="text-sm invisible">Actions</label>
          <div class="flex gap-6">
            <button
              @click="applyFilters"
              class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 rounded-lg transition"
            >
              Apply Filters
            </button>
            <button
              @click="resetFilters"
              class="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition"
            >
              Reset Filters
            </button>
          </div>
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