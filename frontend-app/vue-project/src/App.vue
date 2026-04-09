<template>
  <!-- Global Eye Rest Reminder -->
  <EyeRestReminder />

  <!-- Render child routes -->
  <router-view></router-view>
</template>

<script>
import EyeRestReminder from './components/common/EyeRestReminder.vue'
import { useDocumentTitle } from './utils/useDocumentTitle'
import { useVisitsStore } from './stores/visits';
import { useAuthStore } from './stores/auth';

export default {
  name: 'App', // Component name

  components: {
    EyeRestReminder, // Register EyeRestReminder component
  },
  data() {
    return {
      // Initialize the visit store
      visitStore: useVisitsStore(),

      // Initialize the auth store
      authStore: useAuthStore(),
    }
  },

  // Lifecycle hook: called when component is created
  created() {
    // Call the utility to set the document title
    useDocumentTitle()

    // -----------------------------------
    // If user already logged in, start session
    // -----------------------------------
    if (this.authStore.isAuthenticated) {
      this.visitsStore.registerVisit().catch(console.error)
      this.visitsStore.startSession().catch(console.error)
    }

    // -----------------------------------
    // End session on page/tab close
    // -----------------------------------
    window.addEventListener('beforeunload', async () => {
      try {
        await this.visitsStore.endSession()
      } catch (err) {
        console.warn('Failed to end session on page unload:', err)
      }
    })
  },
}
</script>

<style scoped>
/* No additional CSS needed; all styling handled elsewhere */
</style>
