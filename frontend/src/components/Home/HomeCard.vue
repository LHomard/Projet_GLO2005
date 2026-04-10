<script setup>
  const props = defineProps({ set: Object })
</script>

<template>
  <article
    class="w-100 shadow-xl bg-cover bg-center relative rounded-xl border-l-4 border-[#a78bfa] transform duration-500 hover:-translate-y-12 group overflow-hidden"
    :style="{ backgroundImage: `url(${props.set.image})` }">
    <div class="bg-black/70 group-hover:bg-black/40 relative min-h-150 flex flex-col justify-between transform duration-300 p-6">
      <img :src="props.set.icon" class="w-20 h-20 invert opacity-50 group-hover:opacity-100 duration-300" />
      <div>
        <div class="w-8 h-0.5 bg-[#a78bfa] mb-3 scale-x-0 group-hover:scale-x-100 origin-left duration-300" />
        <p class="text-white uppercase tracking-widest text-base font-medium duration-300 group-hover:text-[#a78bfa]">{{ props.set.name }}</p>
        <p class="text-white/40 text-xs mt-1 group-hover:text-white/70 duration-300">{{ props.set.card_count }} cards</p>
      </div>
    </div>
  </article>
</template>

<style scoped>

</style>
