<script setup>
import { ref } from 'vue'
import Deck from '@/components/Decks/Deck.vue'
import DeckPlaceHolder from '@/components/Decks/DeckPlaceHolder.vue'
import CreateDeckModal from '@/components/Decks/CreateDeckModal.vue'

const showCreateDeckModal = ref(false)

const decks = ref([
  {
    name: 'Mono-Red Aggro',
    cards: [
      {
        colors: ['R'],
        id: '0c780e37-91b1-4fe1-85c9-7007d91209d5',
        image:
          'https://cards.scryfall.io/normal/front/0/c/0c780e37-91b1-4fe1-85c9-7007d91209d5.jpg?1681158251',
        name: 'A-Akki Ronin',
        type: 'Creature — Goblin Samurai',
      },
      {
        name: 'Ardent Dustspeaker',
        image:
          'https://cards.scryfall.io/normal/front/7/9/79b12c44-9537-4863-a678-c982e8714a5a.jpg?1681158267',
        colors: ['Red'],
      },
      {
        name: 'Counterspell',
        image:
          'https://c1.scryfall.com/file/scryfall-cards/normal/front/f/1/f129eafc-b42c-4d39-8044-31888a35f22f.jpg?1562897992',
        colors: ['Blue'],
      },
    ],
  },
  {
    name: 'Empty Deck',
    cards: [],
  },
])

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

    decks.value.push({
      id: newDeck.id_deck,
      name: newDeck.nom,
      format: newDeck.id_format,
      cards: [],
    })

    showCreateDeckModal.value = false
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
</script>

<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold text-white mb-6">Your Decks</h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
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
div {
  background-color: #09090d;
  min-height: 100vh;
}
</style>
