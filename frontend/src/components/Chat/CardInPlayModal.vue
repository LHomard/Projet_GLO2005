<script setup>
  import { ref } from "vue";

  const emit = defineEmits(['close', 'select-card']); // Added select-card event

  const searchQuery = ref('');
  const cardInPlay = ref([]);

  async function getData() {

    if (!searchQuery.value.trim()) {
    cardInPlay.value = [];
    return;
    }

    const url = `http://localhost:5000/api/cards?search=${searchQuery.value}`;
    try {
      const response = await fetch(url);
      if(!response.ok) {
        if (response.status === 404)  {
          cardInPlay.value = [];
          return;
        }
        throw new Error(`Response Status: ${response.status}`)
      }

      const result = await response.json();
      cardInPlay.value = result.cards || [];

    } catch (e) {
      console.error(e.message);
      cardInPlay.value = [];
    }
  }
</script>

<template>
  <div class="fixed inset-0 bg-black/80 backdrop-blur-sm flex justify-center items-center z-50 p-4" @click.self="$emit('close')">

    <div class="bg-[#303F54] border border-white/10 rounded-xl shadow-2xl w-full max-w-2xl flex flex-col max-h-[90vh]">

      <div class="p-6 pb-0 flex justify-between items-center">
        <label class="text-white font-bold text-xl">Search For Card In Play</label>
        <button @click="$emit('close')" class="text-white/50 hover:text-white">✕</button>
      </div>

      <div class="p-6 pb-2 relative">
        <input
          v-model="searchQuery"
          @keyup="getData"
          type="text"
          class="bg-slate-900/50 border border-white/10 text-white text-sm rounded-lg w-full px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type a card name..."
        />
      </div>

      <div class="p-6 pt-2 overflow-y-auto custom-scrollbar">
        <div v-if="cardInPlay.length > 0" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div
            v-for="card in cardInPlay"
            :key="card.id"
            @click="$emit('select-card', card)"
            class="group cursor-pointer"
          >
           <img
              :src="card.image"
              class="w-32 h-auto rounded-lg shadow-md hover:scale-105 transition-transform"
            />
          </div>
        </div>

        <div v-else-if="searchQuery" class="text-center py-10 text-white/30">
          No cards found...
        </div>
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
