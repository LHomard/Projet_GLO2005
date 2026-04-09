import { createRouter, createWebHistory} from "vue-router";
import Home from '../pages/Home.vue'
import Decks from '../pages/Decks.vue'
import Cards from '../pages/Cards.vue'
import Chat from '../pages/Chat.vue'
import Login from '../pages/Login.vue'


const routes = [
  {
    path: '/',
    alias: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/cards',
    name: 'Cards',
    component: Cards,
  },
  {
    path: '/decks',
    name: 'Decks',
    component: Decks,
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
]

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
