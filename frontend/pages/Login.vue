<script setup>
import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'

const auth = inject('auth')
const router = useRouter()

const mode = ref('login')

const first_name = ref('')
const last_name = ref('')
const gender = ref('')
const other_gender = ref('')
const email = ref('')
const password = ref('')
const username = ref('')
const age = ref('')

const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

let messageTimeout = null

function showMessage(type, message, duration) {
  if (messageTimeout) {
    clearTimeout(messageTimeout)
  }

  if (type === 'error') {
    errorMessage.value = message
    successMessage.value = ''
  } else {
    successMessage.value = message
    errorMessage.value = ''
  }

  messageTimeout = setTimeout(() => {
    errorMessage.value = ''
    successMessage.value = ''
  }, duration)
}

function switchMode(newMode) {
  mode.value = newMode
  errorMessage.value = ''
  successMessage.value = ''
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
      showMessage('error', data.error || 'Login failed.', 5000)
      return
    }

    auth.login(data.user)
    await router.push({ name: 'DeckBuilding' })
  } catch (error) {
    showMessage('error', 'Server unavailable.', 5000)
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

async function signup() {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  const finalGender = gender.value === 'other' ? other_gender.value : gender.value

  try {
    const response = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: first_name.value,
        last_name: last_name.value,
        gender: finalGender,
        username: username.value,
        email: email.value,
        age: age.value,
        password: password.value,
      }),
    })

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      showMessage('error', data.error || 'Sign up failed.', 5000)
      return
    }

    username.value = ''
    age.value = ''
    password.value = ''
    mode.value = 'login'
    showMessage('success', 'Account created successfully. You can now log in.', 3000)
  } catch (error) {
    console.error('Signup error:', error)
    showMessage('error', 'Server unavailable.', 5000)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <section
    class="h-full bg-black flex items-center justify-center px-6 py-8 overflow-hidden!"
  >
    <div class="w-full max-w-md">
      <div class="w-full rounded-lg shadow dark:border bg-gray-800/50 border-gray-800/90 mb-16">
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
          <form v-if="mode === 'login'" class="flex flex-col gap-6" @submit.prevent="login">
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
            <p v-if="errorMessage" class="text-sm text-red-400">
              {{ errorMessage }}
            </p>

            <p v-if="successMessage" class="text-sm text-green-400">
              {{ successMessage }}
            </p>
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
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block mb-2 text-sm font-medium text-white"> First name </label>
                <input
                  v-model="first_name"
                  type="text"
                  placeholder="John"
                  class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block mb-2 text-sm font-medium text-white"> Last name </label>
                <input
                  v-model="last_name"
                  type="text"
                  placeholder="Doe"
                  class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="age" class="block mb-2 text-sm font-medium text-white"> Age </label>
                <input
                  v-model="age"
                  type="number"
                  id="age"
                  placeholder="25"
                  min="1"
                  max="120"
                  class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-white"> Gender </label>
                <select
                  v-model="gender"
                  :class="gender === '' ? 'text-gray-400' : 'text-white'"
                  class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 focus:ring-blue-500 appearance-none"
                >
                  <option value="" disabled selected>Select</option>
                  <option value="male" class="text-white">Male</option>
                  <option value="female" class="text-white">Female</option>
                  <option value="non_binary" class="text-white">Non-binary</option>
                  <option value="other" class="text-white">Other</option>
                  <option value="prefer_not_say" class="text-white">N/A</option>
                </select>
              </div>
            </div>

            <div v-if="gender === 'other'" class="mt-2">
              <input
                v-model="other_gender"
                type="text"
                placeholder="Please specify"
                class="rounded-lg focus:outline-none focus:ring-2 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500"
              />
            </div>

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
            <p v-if="errorMessage" class="text-sm text-red-400">
              {{ errorMessage }}
            </p>
            <div class="flex justify-center mt-4">
              <button
                :disabled="isLoading"
                type="submit"
                class="w-50 text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center bg-blue-600 hover:bg-blue-700 focus:ring-blue-800 disabled:opacity-50"
              >
                {{ isLoading ? 'Creating account...' : 'Create account' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped></style>
