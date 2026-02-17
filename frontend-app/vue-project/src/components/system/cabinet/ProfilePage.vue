<template>
  <div class="flex flex-col gap-5 p-5">
    <ProfileHeader v-if="user" :user="user"></ProfileHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5" v-if="user">
      <UserInfoCard :user="user"></UserInfoCard>

      <div class="flex flex-col gap-5">
        <UserProgressCard v-for="(item, index) in progressItems" :key="index" v-bind="item"></UserProgressCard>
      </div>

      <UserModificationCard :actions="actions" @action-click="handleActionClick"></UserModificationCard>
    </div>

    <LoadingScreen v-else></LoadingScreen>

    <!-- Modals -->
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
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useUserStore } from '@/stores/user'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

import UsernameModal from './modals/UsernameModal.vue'
import EmailChangeModal from './modals/EmailChangeModal.vue'
import PasswordChangeModal from './modals/PasswordChangeModal.vue'

export default {
  name: 'UserProfileView',

  data() {
    return {
      openUsernameModal: false,
      openEmailModal: false,
      openPasswordModal: false,
    }
  },

  components: {
    ProfileHeader,
    UserInfoCard,
    UserProgressCard,
    UserModificationCard,
    BaseDialog,
    LoadingScreen,

    UsernameModal,
    EmailChangeModal,
    PasswordChangeModal,
  },

  computed: {
    user() {
      return this.userStore.user
    },

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

    userStore() {
      return useUserStore()
    },
    error() {
      return this.userStore.error
    },

    actions() {
      return [
        { key: 'username', title: this.$t('cabinet.profile.actions.edit_username') },
        { key: 'email', title: this.$t('cabinet.profile.actions.edit_email') },
        { key: 'password', title: this.$t('cabinet.profile.actions.change_password') },
      ]
    },
  },

  methods: {
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
        default:
          break
      }
    },
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
    async submitUsernameChange(username) {
      if (!username) return

      try {
        await this.userStore.changeUsername(username)
        this.openUsernameModal = false
      } catch (err) {
        console.error('Failed to change username:', err)
      }
    },
    async submitEmailChange(email) {
      if (!email) return

      try {
        await this.userStore.changeEmail(email)
        this.openEmailModal = false
      } catch (err) {
        console.error('Failed to change email:', err)
      }
    },
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

  mounted() {
    if (!this.userStore.user) {
      this.userStore.fetchMe()
    }
  },
}
</script>

<style scoped>
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
