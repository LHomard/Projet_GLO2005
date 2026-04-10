<script setup>
import { ref, watch } from 'vue'

const loading = ref(false)
const error = ref(null)
const cardInfo = ref(null)

const props = defineProps({ cardId: [Number, String] })
defineEmits(['close'])

const fetchCardInfo = async (id) => {
  if (!id) return
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`http://localhost:5000/api/cards/${id}`)
    if (!res.ok) throw new Error('Error while retrieving card data')
    cardInfo.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

watch(() => props.cardId, fetchCardInfo, { immediate: true })
</script>

<template>
  <Teleport to="body">
    <div
      v-if="props.cardId"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 overflow-hidden"
      @click.self="$emit('close')"
    >
      <div class="cardInfo-card max-w-sm w-full mx-4 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
        <div v-if="loading" class="text-white text-center py-8">Loading data...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>

        <div v-else-if="cardInfo">
          <h3 class="text-white text-xl font-bold mb-4">{{ cardInfo.name }}</h3>
          <div class="flex align-middle">
            <img
              :src="cardInfo.image"
              :alt="cardInfo.name"
              class="w-full rounded-[10px] shadow-[0_8px_32px_rgba(0,0,0,0.5)]"
            />
          </div>
          <hr class="my-4" />
          <div class="card-details">
            <div class="detail-row">
              <span class="label">Mana cost</span>
              <span class="value">{{ cardInfo.mana_cost ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Release date</span
              ><span class="value">{{ cardInfo.release_date ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">CMC</span><span class="value">{{ cardInfo.cmc ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Power</span><span class="value">{{ cardInfo.power ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Toughness</span
              ><span class="value">{{ cardInfo.toughness ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Rarity</span
              ><span class="value capitalize">{{ cardInfo.rarity ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Set</span
              ><span class="value">{{ cardInfo.set_name ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Artist</span
              ><span class="value">{{ cardInfo.artist ?? '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Price</span
              ><span class="value">{{ cardInfo.price ? `$${cardInfo.price}` : '—' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style>
.cardInfo-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(12px);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 6px;
}

.label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
}

.value {
  color: white;
  font-size: 0.875rem;
}
</style>
