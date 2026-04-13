<script setup>
  import MainLayout from '../MainLayout.vue'
  import { provide } from 'vue'
  import {auth} from "@/auth.js";

  provide('auth', auth)
</script>

<template>
  <main-layout/>
</template>
