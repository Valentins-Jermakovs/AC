<template>
  <div class="transition-all duration-500">
    <!-- register form -->
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
          <span class="label-text">{{ $t('common.email') }}</span>
        </label>
        <input
          v-model="email"
          type="email"
          placeholder="test@example.com"
          class="required input input-bordered w-full"
        />
      </div>
      <div class="form-control flex flex-col gap-2">
        <label class="label">
          <span class="label-text">{{ $t('common.username') }}</span>
        </label>
        <input
          v-model="username"
          type="text"
          placeholder="testuser"
          class="input input-bordered w-full"
        />
      </div>
      <div class="form-control flex flex-col gap-2">
        <label class="label">
          <span class="label-text">{{ $t('common.password') }}</span>
        </label>
        <input
          v-model="password"
          type="password"
          :placeholder="$t('common.password')"
          class="input input-bordered w-full"
        />
      </div>
      <div class="form-control flex flex-col gap-2">
        <label class="label">
          <span class="label-text">{{ $t('common.confirm_password') }}</span>
        </label>
        <input
          v-model="confirmPassword"
          type="password"
          :placeholder="$t('common.password')"
          class="input input-bordered w-full"
        />
      </div>
    </form>
    <div class="flex mt-6">
      <button class="btn btn-primary flex-1" @click="register">{{ $t('common.register') }}</button>
    </div>
    <!-- google auth button -->
    <div class="flex mt-6">
      <button class="btn btn-neutral flex-1" @click="loginGoogle">
        <font-awesome-icon icon="fa-brands fa-google" />
        {{ $t('common.register_with_google') }}
      </button>
    </div>
    <div class="divider"></div>
  </div>
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
      confirmPassword: '',
      email: '',
      error: '',
      authStore: null,
    }
  },

  mounted() {
    this.authStore = useAuthStore()

    const access = this.$route.query.access_token
    const refresh = this.$route.query.refresh_token

    if (access && refresh) {
      this.authStore.setAuthData(access, refresh)
      this.$router.replace('/system')
    }
  },

  methods: {
    async register() {
      this.error = ''

      if (!this.username || !this.password || !this.confirmPassword || !this.email) {
        this.error = 'All fields are required'
        return
      }

      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }

      if (this.password.length < 8 || this.confirmPassword.length < 8) {
        this.error = 'Password must be at least 8 characters long'
        return
      }

      try {
        await this.authStore.register(this.username, this.email, this.password)
        this.$router.push('/system')
      } catch (err) {
        console.error(err)
        if (err.response?.data?.detail) {
          this.error = err.response.data.detail
        } else if (typeof err === 'string') {
          this.error = err
        } else {
          this.error = 'Registration failed'
        }
      }
    },

    loginGoogle() {
      window.location.href = api.defaults.baseURL + API_ENDPOINTS.GOOGLE_LOGIN
    },
  },
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
