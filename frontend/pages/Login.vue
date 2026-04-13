<script setup>
import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'

const auth = inject('auth')
const router = useRouter()

const email = ref('')
const password = ref('')

const errorMessage = ref('')
const isLoading = ref(false)

async function login() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
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
</script>

<template>
  <section class="min-h-screen bg-black flex items-center justify-center px-6 py-8">
    <div class="w-full max-w-md">
      <div
        class="w-full rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 bg-gray-800/50 border-gray-800/90"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight md:text-2xl text-white">
            Log in to your account
          </h1>
          <form class="space-y-4 md:space-y-6" @submit.prevent="login">
            <div>
              <label for="email" class="block mb-2 text-sm font-medium text-white">
                Your email
              </label>
              <input
                v-model="email"
                type="email"
                name="email"
                id="email"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
                placeholder="name@company.com"
                required=""
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
                required=""
              />
            </div>
            <p v-if="errorMessage" class="text-sm text-red-600">
              {{ errorMessage }}
            </p>
            <button
              :disabled="isLoading"
              type="submit"
              class="w-full text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center bg-blue-600 hover:bg-blue-700 focus:ring-blue-800"
            >
              Log in
            </button>
            <p class="text-sm font-light text-gray-400">
              Don’t have an account yet?
              <a href="#" class="font-medium text-blue-500"> Sign up </a>
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped></style>
