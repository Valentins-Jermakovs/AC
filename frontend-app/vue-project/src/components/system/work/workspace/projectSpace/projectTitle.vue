<template>
  <div class="w-full p-1 bg-base-100 border border-base-300 text-2xl pl-5">
    <h1>Project name: {{ projectsStore.selectedProject.title }}</h1>
  </div>
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'ProjectTitle',
  setup() {
    const projectsStore = useWorkspaceProjectsStore()
    return {
      projectsStore,
    }
  },
}
</script>

<style scoped></style>
