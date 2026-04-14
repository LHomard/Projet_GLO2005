<script setup>
  import { ref } from 'vue';
  import CardPlaceHolder from "@/components/Chat/CardPlaceHolder.vue";
  import CardInPlayModal from "@/components/Chat/CardInPlayModal.vue";

  const showModal = ref(false);
  const selectedCards = ref([]);
  const emit = defineEmits(['update-cards']);

  const handleCardSelection = (card) => {
    selectedCards.value.push(card);
    emit('update-cards', selectedCards.value);
    showModal.value = false;
  };

  const removeCard = (index) => {
    selectedCards.value.splice(index, 1);
    emit('update-cards', selectedCards.value);
  };

  const addCardFromAI = (card) => {
    if (!selectedCards.value.find(c => c.name === card.name)) {
      selectedCards.value.push({
        ...card,
        image: card.image_url
      });
      emit('update-cards', selectedCards.value);
    }
  };

  defineExpose({ addCardFromAI });
</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-if="selectedCards.length > 0" class="flex flex-col gap-5">

      <div v-for="(card, index) in selectedCards" :key="index" class="relative group">
         <img
           :src="card.image"
           class="w-63 h-auto rounded-[12px] shadow-2xl border border-white/5"
         />

         <button
            @click="removeCard(index)"
            class="absolute -top-2 -right-2 bg-gray-600 hover:bg-gray-600 text-white rounded-full w-7 h-7 flex items-center justify-center shadow-lg border-2 border-[#303F54] transition-opacity opacity-0 group-hover:opacity-100 z-10"
         >
            <span class="text-xs font-bold">✕</span>
         </button>
      </div>
    </div>

    <CardPlaceHolder @open="showModal = true" :text="'Add card in play'" />

    <CardInPlayModal
      v-if="showModal"
      title="Search for card in play"
      @close="showModal = false"
      @select-card="handleCardSelection"
    />
  </div>
</template>
