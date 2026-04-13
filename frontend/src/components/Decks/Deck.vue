<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({ deck: Object })
const emit = defineEmits(['delete_deck'])

const deckColors = computed(() => {
  const colorsSet = new Set()
  props.deck.cards.forEach((card) => {
    card.colors?.forEach((color) => colorsSet.add(color))
  })
  return Array.from(colorsSet)
})

const totalCards = computed(() => props.deck.cards.length)

const menuOpen = ref(false)
const toggleMenu = () => (menuOpen.value = !menuOpen.value)

const menuRef = ref()
const buttonRef = ref()

const handleClickOutside = (event) => {
  if (
    menuOpen.value &&
    menuRef.value &&
    !menuRef.value.contains(event.target) &&
    buttonRef.value &&
    !buttonRef.value.contains(event.target)
  ) {
    menuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div
    class="relative max-w-xs bg-gray-900 text-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-shadow duration-300"
  >
    <div class="h-48 w-full bg-gray-800 flex items-center justify-center relative">
      <img
        v-if="props.deck.cards.length > 0 && props.deck.cards[0].image"
        :src="props.deck.cards[0].image"
        alt="Deck Image"
        class="object-contain h-full w-full"
      />
      <span v-else class="text-gray-400">No cards yet</span>

      <button
        ref="buttonRef"
        @click.stop="toggleMenu"
        class="absolute top-2 right-2 p-1 text-white hover:bg-gray-700 rounded"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            d="M10 3a1.5 1.5 0 110 3 1.5 1.5 0 010-3zm0 5a1.5 1.5 0 110 3 1.5 1.5 0 010-3zm0 5a1.5 1.5 0 110 3 1.5 1.5 0 010-3z"
          />
        </svg>
      </button>

      <div
        v-if="menuOpen"
        ref="menuRef"
        class="absolute top-10 right-2 bg-gray-800 border border-gray-700 rounded shadow-lg z-10 w-32"
      >
        <button class="block w-full text-left px-4 py-2 hover:bg-gray-700">Edit</button>
        <button
          class="block w-full text-left px-4 py-2 hover:bg-red-600"
          @click="$emit('delete_deck', deck.id)"
        >
          Delete
        </button>
      </div>
    </div>

    <div class="p-4">
      <h2 class="text-lg font-bold mb-2">{{ props.deck.name }}</h2>

      <div class="flex flex-wrap gap-1 mb-2">
        <span
          v-for="color in deckColors"
          :key="color"
          class="text-sm px-2 py-1 border border-white rounded-full"
        >
          {{ color }}
        </span>
      </div>

      <div class="text-sm text-gray-300">Total Cards: {{ totalCards }}</div>
    </div>
  </div>
</template>

<style scoped></style>
