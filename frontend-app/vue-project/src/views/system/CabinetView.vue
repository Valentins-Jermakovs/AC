<template>
  <!-- Page header with title and background image -->
  <PageHeader :title="title" :imageUrl="image"></PageHeader>

  <!-- Navigation panel with buttons.
    v-model controls which page is currently active 
  -->
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>

  <!-- Show Admin page only if:
    1) Active page is "admin"
    2) User has admin rights 
  -->
  <AdminPage
    v-if="activePage === 'admin' && userStore.isAdmin">
  </AdminPage>

  <!-- Show Profile page if active page is "profile" -->
  <ProfilePage
    v-if="activePage === 'profile'">
  </ProfilePage>

  <!-- Show loading screen if user data is not loaded yet -->
  <LoadingScreen
    v-if="!userStore.user">
  </LoadingScreen>
</template>

<script>
// Import UI components
import PageHeader from '@/components/ui/PageHeader.vue'
import headerImage from '@/assets/images/mike-hindle-a8Slhd4Kvxw-unsplash.jpg'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'

// Import pages
import ProfilePage from '@/components/system/cabinet/ProfilePage.vue'
import AdminPage from '@/components/system/cabinet/AdminPage.vue'

// Import loading component
import LoadingScreen from '@/components/common/LoadingScreen.vue'

// Import Pinia user store
import { useUserStore } from '@/stores/user'

export default {
  name: 'CabinetView',

  // Register components
  components: {
    PageHeader,
    NavigationPanel,
    ProfilePage,
    LoadingScreen,
    AdminPage,
  },

  data() {
    return {
      // Background image for header
      image: headerImage,

      // Currently active page (default is dashboard)
      activePage: 'dashboard',
    }
  },

  computed: {
    // Access user store
    userStore() {
      return useUserStore()
    },

    // Page title from translations
    title() {
      return this.$t('cabinet.title')
    },

    // Navigation buttons for NavigationPanel
    navButtons() {
      // Basic navigation buttons
      let navButtons = [
        {
          key: 'dashboard',
          title: this.$t('cabinet.nav_bar.dashboard'),
        },
        {
          key: 'profile',
          title: this.$t('cabinet.nav_bar.profile'),
        },
      ]

      // Add Admin button only if user is admin
      if (this.userStore.isAdmin) {
        navButtons.push({
          key: 'admin',
          title: this.$t('cabinet.nav_bar.admin'),
        })
      }

      return navButtons
    },
  },

  mounted() {
    // When component is loaded:
    // If user data is not available, fetch it from API
    if (!this.userStore.user) {
      this.userStore.fetchMe()
    }
  },
}
</script>

<style scoped>
/* Scoped styles for this component (currently empty) */
</style>
