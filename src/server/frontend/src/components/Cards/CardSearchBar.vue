<script setup>

</script>

<template>
    <div class="relative">
    <input
      type="text"
      placeholder="Search..."
      class="glass bg-white/10 border border-white/20 text-white placeholder-white px-4 py-2 rounded-full w-40 focus:w-64 transition-width duration-500 ease-in-out focus:outline-none focus:ring-2 focus:ring-white/30"
    />
    <svg
      class="absolute right-3 top-2.5 w-5 h-5 text-white pointer-events-none"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1010.5 3a7.5 7.5 0 006.15 13.65z"
      />
    </svg>
  </div>
</template>

<style scoped>
      .glass {
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }

    .transition-width {
      transition: width 0.4s ease;
    }
</style>
