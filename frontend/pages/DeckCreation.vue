<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import CardPlaceHolder from '@/components/Chat/CardPlaceHolder.vue'
import CardInPlayModal from '@/components/Chat/CardInPlayModal.vue'

const router = useRouter()
const route = useRoute()

const deckId = route.params.id

const showCardModal = ref(false)
const cardsInDeck = ref([])
const pendingCardsToAdd = ref([])

const isLoading = ref(false)
const isSaving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const openCardModal = () => {
  showCardModal.value = true
}

const closeCardModal = () => {
  showCardModal.value = false
}

const fetchDeckCards = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(`http://localhost:5000/api/decks/${deckId}/cards`, {
      credentials: 'include',
    })

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      errorMessage.value = data.error || 'Failed to load deck cards.'
      return
    }

    cardsInDeck.value = data.map((card) => ({
        ...card,
        persisted: true,
    }))
  } catch (error) {
    console.error('Error fetching deck cards:', error)
    errorMessage.value = 'Server unavailable.'
  } finally {
    isLoading.value = false
  }
}

const addCardToDeck = (card) => {
  const normalizedCard = {
    ...card,
    image_url: card.image_url || card.image,
    persisted: false,
  }

  cardsInDeck.value.push(normalizedCard)
  pendingCardsToAdd.value.push(normalizedCard)
  showCardModal.value = false
}

const goBackToDecks = () => {
  router.push({ name: 'DeckBuilding' })
}

const saveAndGoBackToDecks = async () => {
  if (pendingCardsToAdd.value.length === 0) {
    goBackToDecks()
    return
  }

  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    for (const card of pendingCardsToAdd.value) {
      const response = await fetch(`http://localhost:5000/api/decks/${deckId}/cards`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id_printing: card.id_printing ?? card.id,
          quantity: 1,
        }),
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        errorMessage.value = data.error || `Failed to save card ${card.name}.`
        return
      }
    }

    pendingCardsToAdd.value = []
    successMessage.value = 'Deck saved successfully.'

    await router.push({ name: 'DeckBuilding' })
  } catch (error) {
    console.error('Error saving deck cards:', error)
    errorMessage.value = 'Server unavailable.'
  } finally {
    isSaving.value = false
  }
}

const removeCardFromDeck = async (cardToRemove) => {
  errorMessage.value = ''
  successMessage.value = ''

  const cardId = cardToRemove.id_printing ?? cardToRemove.id

  if (!cardToRemove.persisted) {
    cardsInDeck.value = cardsInDeck.value.filter(
      (card) => (card.id_printing ?? card.id) !== cardId
    )

    pendingCardsToAdd.value = pendingCardsToAdd.value.filter(
      (card) => (card.id_printing ?? card.id) !== cardId
    )

    return
  }

  try {
    const response = await fetch(
      `http://localhost:5000/api/decks/${deckId}/cards/${cardId}`,
      {
        method: 'DELETE',
        credentials: 'include',
      }
    )

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      errorMessage.value = data.error || `Failed to remove card ${cardToRemove.name}.`
      return
    }

    cardsInDeck.value = cardsInDeck.value.filter(
      (card) => (card.id_printing ?? card.id) !== cardId
    )
  } catch (error) {
    console.error('Error removing card from deck:', error)
    errorMessage.value = 'Server unavailable.'
  }
}

onMounted(() => {
  fetchDeckCards()
})
</script>

<template>
  <div class="p-6 min-h-screen bg-[#09090d] text-white">
    <h1 class="text-2xl font-bold mb-6">Build your deck</h1>

    <p v-if="errorMessage" class="mb-4 text-red-400">
      {{ errorMessage }}
    </p>

    <p v-if="successMessage" class="mb-4 text-green-400">
      {{ successMessage }}
    </p>

    <p v-if="isLoading" class="mb-4 text-white/60">
      Loading cards...
    </p>

    <div class="flex flex-wrap gap-4">
      <CardPlaceHolder @open="openCardModal" :text="'Add a card to your deck'" />

      <div
        v-for="card in cardsInDeck"
        :key="`${card.id_printing ?? card.id}-${card.name}`"
        class="relative w-[63mm] group"
        >
            <button
                type="button"
                @click="removeCardFromDeck(card)"
                class="absolute top-2 right-2 z-10 flex h-7 w-7 items-center justify-center rounded-full bg-black/70 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100 hover:bg-red-500"
            >
                ✕
            </button>

            <img
                :src="card.image_url || card.image"
                :alt="card.name"
                class="w-full rounded-lg shadow-md transition group-hover:brightness-75"
            />
        </div>
    </div>

    <div class="fixed bottom-6 right-6 flex gap-3">
      <button
        @click="goBackToDecks"
        class="bg-red-400 hover:bg-red-500 text-white px-5 py-3 rounded-xl shadow-lg transition-all"
      >
        Cancel
      </button>

      <button
        @click="saveAndGoBackToDecks"
        :disabled="isSaving || pendingCardsToAdd.length === 0"
        class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl shadow-lg transition-all disabled:opacity-50"
      >
        {{ isSaving ? 'Saving...' : 'Save and Return' }}
      </button>
    </div>

    <CardInPlayModal
      v-if="showCardModal"
      title="Search for a card to add to your deck"
      :filters="true"
      :confirmButton="true"
      confirmLabel="Add card to deck"
      @close="closeCardModal"
      @add-card="addCardToDeck"
    />
  </div>
</template>