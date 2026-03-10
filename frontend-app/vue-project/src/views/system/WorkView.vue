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
import headerImage from '@/assets/images/jakub-zerdzicki-POjPlQ8STls-unsplash.jpg'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'

// Import pages
import PrivateTasksPage from '@/components/system/work/PrivateTasksPage.vue'
import KanbanPage from '@/components/system/work/KanbanPage.vue'
import ProjectsPage from '@/components/system/work/ProjectsPage.vue'

// Import loading component
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'WorkView',

  // Register components
  components: {
    PageHeader,
    NavigationPanel,
    LoadingScreen,
    PrivateTasksPage,
    KanbanPage,
    ProjectsPage
  },

  data() {
    return {
      // Background image for header
      image: headerImage,

      // Currently active page (default is private tasks)
      activePage: 'private-tasks',
    }
  },

  computed: {
    title() {
      return "Work"
    },

    // Navigation buttons for NavigationPanel
    navButtons() {
      // Basic navigation buttons
      let navButtons = [
        {
          key: 'private-tasks',
          title: 'Private Tasks',
        },
        {
          key: 'kanban',
          title: 'Kanban',
        },
        {
          key: 'projects',
          title: 'Projects',
        }
      ]

      return navButtons
    },
  }
}
</script>

<style scoped></style>
