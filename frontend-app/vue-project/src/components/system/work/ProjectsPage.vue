<template>
  <div class="w-full h-full flex items-center justify-center p-2">
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
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue';
import EmptyProjectsList from './workspace/emptyProjectsList.vue';
import ProjectsFooter from './workspace/projectsFooter.vue';
import ProjectsList from './workspace/projectsList.vue';
import TopBar from './workspace/topBar.vue';

import { useWorkspaceProjectsStore } from '@/stores/workspace/projects';


export default {
  name: 'ProjectsPage',
  components: {
    TopBar, // Top navigation bar
    ProjectsFooter,
    ProjectsList,
    EmptyProjectsList,
    LoadingScreen
  },

  data() {
    return {
      projectsStore: useWorkspaceProjectsStore(),
    }
  },

  mounted() {
    this.projectsStore.getAllProjects();
  }
}
</script>

<style scoped></style>
