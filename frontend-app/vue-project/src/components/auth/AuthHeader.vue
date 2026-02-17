<template>
  <!-- Show page header depending on the current route -->

  <!-- If the user is on the login page -->
  <div v-if="isLogin" class="mb-4 mt-5">
    <h1 class="text-2xl">{{ $t('auth.login.title') }}</h1>
  </div>

  <!-- If the user is on the registration page -->
  <div v-if="isRegister" class="mb-4 mt-5">
    <h1 class="text-2xl">{{ $t('auth.register.title') }}</h1>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'

export default {
  name: 'AuthHeader',

  data() {
    return {
      route: useRoute(), // store current route
    }
  },

  computed: {
    // Check if current route is login page
    isLogin() {
      return this.route.name === 'login'
    },

    // Check if current route is register page
    isRegister() {
      return this.route.name === 'register'
    },
  },
}
</script>

<style scoped></style>
