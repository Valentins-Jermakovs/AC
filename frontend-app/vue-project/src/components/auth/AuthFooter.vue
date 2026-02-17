<template>
  <!-- Show navigation link depending on current page -->
  
  <!-- If the user is on login page, show link to register -->
  <div v-if="isLogin">
    <h3>
      {{ $t('common.switch_to_register') }}
      <router-link to="/register" class="link link-hover link-primary underline">
        {{ $t('common.register') }}
      </router-link>
    </h3>
  </div>

  <!-- If the user is on register page, show link to login -->
  <div v-if="isRegister">
    <h3>
      {{ $t('common.switch_to_login') }}
      <router-link to="/login" class="link link-hover link-primary underline">
        {{ $t('common.login') }}
      </router-link>
    </h3>
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
    // Check if the current route is login
    isLogin() {
      return this.route.name === 'login'
    },

    // Check if the current route is register
    isRegister() {
      return this.route.name === 'register'
    },
  },
}
</script>


<style scoped></style>
