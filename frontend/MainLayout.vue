<script setup>
import AppBar from '@/components/NavBar/AppBar.vue'
</script>

<template>
  <div class="flex flex-col h-full bg-[#09090D]">
    <app-bar class="h-16 shrink-0" />

    <div class="flex-1 min-h-0 overflow-auto">
      <router-view />
    </div>
  </div>
</template>