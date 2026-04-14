<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Deck from '@/components/Decks/Deck.vue'
import DeckPlaceHolder from '@/components/Decks/DeckPlaceHolder.vue'
import CreateDeckModal from '@/components/Decks/CreateDeckModal.vue'

const router = useRouter()

const showCreateDeckModal = ref(false);
const decks = ref([]);

const createNewDeck = async (deckData) => {
  try {
    const response = await fetch('http://localhost:5000/api/decks', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify({
        deck_name: deckData.name,
        format_name: deckData.format,
        description: deckData.description ?? '',
      }),
    })

    if (!response.ok) {
      const text = await response.text()
      console.error('ERROR RESPONSE:', text)
      return
    }

    const newDeck = await response.json()

    // decks.value.push({
    //   id: newDeck.id_deck,
    //   name: newDeck.nom,
    //   format: newDeck.id_format,
    //   cards: [],
    // })

    showCreateDeckModal.value = false
    await router.push({
      name: 'DeckCreate',
      params: { id: newDeck.id_deck },
    })
  } catch (error) {
    console.error('ERROR while creating new deck:', error)
  }
}

const deleteDeck = async (deckId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/decks/${deckId}`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (!response.ok) {
      const text = await response.text()
      console.error('DELETE ERROR:', text)
      return
    }

    decks.value = decks.value.filter((deck) => deck.id !== deckId)
  } catch (error) {
    console.error('ERROR deleting deck:', error)
  }
}

const fetchDecks = async () => {
  const response = await fetch('http://localhost:5000/api/decks', {
    credentials: 'include',
  })
  if (!response.ok) return

  const data = await response.json()

  decks.value = data.map((d) => ({
    id: d.id,
    name: d.name,
    format: d.format,
    image_url: d.image_url,
    colors: d.colors || [],
    card_count: d.card_count || 0,
    created_at: d.created_at,
  }))
}

onMounted(fetchDecks)
</script>

<template>
  <div class="decks-page p-8">
    <h1 class="text-2xl font-bold text-white mb-6">Your Decks</h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 items-start">
      <DeckPlaceHolder @create="showCreateDeckModal = true" />
      <Deck v-for="deck in decks" :key="deck.name" :deck="deck" @delete_deck="deleteDeck" />
    </div>

    <CreateDeckModal
      :open="showCreateDeckModal"
      @close="showCreateDeckModal = false"
      @create="createNewDeck"
    />
  </div>
</template>

<style scoped>
.decks-page {
  background-color: #09090d;
  min-height: 100vh;
}
</style>
