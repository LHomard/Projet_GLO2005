<script setup>
  import { ref } from 'vue';

  const props = defineProps(['cards']);
  const emit = defineEmits(['send']);
  const inputText = ref('');

  async function getJudge(prompt) {
    const url = `http://localhost:5000/api/judges`;
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          message: prompt,
          cards: props.cards})
      });
      if(!response.ok) {
        throw new Error(`Response Status: ${response.status}`)
      }

      const result = await response.json();
      return result.reply;

    } catch (e) {
      console.error(e.message);
    }
  }

  async function submit() {
    if (!inputText.value.trim()) return;
    const reply = await getJudge(inputText.value);
    emit('send', inputText.value, reply);
    inputText.value = '';
  }
</script>

<template>
  <div class="flex justify-center">
    <div class="input-group">
      <input
        class="input-text"
        v-model="inputText"
        name="text"
        type="text"
        placeholder="Type here"
        autocomplete="off"
        @keydown.enter="submit"
      />
      <label class="input-text-label" for="text">Type here</label>
    </div>
  </div>
</template>

<style scoped>
  .input-group {
    display: flex;
    gap: 10px;
    position: relative;
    padding: 7px 0 0;
    width: 80%;
    margin-bottom: 10px;
    margin-top: 2px;
  }

  .input-text {
    font-family: inherit;
    width: 100%;
    border: none;
    border-bottom: 2px solid #7f7f7f;
    border-radius: 0 !important;
    outline: 0;
    font-size: 17px;
    color: #7f7f7f;
    padding: 7px 0;
    background: transparent;
    transition: border-color 0.2s;
  }

  .input-text::placeholder {
    color: transparent;
  }

  .input-text:placeholder-shown ~ .input-text-label {
    font-size: 17px;
    cursor: text;
  }

  .input-text-label {
    position: absolute;
    display: block;
    transition: 0.2s;
    font-size: 17px;
    color: #7f7f7f;
    pointer-events: none;
  }

  .input-text:focus {
    padding-bottom: 6px;
    border-width: 3px;
    border-image: linear-gradient(to right, #214494, #214494);
    border-image-slice: 1;
  }

  .input-text:focus ~ .input-text-label {
    color: #214494;
  }

  .input-text:not(:placeholder-shown) ~ .input-text-label,
  .input-text:focus ~ .input-text-label {
    position: absolute;
    display: block;
    transition: 0.2s;
    font-size: 15px;
    font-weight: 700;
    top: -17px;
  }

  .input-text:required,
  .input-text:invalid {
    box-shadow: none;
  }

</style>
