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

    <!-- Modals for changing username, email, password -->
    <UsernameModal v-model="openUsernameModal" :error="error" @submit="submitUsernameChange" />

    <EmailChangeModal v-model="openEmailModal" :error="error" @submit="submitEmailChange" />

    <BlockMeModal v-model="openBlockModal" :error="error" @submit="submitBlockMe" />

    <PasswordChangeModal
      v-model="openPasswordModal"
      :error="error"
      @submit="submitPasswordChange"
    />
  </div>
  <!-- Loading screen while user data is not loaded -->
  <LoadingScreen v-if="taskStore.loading || userStore.loading"></LoadingScreen>
</template>

<script>
import ProfileHeader from './ProfileHeader.vue'
import UserInfoCard from './UserInfoCard.vue'
import UserProgressCard from './UserProgressCard.vue'
import UserModificationCard from './UserModificationCard.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

import { useUserStore } from '@/stores/user'
import { useAdminStore } from '@/stores/admin'
import { usePrivateTasksStore } from '@/stores/privateTasks'
import { useEventsStore } from '@/stores/events'
import { useEventParticipantsStore } from '@/stores/eventParticipants'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'
import { useKanbanTasksStore } from '@/stores/kanban/kanbanTasks'
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import { useWorkspaceProjectStagesStore } from '@/stores/workspace/projectStages'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useWorkspaceProjectsTasksStore } from '@/stores/workspace/projectsTasks'
import { useSelectedProjectStore } from '@/stores/selectedProject'
import { useAuthStore } from '@/stores/auth'
import { useVisitsStore } from '@/stores/visits'
import { useNewsStore } from '@/stores/news'
import { useExpenseStore } from '@/stores/expense'
import { useBudgetStore } from '@/stores/budget'
import { usePaymentStore } from '@/stores/payment'

import UsernameModal from './modals/UsernameModal.vue'
import EmailChangeModal from './modals/EmailChangeModal.vue'
import PasswordChangeModal from './modals/PasswordChangeModal.vue'
import BlockMeModal from './modals/BlockMeModal.vue'

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
    BlockMeModal,
  },

  data() {
    return {
      // Modal open states
      openUsernameModal: false,
      openEmailModal: false,
      openPasswordModal: false,
      openBlockModal: false,

      taskStore: usePrivateTasksStore(),
      adminStore: useAdminStore(),
      eventsStore: useEventsStore(),
      eventParticipantsStore: useEventParticipantsStore(),
      kanbanBoardStore: useKanbanBoardStore(),
      kanbanMembersStore: useKanbanMembersStore(),
      kanbanStagesStore: useKanbanStagesStore(),
      kanbanTasksStore: useKanbanTasksStore(),
      workspaceProjectMembersStore: useWorkspaceProjectMembersStore(),
      workspaceProjectStagesStore: useWorkspaceProjectStagesStore(),
      workspaceProjectsStore: useWorkspaceProjectsStore(),
      workspaceProjectsTasksStore: useWorkspaceProjectsTasksStore(),
      selectedProjectStore: useSelectedProjectStore(),
      authStore: useAuthStore(),
      visitsStore: useVisitsStore(),
      newsStore: useNewsStore(),
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
          value: this.taskStore.tasksKpi.totalCompletedTasks || 0,
          max: this.taskStore.tasksKpi.totalTasks || 0,
          percent: Math.round(
            (this.taskStore.tasksKpi.totalCompletedTasks / this.taskStore.tasksKpi.totalTasks) *
              100 || 0,
          ),
          colorClass: 'text-success',
          progressClass: 'progress-success',
        },
        {
          title: this.$t('cabinet.profile.kpi.month_tasks'),
          value: this.taskStore.tasksKpi.totalInMonthCompleted || 0,
          max: this.taskStore.tasksKpi.totalInMonth || 0,
          percent: Math.round(
            (this.taskStore.tasksKpi.totalInMonthCompleted / this.taskStore.tasksKpi.totalInMonth) *
              100 || 0,
          ),
          colorClass: 'text-primary',
          progressClass: 'progress-primary',
        },
        {
          title: this.$t('cabinet.profile.kpi.week_activity'),
          value: this.visitsStore.visits.active_days || 0,
          max: 7,
          percent: Math.round((this.visitsStore.visits.active_days / 7) * 100 || 0),
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
        { key: 'block', title: this.$t('cabinet.profile.actions.block_me') },
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
        case 'block':
          this.openBlockModal = false
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
        case 'block':
          this.openBlockModal = true
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

    // Block user
    async submitBlockMe() {
      try {
        await this.adminStore.changeMyActivity()
        this.openBlockModal = false

        await this.authStore.logout()

        // Reset every store
        this.taskStore.$reset()
        this.adminStore.$reset()
        this.eventsStore.$reset()
        this.eventParticipantsStore.$reset()
        this.kanbanBoardStore.$reset()
        this.kanbanMembersStore.$reset()
        this.kanbanStagesStore.$reset()
        this.kanbanTasksStore.$reset()
        this.workspaceProjectMembersStore.$reset()
        this.workspaceProjectStagesStore.$reset()
        this.workspaceProjectsStore.$reset()
        this.workspaceProjectsTasksStore.$reset()
        this.selectedProjectStore.$reset()
        this.userStore.$reset()
        this.newsStore.$reset()
        this.visitsStore.$reset()
        this.expenseStore.$reset()
        this.budgetStore.$reset()
        this.paymentStore.$reset()

        this.$router.push({ name: 'logout' })
      } catch (err) {
        console.error('Failed to block user:', err)
      }
    },
  },

  // Fetch current user on mount
  async mounted() {
    if (!this.userStore.user) {
      await this.userStore.fetchMe()
    }

    await this.taskStore.fetchTasksAll()
    await this.taskStore.fetchTasksAllCompleted()
    await this.taskStore.fetchTasksAllInMonth()
    await this.taskStore.fetchTasksAllCompletedInMonth()
    await this.visitsStore.getWeekStats()
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
