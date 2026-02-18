<template>
  <!-- Main layout for authentication pages (centered content, styling, etc.) -->
  <AuthLayout>

    <!-- Header section (usually contains title or logo) -->
    <AuthHeader></AuthHeader>

    <!-- Registration form where user creates a new account -->
    <RegisterForm></RegisterForm>

    <!-- Footer section (links, additional info, etc.) -->
    <AuthFooter></AuthFooter>

  </AuthLayout>
</template>

<script>
// Import layout for auth pages
import AuthLayout from '@/layouts/AuthLayout.vue'

// Import auth page components
import AuthHeader from '@/components/auth/AuthHeader.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'
import AuthFooter from '@/components/auth/AuthFooter.vue'

export default {
  name: 'RegisterView', // Component name

  // Register child components
  components: {
    AuthFooter,
    AuthHeader,
    RegisterForm,
    AuthLayout,
  },
}
</script>

<style scoped>
/* Scoped styles for this page (currently empty) */
</style>
