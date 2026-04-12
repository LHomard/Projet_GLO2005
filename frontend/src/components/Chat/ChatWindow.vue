<script setup>
import { ref } from 'vue'

import InputBar from "@/components/Chat/InputBar.vue";
import UserBubble from "@/components/Chat/UserBubble.vue";
import AIBubble from "@/components/Chat/AIBubble.vue";
import CardInPlay from "@/components/Chat/CardInPlay.vue";
import ChatSideBar from "@/components/Chat/ChatSideBar.vue";

const messages = ref([]);
const selectedCards = ref([]);
const cardInPlayRef = ref(null);

function handleSend(text, responseData) {
  messages.value.push({ role: 'user', text, time: new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'}) });
  if (responseData) {
    messages.value.push({ role: 'ai', text: responseData.reply, time: new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})});

    if (responseData.new_cards && responseData.new_cards.length > 0) {
      responseData.new_cards.forEach(card => {
        cardInPlayRef.value?.addCardFromAI(card);
      });
    }
  }
}

const updateCards = (cards) => {
  selectedCards.value = cards;
};

</script>

<template>
  <div class="flex">

    <div class="py-3 px-3 flex-col">
      <CardInPlay ref="cardInPlayRef" @update-cards="updateCards" />
    </div>
    <div class="flex flex-col flex-1 h-screen pt-1">
      <div class="fix flex-1 overflow-y-auto px-50 py-4 space-y-3">
        <template v-for="(msg, i) in messages" :key="i">
          <UserBubble v-if="msg.role === 'user'" :text="msg.text" :time="msg.time" />
          <AIBubble v-else :text="msg.text" :time="msg.time" />
        </template>
      </div>

      <div class="px-4 pb-4">
        <InputBar
          :currentChatId="currentChatId"
          :playerId="1"
          :cards="selectedCards"
          @updateChatId="id => currentChatId = id"
          @send="handleSend"
        />
      </div>
    </div>

    <div>
      <ChatSideBar />
    </div>
  </div>
</template>

<style scoped>
  .fix::-webkit-scrollbar {
    display: none;
  }

  .ascii-bg-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1; /* Pushes it behind everything else */
  pointer-events: none; /* Allows you to click 'through' it to the chat */
}
</style>
