<script setup>
  const props = defineProps({ set: Object })
</script>

<template>
  <article
    class="w-100 shadow-xl bg-cover bg-center relative border-8 rounded-xl border-black transform duration-500 hover:-translate-y-12 group overflow-hidden"
    :style="{ backgroundImage: `url(${props.set.image})` }">
    <div class="bg-black/60 group-hover:bg-black/20 relative min-h-150 flex flex-wrap flex-col hover:bg-opacity-75 transform duration-300">
      <div class="p-8 h-full justify-end flex flex-col rounded-lg">
        <img :src="props.set.icon" class="w-10 h-10 mb-3 invert" />
        <p class="text-white mt-2 text-xl mb-5 uppercase duration-300 group-hover:text-orange-500">{{ props.set.name }}</p>
        <p class="text-gray-400 text-xs mt-1">{{ props.set.card_count }} cards</p>
      </div>
    </div>
  </article>
</template>

<style scoped>

</style>
