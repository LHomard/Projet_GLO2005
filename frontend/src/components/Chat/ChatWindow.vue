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
  const currentChatId = ref(null);

  function handleSend(text, responseData) {
    messages.value.push({ role: 'user', text, time: new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'}) });
    if (responseData) {
      messages.value.push({ role: 'ai', text: responseData.reply, time: new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})});

      if (responseData.chatId) {
        currentChatId.value = responseData.chatId;
      }

      if (responseData.new_cards?.length > 0) {
        responseData.new_cards.forEach(card => {
          cardInPlayRef.value?.addCardFromAI(card);
        });
      }
    }
  }

  function onSelectChat({chatId, history}){
    currentChatId.value = chatId
    messages.value = history.map(msg => ({
      ...msg, time: ''
    }))
  }

  function resetChat() {
    messages.value = [];
    currentChatId.value = null;
  }

  const updateCards = (cards) => {
    selectedCards.value = cards;
  };

</script>

<template>
  <div class="flex h-full min-h-0">

    <div class="py-3 px-3 flex-col">
      <CardInPlay ref="cardInPlayRef" @update-cards="updateCards" />
    </div>
    <div class="flex flex-col flex-1 min-h-0 pt-1">
      <div class="fix flex-1 min-h-0 overflow-y-auto px-50 py-4 space-y-3">
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
          :history="messages"
          @send="handleSend"
        />
      </div>
    </div>

    <div>
      <ChatSideBar
        :playerId="1"
        @newChat="resetChat"
        @getSelectedChat="onSelectChat"
      />
    </div>
  </div>
</template>

<style scoped>
  .fix::-webkit-scrollbar {
    display: none;
  }
</style>
