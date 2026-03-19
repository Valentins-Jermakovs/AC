<template>
  <div class="w-full h-full flex items-center justify-center p-2">
    <div class="w-4/5 h-full flex flex-col bg-base-200 border border-base-300">
      <!-- Top bar -->
      <TopBar></TopBar>
      <!-- List -->
      <ProjectsList></ProjectsList>
      <!-- Empty list -->
      <!-- <EmptyProjectsList></EmptyProjectsList> -->
      <!-- Footer -->
      <ProjectsFooter></ProjectsFooter>
    </div>
  </div>
</template>

<script>
import EmptyProjectsList from './workspace/emptyProjectsList.vue';
import ProjectsFooter from './workspace/projectsFooter.vue';
import ProjectsList from './workspace/projectsList.vue';
import TopBar from './workspace/topBar.vue';


export default {
  name: 'ProjectsPage',
  components: {
    TopBar, // Top navigation bar
    ProjectsFooter,
    ProjectsList,
    EmptyProjectsList
  },
}
</script>

<style scoped></style>
