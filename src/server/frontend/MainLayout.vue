<script setup>
import AppBar from "@/components/NavBar/AppBar.vue";
</script>

<template>
    <div class="flex flex-1 flex-col bg-[#354024]">
      <app-bar/>
    <div id="main-content" style="max-height:calc(100vh - 64px); overflow: auto" class="flex-1">
      <router-view/>
    </div>
  </div>
</template>

<style scoped>
</style>
