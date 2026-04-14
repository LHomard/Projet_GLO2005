<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { manaIconMap } from '@/utils/mtgIcons'

const router = useRouter()
const props = defineProps({ deck: Object })
const emit = defineEmits(['delete_deck'])

const menuOpen = ref(false)
const toggleMenu = () => (menuOpen.value = !menuOpen.value)

const menuRef = ref()
const buttonRef = ref()

const formatLabel = (value) => {
  if (!value) return ''
  return value.charAt(0).toUpperCase() + value.slice(1)
}

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

const goToEdit = () => {
  menuOpen.value = false
  router.push({ name: 'DeckCreate', params: { id: props.deck.id } })
}

const deleteDeck = () => {
  menuOpen.value = false
  emit('delete_deck', props.deck.id)
}

const formatCreatedAt = (dateString) => {
  if (!dateString) return ''

  const date = new Date(dateString)

  return date.toLocaleDateString('en-CA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
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
    class="relative self-start max-w-xs bg-gray-900 text-white rounded-xl shadow-lg overflow-hidden border border-white/20 hover:shadow-2xl transition-shadow duration-300"
  >
    <div class="py-2 h-48 w-full bg-gray-800 flex items-center justify-center relative">
      <img
        v-if="props.deck.image_url"
        :src="props.deck.image_url"
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
        <button
          class="block w-full text-left px-4 py-2 hover:bg-gray-700"
          @click="goToEdit"
        >
          Edit
        </button>

        <button
          class="block w-full text-left px-4 py-2 hover:bg-red-600"
          @click="deleteDeck"
        >
          Delete
        </button>
      </div>
    </div>

    <div class="flex flex-col gap-1 px-4 py-2">
      <h2 class="text-lg font-bold mb-2">{{ props.deck.name }}</h2>

      <div class="flex items-center gap-1 mb-2">
        <img
          v-for="color in props.deck.colors"
          :key="color"
          :src="manaIconMap[color]"
          :alt="color"
          class="w-5 h-5 object-contain"
        />
      </div>

      <div class="mb-2">
        <span class="text-xs px-2 py-1 rounded-md bg-white/10 border border-white/10 text-white/80">
          {{ formatLabel(props.deck.format) }}
        </span>
      </div>

      <div class="text-sm text-gray-300">
        Total Cards: {{ props.deck.card_count }}
      </div>

      <div v-if="props.deck.created_at" class="mt-1 text-xs text-gray-400">
        Created: {{ formatCreatedAt(props.deck.created_at) }}
      </div>
    </div>
  </div>
</template>

<style scoped></style>