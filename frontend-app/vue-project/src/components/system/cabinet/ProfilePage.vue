<template>
  <div class="flex flex-col gap-5 p-5">
    <!-- Profile header, shows user info -->
    <ProfileHeader v-if="user" :user="user"></ProfileHeader>

    <!-- Main content: user info, progress, modification actions -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5" v-if="user">
      <UserInfoCard :user="user"></UserInfoCard>

      <div class="flex flex-col gap-5">
        <UserProgressCard
          v-for="(item, index) in progressItems"
          :key="index"
          v-bind="item"
        ></UserProgressCard>
      </div>

      <UserModificationCard
        :actions="actions"
        @action-click="handleActionClick"
      ></UserModificationCard>
    </div>

    <!-- Loading screen while user data is not loaded -->
    <LoadingScreen v-else></LoadingScreen>

    <!-- Modals for changing username, email, password -->
    <UsernameModal 
      v-model="openUsernameModal" 
      :error="error" 
      @submit="submitUsernameChange" 
    />

    <EmailChangeModal 
      v-model="openEmailModal" 
      :error="error" 
      @submit="submitEmailChange" 
    />

    <PasswordChangeModal 
      v-model="openPasswordModal" 
      :error="error" 
      @submit="submitPasswordChange" 
    />
  </div>
</template>

<script>
import ProfileHeader from './ProfileHeader.vue'
import UserInfoCard from './UserInfoCard.vue'
import UserProgressCard from './UserProgressCard.vue'
import UserModificationCard from './UserModificationCard.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useUserStore } from '@/stores/user'

import UsernameModal from './modals/UsernameModal.vue'
import EmailChangeModal from './modals/EmailChangeModal.vue'
import PasswordChangeModal from './modals/PasswordChangeModal.vue'

export default {
  name: 'UserProfileView',

  components: {
    ProfileHeader,
    UserInfoCard,
    UserProgressCard,
    UserModificationCard,
    LoadingScreen,

    UsernameModal,
    EmailChangeModal,
    PasswordChangeModal,
  },

  data() {
    return {
      // Modal open states
      openUsernameModal: false,
      openEmailModal: false,
      openPasswordModal: false,
    }
  },

  computed: {
    // Pinia user store
    userStore() {
      return useUserStore()
    },

    // Current user data
    user() {
      return this.userStore.user
    },

    // Error message from store
    error() {
      return this.userStore.error
    },

    // User KPI/progress cards
    progressItems() {
      return [
        {
          title: this.$t('cabinet.profile.kpi.tasks'),
          value: 78,
          max: 100,
          percent: 78,
          colorClass: 'text-success',
          progressClass: 'progress-success',
        },
        {
          title: this.$t('cabinet.profile.kpi.month_tasks'),
          value: 3,
          max: 5,
          percent: 60,
          colorClass: 'text-primary',
          progressClass: 'progress-primary',
        },
        {
          title: this.$t('cabinet.profile.kpi.week_activity'),
          value: 5,
          max: 7,
          percent: 71,
          colorClass: 'text-warning',
          progressClass: 'progress-warning',
        },
      ]
    },

    // Actions available in UserModificationCard
    actions() {
      return [
        { key: 'username', title: this.$t('cabinet.profile.actions.edit_username') },
        { key: 'email', title: this.$t('cabinet.profile.actions.edit_email') },
        { key: 'password', title: this.$t('cabinet.profile.actions.change_password') },
      ]
    },
  },

  methods: {
    // Close modal by type and reset error
    closeModal(modalName) {
      switch (modalName) {
        case 'username':
          this.openUsernameModal = false
          this.userStore.error = ''
          break
        case 'email':
          this.openEmailModal = false
          this.userStore.error = ''
          break
        case 'password':
          this.openPasswordModal = false
          this.userStore.error = ''
          break
      }
    },

    // Handle action button click to open modal
    handleActionClick(key) {
      switch (key) {
        case 'username':
          this.openUsernameModal = true
          this.userStore.clearError()
          break
        case 'email':
          this.openEmailModal = true
          this.userStore.clearError()
          break
        case 'password':
          this.openPasswordModal = true
          this.userStore.clearError()
          break
      }
    },

    // Submit username change
    async submitUsernameChange(username) {
      if (!username) return
      try {
        await this.userStore.changeUsername(username)
        this.openUsernameModal = false
      } catch (err) {
        console.error('Failed to change username:', err)
      }
    },

    // Submit email change
    async submitEmailChange(email) {
      if (!email) return
      try {
        await this.userStore.changeEmail(email)
        this.openEmailModal = false
      } catch (err) {
        console.error('Failed to change email:', err)
      }
    },

    // Submit password change
    async submitPasswordChange({ oldPassword, newPassword }) {
      if (!oldPassword || !newPassword) return
      try {
        await this.userStore.changePassword(newPassword, oldPassword)
        this.openPasswordModal = false
      } catch (err) {
        console.error('Failed to change password:', err)
      }
    },
  },

  // Fetch current user on mount
  mounted() {
    if (!this.userStore.user) {
      this.userStore.fetchMe()
    }
  },
}
</script>

<style scoped>
/* Error slide animation for modals */
.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 100px;
}
</style>
