<script setup>
  import bg from '@/assets/background.jpg'
</script>

<template>
        <section class="relative bg-gradient-to-br from-blue-900 to-indigo-800 text-white overflow-hidden min-h-screen">
            <div class="absolute inset-0 bg-black opacity-50"></div>
            <div class="absolute inset-0 bg-cover bg-center" :style="{ backgroundImage: `url(${bg})`, filter: 'blur(10px)', transform: 'scale(1.05)' }"></div>
            <div class="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-b from-transparent to-[#08060DFF] z-10"></div>

            <div class="container mx-auto px-4 py-24 md:py-32 relative z-20">
                <div class="flex flex-col md:flex-row items-center justify-between">
                    <!-- Left Side: Info -->
                    <div class="w-full md:w-1/2 mb-12 md:mb-0">
                        <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                          Gather. Battle. Conquer.
                        </h1>
                    </div>
                </div>
            </div>
        </section>
</template>

<style scoped>
  background_box {
    background-color: #050d1a;
    background-image:
    radial-gradient(ellipse at 20% 50%, rgba(29, 78, 216, 0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(67, 56, 202, 0.15) 0%, transparent 60%);
    min-height: 100vh;
  }
</style>
