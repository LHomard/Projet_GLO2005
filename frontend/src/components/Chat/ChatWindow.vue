<script setup>
import { ref } from 'vue'

import InputBar from "@/components/Chat/InputBar.vue";
import UserBubble from "@/components/Chat/UserBubble.vue";
import AIBubble from "@/components/Chat/AIBubble.vue";
import CardInPlay from "@/components/Chat/CardInPlay.vue";

const messages = ref([])

function handleSend(text) {
  if (!text.trim()) return;

  messages.value.push({ role: 'user', text, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
}

</script>

<template>
  <div class="flex">
    <div>
      <CardInPlay />
    </div>
    <div class="flex flex-col flex-1 h-screen pt-1">
      <div class="fix flex-1 overflow-y-auto px-50 py-4 space-y-3">
        <template v-for="(msg, i) in messages" :key="i">
          <UserBubble v-if="msg.role === 'user'" :text="msg.text" :time="msg.time" />
          <AIBubble v-else :text="msg.text" :time="msg.time" />
        </template>
      </div>

      <div class="px-4 pb-4">
        <InputBar @send="handleSend" />
      </div>
    </div>
  </div>
</template>

<style scoped>
  .fix::-webkit-scrollbar {
    display: none;
  }
</style>
