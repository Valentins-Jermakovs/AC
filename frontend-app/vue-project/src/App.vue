<template>
  <!-- Global Eye Rest Reminder -->
  <EyeRestReminder />

  <!-- Render child routes -->
  <router-view></router-view>
</template>

<script>
import EyeRestReminder from './components/common/EyeRestReminder.vue'
import { useDocumentTitle } from './utils/useDocumentTitle'

export default {
  name: 'App', // Component name

  components: {
    EyeRestReminder, // Register EyeRestReminder component
  },

  // Lifecycle hook: called when component is created
  created() {
    // Call the utility to set the document title
    useDocumentTitle()
  },
}
</script>

<style scoped>
/* No additional CSS needed; all styling handled elsewhere */
</style>
