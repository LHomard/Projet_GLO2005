<script setup>
  defineProps({
    text: String,
    time: String
  });
</script>

<template>
  <div class="flex justify-end items-start gap-2.5">
    <div class="flex flex-col w-full max-w-[320px] leading-1.5">
        <div class="flex items-center space-x-1.5 rtl:space-x-reverse">
            <span class="text-sm text-body text-amber-50">{{ time }}</span>
        </div>
        <p class="text-sm py-2 text-heading text-amber-50">{{ text }} </p>
    </div>
  </div>
</template>

<style scoped>

</style>
