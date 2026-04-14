import { createRouter, createWebHistory} from "vue-router";
import Home from '../pages/Home.vue'
import Decks from '../pages/Decks.vue'
import Cards from '../pages/Cards.vue'
import Chat from '../pages/Chat.vue'
import Login from '../pages/Login.vue'
import { auth } from '@/auth.js'


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
    name: 'DeckBuilding',
    component: Decks,
    meta: { requiresAuth: true},
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    meta: {requiresAuth: true},
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

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !auth.isLoggedIn.value) {
    return { name: 'Login' }
  }
  if (to.name === 'Login' && auth.isLoggedIn.value) {
    return { name: 'Home' }
  }
  return true
})

export default router
