<template>
  <div class="w-full flex justify-center">
    <div class="w-4/5 bg-base-200 border border-base-300 p-1 mt-10">
      <ProjectStage
        v-for="stage in stagesStore.projectStages"
        :key="stage.id"
        :stage="stage"
        class="mt-5"
      ></ProjectStage>
      <!-- Create new stage -->
      <div class="w-full flex items-center justify-center p-2">
        <button class="btn btn-primary">Create new stage</button>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectStage from './projectStage.vue'
import { useWorkspaceProjectStagesStore } from '@/stores/workspace/projectStages'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'ProjectStageList',
  components: { ProjectStage },

  data() {
    return {
      stagesStore: useWorkspaceProjectStagesStore(),
      projectsStore: useWorkspaceProjectsStore(),
    }
  },

  mounted() {
    this.stagesStore.projectId = this.projectsStore.selectedProject.id
    if (this.stagesStore.projectId) {
      this.stagesStore.getStages()
    }
  },
}
</script>

<style scoped></style>
