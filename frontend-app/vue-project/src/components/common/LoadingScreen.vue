<template>
  <!-- Full-screen loading overlay -->
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-base-100/80 backdrop-blur-sm">
    <!-- Spinner -->
    <span class="loading loading-spinner loading-lg text-primary"></span>
  </div>
</template>

<script>
export default {
  name: 'LoadingOverlay', // Component name
}
</script>

<style scoped>
/* No additional styles needed since Tailwind classes are used */
</style>
