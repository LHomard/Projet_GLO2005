<script setup>
import { reactive, computed, watch } from 'vue'
import whiteIcon from '@/assets/white.png'
import blueIcon from '@/assets/blue.png'
import blackIcon from '@/assets/black.png'
import redIcon from '@/assets/red.png'
import greenIcon from '@/assets/green.png'
import colorlessIcon from '@/assets/colorless.png'

const props = defineProps({
  open: Boolean,
})

const emit = defineEmits(['close', 'create'])

const form = reactive({
  name: '',
  format: '',
  commanderColors: [],
})

const formatOptions = ['Standard', 'Modern', 'Legacy', 'Vintage', 'Pioneer', 'Commander']

const mtgColors = [
  { label: 'White', value: 'W', icon: whiteIcon },
  { label: 'Blue', value: 'U', icon: blueIcon },
  { label: 'Black', value: 'B', icon: blackIcon },
  { label: 'Red', value: 'R', icon: redIcon },
  { label: 'Green', value: 'G', icon: greenIcon },
  { label: 'Colorless', value: 'C', icon: colorlessIcon },
]

const isCommander = computed(() => form.format === 'Commander')

watch(
  () => form.format,
  (newFormat) => {
    if (newFormat !== 'Commander') {
      form.commanderColors = []
    }
  }
)

const submitForm = () => {
  emit('create', {
    name: form.name,
    format: form.format,
    commanderColors: [...form.commanderColors],
  })

  form.name = ''
  form.format = ''
  form.commanderColors = []
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="props.open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      @click.self="$emit('close')"
    >
      <div class="deck-modal">
        <h2 class="modal-title">Create a new deck</h2>

        <form class="deck-form" @submit.prevent="submitForm">
          <div class="form-group">
            <label for="deck-name">Deck name</label>
            <input
              id="deck-name"
              v-model="form.name"
              type="text"
              placeholder="Enter deck name"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="deck-format">Format</label>
            <select
              id="deck-format"
              v-model="form.format"
              class="form-input"
              required
            >
              <option disabled value="">Select a format</option>
              <option
                v-for="format in formatOptions"
                :key="format"
                :value="format"
              >
                {{ format }}
              </option>
            </select>
          </div>

          <div v-if="isCommander" class="form-group">
            <label>Commander colors</label>
            <p class="helper-text">
                Select your commander's color identity
            </p>
            <div class="checkbox-row">
              <label
                v-for="color in mtgColors"
                :key="color.value"
                class="checkbox-item"
              >
                <input
                  v-model="form.commanderColors"
                  type="checkbox"
                  :value="color.value"
                />
                <img :src="color.icon" :alt="color.label" class="color-icon" />
                <span>{{ color.label }}</span>
              </label>
            </div>
          </div>

          <div class="button-row">
            <button type="button" class="secondary-btn" @click="$emit('close')">
              Cancel
            </button>
            <button type="submit" class="primary-btn">
              Create deck
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.deck-modal {
  width: min(92vw, 750px);
  max-height: 85vh;
  overflow-y: auto;

  padding: clamp(1rem, 2vw, 2rem);
  border-radius: 20px;
  backdrop-filter: blur(12px);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.deck-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.95rem;
}

.form-input {
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.06);
  color: white;
  outline: none;
}

.form-input:focus {
  border-color: rgba(255, 255, 255, 0.35);
}

.form-input option {
  background-color: #111827;
  color: white;
}

.helper-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: -4px;
  font-style: italic;
}

.checkbox-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.25rem;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 4px 8px;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.checkbox-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.color-icon {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

.button-row {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.primary-btn,
.secondary-btn {
  padding: 0.7rem 1.2rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.primary-btn {
  background: #374151;
  color: white;
}

.secondary-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
}

.primary-btn:hover,
.secondary-btn:hover {
  transform: scale(1.03);
  opacity: 0.95;
}
</style>