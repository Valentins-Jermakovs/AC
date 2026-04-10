<template>
  <!-- Top navigation bar -->
  <div
    class="flex w-full h-full bg-base-200 items-center justify-between py-2 pr-2 pl-1 border border-base-300"
  >
    <!-- LEFT SECTION: Burger button (toggle sidebar) + logo -->
    <div class="flex items-center gap-4 pl-1">
      <BurgerButton />
      <Logo />
    </div>

    <!-- CENTER SECTION: Date & Time (visible on large screens only) -->
    <div class="hidden lg:flex gap-3 rounded-field bg-base-200 font-semibold">
      <h1>{{ date }}</h1>
      <h1>{{ time }}</h1>
    </div>

    <!-- RIGHT SECTION: Top buttons for modals -->
    <div class="flex">
      <TopButton
        v-for="(item, index) in navigation"
        :key="index"
        :icon="item.icon"
        @click="openModal(item.modal)"
      />
    </div>

    <!-- MODALS: Email, Language, Support, Logout -->
    <EmailModal :modelValue="activeModal === 'email'" @update:modelValue="activeModal = null" />

    <LanguageModal
      :modelValue="activeModal === 'language'"
      @update:modelValue="activeModal = null"
    />

    <SupportModal :modelValue="activeModal === 'support'" @update:modelValue="activeModal = null" />

    <LogoutModal
      :modelValue="activeModal === 'logout'"
      @update:modelValue="activeModal = null"
      @confirm="handleLogout"
    />
  </div>
</template>

<script>
// Import Vue features
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

// Import stores
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
import { useNewsStore } from '@/stores/news'
import { useVisitsStore } from '@/stores/visits'

// Import components
import BurgerButton from './BurgerButton.vue'
import Logo from './ProjectLogo.vue'
import TopButton from './TopButton.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'

// Import modals
import EmailModal from './modals/EmailModal.vue'
import LanguageModal from './modals/LanguageModal.vue'
import SupportModal from './modals/SupportModal.vue'
import LogoutModal from './modals/LogoutModal.vue'

export default {
  name: 'TopBar',

  // Register child components
  components: {
    BurgerButton,
    Logo,
    TopButton,
    BaseDialog,
    EmailModal,
    LanguageModal,
    SupportModal,
    LogoutModal,
  },

  data() {
    return {
      activeModal: null, // Currently active modal

      date: new Date().toLocaleDateString(), // Current date
      time: '', // Current time, updated every second

      // Top buttons configuration: icon + modal to open
      navigation: [
        { icon: 'fa-solid fa-envelope', modal: 'email' },
        { icon: 'fa-solid fa-globe', modal: 'language' },
        { icon: 'fa-solid fa-question-circle', modal: 'support' },
        { icon: 'fa-solid fa-circle-xmark', modal: 'logout' },
      ],

      timerId: null, // Interval ID for updating time
    }
  },

  setup() {
    // Composables
    const { locale } = useI18n({ useScope: 'global' }) // For internationalization
    const router = useRouter()
    const authStore = useAuthStore()

    return { locale, router, authStore }
  },

  methods: {
    // Open a modal by setting activeModal
    openModal(modalName) {
      this.activeModal = modalName
    },

    // Handle logout: call auth store, reset all stores, redirect
    async handleLogout() {
      try {
        await this.authStore.logout()

        const userStore = useUserStore()
        const authStore = useAuthStore()
        const adminStore = useAdminStore()
        const privateTasksStore = usePrivateTasksStore()
        const eventsStore = useEventsStore()
        const eventParticipantsStore = useEventParticipantsStore()
        const kanbanBoardStore = useKanbanBoardStore()
        const kanbanMembersStore = useKanbanMembersStore()
        const kanbanStagesStore = useKanbanStagesStore()
        const kanbanTasksStore = useKanbanTasksStore()
        const workspaceProjectMembersStore = useWorkspaceProjectMembersStore()
        const workspaceProjectStagesStore = useWorkspaceProjectStagesStore()
        const workspaceProjectsStore = useWorkspaceProjectsStore()
        const workspaceProjectsTasksStore = useWorkspaceProjectsTasksStore()
        const selectedProjectStore = useSelectedProjectStore()
        const newsStore = useNewsStore()
        const visitsStore = useVisitsStore()

        // Reset all stores
        privateTasksStore.$reset()
        eventsStore.$reset()
        eventParticipantsStore.$reset()
        kanbanBoardStore.$reset()
        kanbanMembersStore.$reset()
        kanbanStagesStore.$reset()
        kanbanTasksStore.$reset()
        workspaceProjectMembersStore.$reset()
        workspaceProjectStagesStore.$reset()
        workspaceProjectsStore.$reset()
        workspaceProjectsTasksStore.$reset()
        selectedProjectStore.$reset()
        newsStore.$reset()
        visitsStore.$reset()

        // Reset all stores
        userStore.$reset()
        authStore.$reset()
        adminStore.$reset()
      } finally {
        this.activeModal = null
        this.router.push({ name: 'logout' }) // Redirect to logout page
      }
    },

    // Update the time every second
    updateTime() {
      this.time = new Date().toLocaleTimeString().slice(0, -3) // Format HH:MM
    },
  },

  mounted() {
    this.updateTime() // Set initial time
    this.timerId = setInterval(this.updateTime, 1000) // Update every second
  },

  beforeUnmount() {
    // Clear interval when component is destroyed
    if (this.timerId) clearInterval(this.timerId)
  },
}
</script>

<style scoped>
/* Scoped styles for TopBar (currently empty) */
</style>
