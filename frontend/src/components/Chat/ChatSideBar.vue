<script setup>
  import { ref, onMounted } from "vue";

  const props = defineProps(['playerId'])
  const emit = defineEmits(['newChat', 'getSelectedChat']);
  const chatDiscussion = ref([]);

  onMounted(async () => {
    const res = await fetch(`http://localhost:5000/api/judges/id_player/${props.playerId}`);
    const data = await res.json();
    chatDiscussion.value = data.history;
  })


  function newChat() {
    emit('newChat');
  }

  async function getSelectedChat(chatId) {

    const url = `http://localhost:5000/api/judges/chat/${chatId}`;
    try {
      const response = await fetch(url);
      if(!response.ok) {
        throw new Error(`Response Status: ${response.status}`)
      }

      const result = await response.json();
      emit('getSelectedChat', {chatId, history: result.chat.chats})

    } catch (e) {
      console.error(e.message);
    }
  }

  async function deleteChat(chatId){
    const url = `http://localhost:5000/api/chat/${chatId}`
    try  {
      const response = await fetch(url, {method: 'DELETE'});
      if (!response.ok){
        throw new Error(`Response status: ${response.status}`)
      }

      chatDiscussion.value = chatDiscussion.value.filter(chat => chat.id_chat !== chatId);

    } catch(e){
      console.error(e.message);
    }
  }
</script>

<template>
  <div class="hidden peer-checked:flex md:flex flex-col w-80 bg-gray-800 transition-all duration-300 ease-in-out h-full min-h-0">
			<div class="flex items-center justify-between h-16 bg-gray-900 px-4">
				<span class="text-white font-bold uppercase">The Oracle</span>
				<label for="menu-toggle" class="text-white cursor-pointer">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 lg:hidden" fill="none" viewBox="0 0 24 24"
						stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
							d="M6 18L18 6M6 6l12 12" />
					</svg>
				</label>
			</div>
      <button @click="newChat">
        New Chat
      </button>
    <nav class="chat flex-1 min-h-0 px-8 py-4 bg-gray-800 overflow-y-auto">

      <hr class="border-b-black my-3">


      <a v-for="chat in chatDiscussion"
         :key="chat.id_chat"
         @click="getSelectedChat(chat.id_chat)"
         class="fancy" href="#">
          <button @click.stop="deleteChat(chat.id_chat)" class="delete">
            x
          </button>
        <span class="top-key gap-x-1"></span>
        <span class="text">{{ chat.title }}</span>
        <span class="bottom-key-1"></span>
        <span class="bottom-key-2"></span>
      </a>

    </nav>
		</div>
</template>

<style scoped>
  .fancy {
     background-color: transparent;
     border: 2px solid #000;
     border-radius: 0;
     box-sizing: border-box;
     color: #fff;
     cursor: pointer;
     display: inline-block;
     float: none;
     font-weight: 700;
     letter-spacing: 0.05em;
     margin: 0;
     outline: none;
     overflow: visible;
     padding: 1.25em 2em;
     position: relative;
     text-align: center;
     text-decoration: none;
     text-transform: none;
     transition: all 0.3s ease-in-out;
     user-select: none;
     font-size: 13px;
     width: 100%;

  }


  .fancy::before {
     content: " ";
     width: 1.5625rem;
     height: 2px;
     background: black;
     top: 50%;
     left: 1.5em;
     position: absolute;
     transform: translateY(-50%);
     transform-origin: center;
     transition: background 0.3s linear, width 0.3s linear;
  }

  .fancy .text {
     font-size: 1.125em;
     line-height: 1.33333em;
     padding-left: 2em;
     display: block;
     text-align: left;
     transition: all 0.3s ease-in-out;
     text-transform: uppercase;
     text-decoration: none;
     color: black;
     white-space: nowrap;
     overflow: hidden;
     text-overflow: ellipsis;
     max-width: 200px;
  }

  .fancy .top-key {
     height: 2px;
     width: 1.5625rem;
     top: -2px;
     left: 0.625rem;
     position: absolute;
     background: #e8e8e8;
     transition: width 0.5s ease-out, left 0.3s ease-out;
  }

  .fancy .bottom-key-1 {
     height: 2px;
     width: 1.5625rem;
     right: 1.875rem;
     bottom: -2px;
     position: absolute;
     background: #e8e8e8;
     transition: width 0.5s ease-out, right 0.3s ease-out;
  }

  .fancy .bottom-key-2 {
     height: 2px;
     width: 0.625rem;
     right: 0.625rem;
     bottom: -2px;
     position: absolute;
     background: #e8e8e8;
     transition: width 0.5s ease-out, right 0.3s ease-out;
  }

  .fancy:hover {
     color: white;
     background: black;
  }

  .fancy:hover::before {
     width: 0.9375rem;
     background: white;
  }

  .fancy:hover .text {
     color: white;
     padding-left: 1.5em;
  }

  .fancy:hover .top-key {
     left: -2px;
     width: 0px;
  }

  .fancy:hover .bottom-key-1,
     .fancy:hover .bottom-key-2 {
       right: 0;
       width: 0;
  }

  button {
    align-items: center;
    background-color: transparent;
    color: #fff;
    cursor: pointer;
    display: flex;
    font-family: ui-sans-serif,system-ui,-apple-system,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.5;
    text-decoration: none;
    text-transform: uppercase;
    outline: 0;
    border: 0;
    padding: 1rem;
  }

  .button:before {
    background-color: #fff;
    content: "";
    display: inline-block;
    height: 1px;
    margin-right: 10px;
    transition: all .42s cubic-bezier(.25,.8,.25,1);
    width: 0;
  }

  .button:hover:before {
    background-color: #fff;
    width: 3rem;
  }

  .chat::-webkit-scrollbar {
    display: none;
  }

  .delete {
    position: absolute;
    left: 8px;
    top: 50%;
    transform: translateY(-50%);
    padding: 0;
    width: 20px;
    height: 20px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
