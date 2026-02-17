<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>
  <AdminPage v-if="activePage === 'admin' && userStore.isAdmin"></AdminPage>
  <ProfilePage v-if="activePage === 'profile'"></ProfilePage>
  <LoadingScreen v-if="!userStore.user"></LoadingScreen>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue'
import headerImage from '@/assets/images/mike-hindle-a8Slhd4Kvxw-unsplash.jpg'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'
import ProfilePage from '@/components/system/cabinet/ProfilePage.vue'

import { useUserStore } from '@/stores/user'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import AdminPage from '@/components/system/cabinet/AdminPage.vue'

export default {
  name: 'CabinetView',
  components: {
    PageHeader,
    NavigationPanel,
    ProfilePage,
    LoadingScreen,
    AdminPage,
  },

  data() {
    return {
      image: headerImage,
      activePage: 'dashboard',
    }
  },

  computed: {
    userStore() {
      return useUserStore()
    },
    title() {
      return this.$t('cabinet.title')
    },
    navButtons() {
      let navButtons = [
        { key: 'dashboard', title: this.$t('cabinet.nav_bar.dashboard') },
        { key: 'profile', title: this.$t('cabinet.nav_bar.profile') },
      ]

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
    if (!this.userStore.user) {
      this.userStore.fetchMe()
    }
  },
}
</script>

<style scoped></style>
