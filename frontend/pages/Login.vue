<script setup>
import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'

const auth = inject('auth')
const router = useRouter()

const mode = ref('login')

const email = ref('')
const password = ref('')
const username = ref('')
const age = ref('')

const errorMessage = ref('')
const isLoading = ref(false)

function switchMode(newMode) {
  mode.value = newMode
  errorMessage.value = ''
}

async function login() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value }),
    })

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      errorMessage.value = data.error || 'Login failed.'
      return
    }

    auth.login(data.user)
    await router.push({ name: 'Deck building' })
  } catch (error) {
    errorMessage.value = 'Server unavailable.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

async function signup() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const response = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        age: age.value,
        password: password.value,
      }),
    })

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      errorMessage.value = data.error || 'Sign up failed.'
      return
    }

    auth.login(data.user)
    await router.push({ name: 'Deck building' })
  } catch (error) {
    errorMessage.value = 'Server unavailable.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <section class="min-h-screen bg-black flex items-center justify-center px-6 py-8">
    <div class="w-full max-w-md">
      <div class="w-full rounded-lg shadow dark:border bg-gray-800/50 border-gray-800/90">
        <!-- Toggle tabs -->
        <div class="flex rounded-t-lg overflow-hidden border-b border-gray-700">
          <button
            @click="switchMode('login')"
            class="flex-1 py-3 text-sm font-medium transition-colors duration-200"
            :class="
              mode === 'login'
                ? 'bg-gray-700 text-white'
                : 'bg-transparent text-gray-400 hover:text-white'
            "
          >
            Log in
          </button>
          <button
            @click="switchMode('signup')"
            class="flex-1 py-3 text-sm font-medium transition-colors duration-200"
            :class="
              mode === 'signup'
                ? 'bg-gray-700 text-white'
                : 'bg-transparent text-gray-400 hover:text-white'
            "
          >
            Sign up
          </button>
        </div>

        <div class="p-6 space-y-4 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight md:text-2xl text-white">
            {{ mode === 'login' ? 'Log in to your account' : 'Create an account' }}
          </h1>

          <!-- LOGIN FORM -->
          <form v-if="mode === 'login'" class="space-y-4 md:space-y-6" @submit.prevent="login">
            <div>
              <label for="email" class="block mb-2 text-sm font-medium text-white">
                Your email
              </label>
              <input
                v-model="email"
                type="email"
                name="email"
                id="email"
                placeholder="name@company.com"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-white">
                Password
              </label>
              <input
                v-model="password"
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <p v-if="errorMessage" class="text-sm text-red-400">{{ errorMessage }}</p>
            <button
              :disabled="isLoading"
              type="submit"
              class="w-full text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center bg-blue-600 hover:bg-blue-700 focus:ring-blue-800 disabled:opacity-50"
            >
              {{ isLoading ? 'Logging in...' : 'Log in' }}
            </button>
          </form>

          <!-- SIGNUP FORM -->
          <form v-else class="space-y-4 md:space-y-6" @submit.prevent="signup">
            <div>
              <label for="username" class="block mb-2 text-sm font-medium text-white">
                Username
              </label>
              <input
                v-model="username"
                type="text"
                id="username"
                placeholder="YourUsername"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label for="signup-email" class="block mb-2 text-sm font-medium text-white">
                Email
              </label>
              <input
                v-model="email"
                type="email"
                id="signup-email"
                placeholder="name@company.com"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label for="age" class="block mb-2 text-sm font-medium text-white"> Age </label>
              <input
                v-model="age"
                type="number"
                id="age"
                placeholder="25"
                min="1"
                max="120"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label for="signup-password" class="block mb-2 text-sm font-medium text-white">
                Password
              </label>
              <input
                v-model="password"
                type="password"
                id="signup-password"
                placeholder="••••••••"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <p v-if="errorMessage" class="text-sm text-red-400">{{ errorMessage }}</p>
            <button
              :disabled="isLoading"
              type="submit"
              class="w-full text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center bg-blue-600 hover:bg-blue-700 focus:ring-blue-800 disabled:opacity-50"
            >
              {{ isLoading ? 'Creating account...' : 'Create account' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped></style>
