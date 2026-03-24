<template>
  <!-- Page header with title and background image -->
  <PageHeader :title="title" :imageUrl="image"></PageHeader>

  <!-- Navigation panel with buttons.
    v-model controls which page is currently active 
  -->
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>

  <!-- Show PrivateTasksPage only if active page is "private-tasks" -->
  <PrivateTasksPage v-if="activePage === 'private-tasks'"></PrivateTasksPage>
  <!-- Show KanbanPage only if active page is "kanban" -->
  <KanbanPage v-if="activePage === 'kanban'"></KanbanPage>
  <!-- Show ProjectsPage only if active page is "projects" -->
  <ProjectsPage v-if="activePage === 'projects'"></ProjectsPage>
</template>

<script>
// Import UI components
import PageHeader from '@/components/ui/PageHeader.vue'
import headerImage from '@/assets/images/frederic-koberl-RrJCrlU2yZs-unsplash.jpg'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'

// Import pages
import PrivateTasksPage from '@/components/system/work/PrivateTasksPage.vue'
import KanbanPage from '@/components/system/work/KanbanPage.vue'
import ProjectsPage from '@/components/system/work/ProjectsPage.vue'

// Import loading component
import LoadingScreen from '@/components/common/LoadingScreen.vue'

// Import stores
import { usePrivateTasksStore } from '@/stores/privateTasks'

export default {
  name: 'WorkView',

  // Register components
  components: {
    PageHeader,
    NavigationPanel,
    LoadingScreen,
    PrivateTasksPage,
    KanbanPage,
    ProjectsPage,
  },

  data() {
    return {
      // Background image for header
      image: headerImage,

      // Currently active page (default is private tasks)
      activePage: 'private-tasks',

      // Private tasks store
      privateTasksStore: usePrivateTasksStore(),
    }
  },

  computed: {
    title() {
      return this.$t('work.title')
    },

    // Navigation buttons for NavigationPanel
    navButtons() {
      // Basic navigation buttons
      let navButtons = [
        {
          key: 'private-tasks',
          title: this.$t('work.nav_bar.private'),
        },
        {
          key: 'kanban',
          title: this.$t('work.nav_bar.kanban'),
        },
        {
          key: 'projects',
          title: this.$t('work.nav_bar.projects'),
        },
      ]

      return navButtons
    },
  },
}
</script>

<style scoped></style>
