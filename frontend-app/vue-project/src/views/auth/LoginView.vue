<template>
  <!-- Main layout for authentication pages (common structure and styling) -->
  <AuthLayout>

    <!-- Header section (title, logo, or welcome text) -->
    <AuthHeader></AuthHeader>

    <!-- Login form where user enters email and password -->
    <LoginForm></LoginForm>

    <!-- Footer section (links like register, forgot password, etc.) -->
    <AuthFooter></AuthFooter>

  </AuthLayout>
</template>

<script>
// Import layout used for authentication pages
import AuthLayout from '@/layouts/AuthLayout.vue'

// Import auth components
import AuthHeader from '@/components/auth/AuthHeader.vue'
import LoginForm from '@/components/auth/LoginForm.vue'
import AuthFooter from '@/components/auth/AuthFooter.vue'

export default {
  name: 'LoginView', // Component name

  // Register child components
  components: {
    AuthFooter,
    AuthHeader,
    LoginForm,
    AuthLayout,
  },
}
</script>

<style scoped>
/* Scoped styles for this page (currently empty) */
</style>
