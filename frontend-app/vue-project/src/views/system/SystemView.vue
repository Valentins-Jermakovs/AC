<template>
  <!-- System View renders the main SystemLayout -->
  <SystemLayout></SystemLayout>
</template>

<script>
// Import the layout component
import SystemLayout from '@/layouts/SystemLayout.vue'

export default {
  name: 'SystemView', // Component name

  // Register child components
  components: {
    SystemLayout, // Main system layout
  },
}
</script>

<style scoped>
/* No additional styles; styling handled in the layout or globally */
</style>
