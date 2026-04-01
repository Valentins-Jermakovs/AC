<template>
  <div class="w-full p-1 bg-base-100 border border-base-300 text-2xl pl-5">
    <h1>{{ title }}</h1>
  </div>
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'ProjectTitle',
  data() {
    return {
      projectsStore: useWorkspaceProjectsStore(),
    }
  },
  computed: {
    title() {
      return this.projectsStore.selectedProject.title
    },
  },
}
</script>

<style scoped></style>
