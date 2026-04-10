<script setup>
import {onMounted, ref} from "vue";
  import Card from "@/components/Cards/Card.vue";

  const combo = ref(null)
 async function getCombo() {
      const stored = localStorage.getItem('dailyCombo')
    const storedDate = localStorage.getItem('dailyComboDate')
    const today = new Date().toDateString()

    if (stored && storedDate === today) {
      combo.value = JSON.parse(stored)
      return
    }
    const base_url = "https://backend.commanderspellbook.com/variants/?ordering=random&limit=1"
   try {
      const response = await fetch(base_url);
     if (!response.ok) {
       throw new Error(`Response Status : ${response.status}`);
     }

     const result = await response.json();
     combo.value = result.results[0];

     localStorage.setItem('dailyCombo', JSON.stringify(combo.value));
     localStorage.setItem('dailyComboDate', today);

   } catch(e) {
      console.error(e.message);
   }
 }

 onMounted(() => getCombo());
</script>

<template>
  <section class="combo-section">
    <div class="combo-header">
      <span class="combo-eyebrow">✦ Featured</span>
      <h2 class="combo-title">Combo of the Day</h2>
    </div>

    <div v-if="combo" class="combo-card">
      <!-- Cards display -->
      <div class="cards-row">
        <div
          v-for="(use, index) in combo.uses"
          :key="use.card.id"
          class="card-wrapper"
          :style="{ '--i': index }"
        >
          <img
            :src="use.card.imageUriFrontNormal"
            :alt="use.card.name"
            class="card-img"
          />
          <div class="card-name">{{ use.card.name }}</div>
        </div>
      </div>

      <div class="produces-row">
        <span v-for="p in combo.produces" :key="p.feature.id" class="produce-badge">
          {{ p.feature.name }}
        </span>
      </div>

      <div class="combo-body">
        <div class="description-block">
          <h3 class="description-label">How it works</h3>
          <ol class="step-list">
            <li
              v-for="(step, i) in combo.description.split('\n').filter(s => s.trim())"
              :key="i"
              class="step-item"
            >
              {{ step.replace(/^\d+\.\s*/, '') }}
            </li>
          </ol>
        </div>

        <div class="combo-meta">
          <div class="identity-badge">{{ combo.identity }}</div>
          <div class="price-block">
            <span class="price-label">TCGPlayer</span>
            <span class="price-value">${{ combo.prices.tcgplayer }}</span>
          </div>
          <div class="price-block">
            <span class="price-label">Card Kingdom</span>
            <span class="price-value">${{ combo.prices.cardkingdom }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading-state">
      <span class="loading-dot" v-for="i in 3" :key="i" :style="{ '--d': i }">●</span>
    </div>
  </section>
</template>

<style scoped>
.combo-section {
  padding: 3rem 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.combo-header {
  margin-bottom: 2rem;
}

.combo-eyebrow {
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #a78bfa;
  font-weight: 600;
}

.combo-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  color: #f1f5f9;
  margin: 0.25rem 0 0;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.combo-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(12px);
}

/* Cards row */
.cards-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.card-wrapper {
  flex: 1;
  min-width: 140px;
  max-width: 200px;
  animation: floatIn 0.5s ease both;
  animation-delay: calc(var(--i) * 0.1s);
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card-img {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-img:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 16px 48px rgba(0,0,0,0.7);
}

.card-name {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: rgba(255,255,255,0.5);
  text-align: center;
  font-weight: 500;
}

/* Produces */
.produces-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.produce-badge {
  background: rgba(167, 139, 250, 0.15);
  border: 1px solid rgba(167, 139, 250, 0.35);
  color: #c4b5fd;
  padding: 0.3rem 0.8rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

/* Body */
.combo-body {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2rem;
  align-items: start;
}

.description-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: rgba(255,255,255,0.35);
  margin: 0 0 0.75rem;
  font-weight: 600;
}

.step-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.step-item {
  display: flex;
  gap: 0.75rem;
  font-size: 0.85rem;
  color: rgba(255,255,255,0.7);
  line-height: 1.5;
  counter-increment: steps;
}

.step-item::before {
  content: counter(steps);
  counter-increment: none;
  min-width: 1.4rem;
  height: 1.4rem;
  background: rgba(167,139,250,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: #a78bfa;
  flex-shrink: 0;
}

.step-list {
  counter-reset: steps;
}

/* Meta */
.combo-meta {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-end;
}

.identity-badge {
  background: linear-gradient(135deg, #1e3a5f, #0f2744);
  border: 1px solid rgba(96,165,250,0.3);
  color: #93c5fd;
  padding: 0.4rem 1rem;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.price-block {
  text-align: right;
}

.price-label {
  display: block;
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255,255,255,0.3);
  margin-bottom: 0.1rem;
}

.price-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #4ade80;
}

.loading-state {
  display: flex;
  gap: 0.4rem;
  padding: 2rem;
  justify-content: center;
}

.loading-dot {
  color: #a78bfa;
  font-size: 0.5rem;
  animation: pulse 1.2s ease infinite;
  animation-delay: calc(var(--d) * 0.2s);
}

@keyframes pulse {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50%       { opacity: 1;   transform: scale(1.4); }
}

@media (max-width: 640px) {
  .combo-body { grid-template-columns: 1fr; }
  .combo-meta { align-items: flex-start; }
}
</style>
