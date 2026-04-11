<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: String,
  options: Array, // [{ value: 'name', label: 'Nom' }]
})
const emit = defineEmits(['update:modelValue'])

const open = ref(false)

const select = (value) => {
  emit('update:modelValue', value)
  open.value = false
}

const selectedLabel = () => props.options.find((o) => o.value === props.modelValue)?.label
</script>

<template>
  <div class="relative">
    <button
      @click="open = !open"
      class="bg-[#3a3a3a] border-white/10 rounded-lg px-3 py-2 text-white w-full text-left flex justify-between items-center gap-4"
    >
      {{ selectedLabel() }}
      <span class="text-white/40 text-xs">{{ open ? '▲' : '▼' }}</span>
    </button>

    <Transition name="slide-down">
      <div
        v-if="open"
        class="absolute z-100 mt-1 w-full bg-[#3a3a3a] border border-white/10 rounded-lg overflow-hidden shadow-xl"
      >
        <div
          v-for="option in options"
          :key="option.value"
          @click="select(option.value)"
          class="px-3 py-2 hover:bg-white/10 cursor-pointer text-white text-sm"
          :class="{ 'bg-[#3a3a3a]': option.value === modelValue }"
        >
          {{ option.label }}
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.slide-down-enter-from,
.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
}
.slide-down-enter-to,
.slide-down-leave-from {
  max-height: 200px;
  opacity: 1;
}
</style>
