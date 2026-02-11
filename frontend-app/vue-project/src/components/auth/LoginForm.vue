<template>
  <!-- login form -->
  <!-- Animated error -->
  <Transition name="error-slide">
    <div v-if="error" class="overflow-hidden">
      <h1 class="text-red-500 mb-2">
        {{ error }}
      </h1>
    </div>
  </Transition>
  <div class="divider"></div>
  <form action="" class="flex flex-col gap-5">
    <div class="form-control flex flex-col gap-2">
      <label class="label">
        <span class="label-text">{{ $t('common.username') }}</span>
      </label>
      <input v-model="username" placeholder="testuser" class="input input-bordered w-full" />
    </div>
    <div class="form-control flex flex-col gap-2">
      <label class="label">
        <span class="label-text">{{ $t('common.password') }}</span>
      </label>
      <input v-model="password" type="password" :placeholder="$t('common.password')"
        class="input input-bordered w-full" />
    </div>
  </form>
  <div class="flex mt-6">
    <button class="btn btn-primary flex-1" @click="login">
      {{ $t('common.login') }}
    </button>
  </div>
  <!-- google auth button -->
  <div class="flex mt-6">
    <button class="btn btn-neutral flex-1" @click="loginGoogle">
      <font-awesome-icon icon="fa-brands fa-google" />
      {{ $t('common.login_with_google') }}
    </button>
  </div>
  <div class="divider"></div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { API_ENDPOINTS } from '@/config/api'
import { api } from '@/services/axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      authStore: null
    }
  },

  mounted() {
    this.authStore = useAuthStore()

    const access = this.$route.query.access_token
    const refresh = this.$route.query.refresh_token

    if (access && refresh) {
      this.authStore.setAuthData(access, refresh)
      this.$router.replace('/')
    }
  },

  methods: {
    async login() {
      this.error = ''

      if (!this.username || !this.password) {
        this.error = 'All fields are required'
        return
      }

      try {
        await this.authStore.login(this.username, this.password)
        this.$router.push('/')
      } catch (err) {
        console.error(err)
        if (err.response?.data?.detail) {
          this.error = err.response.data.detail
        } else if (typeof err === 'string') {
          this.error = err
        } else {
          this.error = 'Login failed'
        }
      }
    },

    loginGoogle() {
      window.location.href = api.defaults.baseURL + API_ENDPOINTS.GOOGLE_LOGIN
    }
  }
}
</script>


<style scoped>
.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 100px;
}
</style>