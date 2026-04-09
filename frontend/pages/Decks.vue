<script setup>
import { ref } from 'vue'
import Deck from '@/components/Decks/Deck.vue' // your deck card component

const fakeDecks = ref([
  {
    name: 'Mono-Red Aggro',
    cards: [
      {
        colors: ['R'],
        id: '0c780e37-91b1-4fe1-85c9-7007d91209d5',
        image:
          'https://cards.scryfall.io/normal/front/0/c/0c780e37-91b1-4fe1-85c9-7007d91209d5.jpg?1681158251',
        name: 'A-Akki Ronin',
        type: 'Creature \u2014 Goblin Samurai',
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
    name: 'Blue Control',
    cards: [
      {
        name: 'Counterspell',
        image:
          'https://c1.scryfall.com/file/scryfall-cards/normal/front/f/1/f129eafc-b42c-4d39-8044-31888a35f22f.jpg?1562897992',
        colors: ['Blue'],
      },
      {
        name: 'Island',
        image:
          'https://c1.scryfall.com/file/scryfall-cards/normal/front/0/f/0f83a8e1-837e-45a2-a9a0-55fa53cb056b.jpg?1562812236',
        colors: ['Blue'],
      },
    ],
  },
  {
    name: 'Empty Deck',
    cards: [],
  },
])
</script>

<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold text-white mb-6">Your Decks</h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <Deck v-for="deck in fakeDecks" :key="deck.name" :deck="deck" />
    </div>
  </div>
</template>

<style scoped>
div {
  background-color: #09090d;
  min-height: 100vh;
}
</style>
