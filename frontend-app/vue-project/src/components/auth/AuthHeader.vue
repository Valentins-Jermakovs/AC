<template>
  <!-- Login and registration header -->
  <!-- if login -->
  <div v-if="isLogin" class="mb-4 mt-5">
    <h1 class="text-2xl">{{ $t('auth.login.title') }}</h1>
  </div>
  <!-- if registration -->
  <div v-if="isRegister" class="mb-4 mt-5">
    <h1 class="text-2xl">{{ $t('auth.register.title') }}</h1>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

export default {
  setup() {
    const route = useRoute()

    const isLogin = computed(() => route.name === 'login')
    const isRegister = computed(() => route.name === 'register')

    return {
      isLogin,
      isRegister,
    }
  },
}
</script>

<style scoped></style>
