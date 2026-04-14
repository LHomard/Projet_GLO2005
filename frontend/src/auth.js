import { computed, ref } from 'vue'

const currentUser = ref(null)
const isLoggedIn = computed(() => !!currentUser.value)

function login(user) {
  currentUser.value = user
}

function logout() {
  currentUser.value = null
}

export const auth = {
  currentUser,
  isLoggedIn,
  login,
  logout,
}
