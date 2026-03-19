<template>
  <!-- Projects list -->
  <div
    class="w-full h-full flex items-center justify-center p-2"
    v-if="projectsStore.selectedProject == null"
  >
    <div class="w-4/5 h-full flex flex-col bg-base-200 border border-base-300">
      <!-- Top bar -->
      <TopBar></TopBar>
      <!-- List -->
      <ProjectsList v-if="projectsStore.hasProjects"></ProjectsList>
      <!-- Empty list -->
      <EmptyProjectsList v-else></EmptyProjectsList>
      <!-- Footer -->
      <ProjectsFooter></ProjectsFooter>
      <LoadingScreen v-if="projectsStore.loading"></LoadingScreen>
    </div>
  </div>
  <!-- The selected project -->
  <div class="w-full h-full flex flex-col items-center" v-if="projectsStore.selectedProject">
    <!-- Top bar -->
    <ProjectTitle></ProjectTitle>
    <!-- navigation butttons -->
    <ProjectControls v-model:activeView="activeView" />

    <!-- project view -->
    <!-- List of stages -->
    <!-- Project view -->
    <div v-if="this.activeView === 'project'" class="w-full">
      <ProjectStageList></ProjectStageList>
    </div>

    <!-- Members view -->
    <div v-if="this.activeView === 'members'">
      <h2>Members</h2>
    </div>
  </div>
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import EmptyProjectsList from './workspace/emptyProjectsList.vue'
import ProjectsFooter from './workspace/projectsFooter.vue'
import ProjectsList from './workspace/projectsList.vue'
import TopBar from './workspace/topBar.vue'

import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import ProjectTitle from './workspace/projectSpace/projectTitle.vue'
import ProjectControls from './workspace/projectSpace/projectControls.vue'
import ProjectStageList from './workspace/projectSpace/projectStageList.vue'

export default {
  name: 'ProjectsPage',
  components: {
    TopBar, // Top navigation bar
    ProjectsFooter,
    ProjectsList,
    EmptyProjectsList,
    LoadingScreen,
    ProjectTitle,
    ProjectControls,
    ProjectStageList,
  },

  data() {
    return {
      projectsStore: useWorkspaceProjectsStore(),
      activeView: 'project',
    }
  },

  mounted() {
    this.projectsStore.getAllProjects()
  },
}
</script>

<style scoped></style>
