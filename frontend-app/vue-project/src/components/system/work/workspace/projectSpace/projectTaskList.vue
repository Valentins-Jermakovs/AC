<template>
  <div class="p-2 flex flex-col items-center bg-base-200 rounded-box border border-base-300">
    
    <ProjectTask
      v-for="task in tasksStore.getTasksByStage(stage.id)"
      :key="task.id"
      :task="task"
    />

    <!-- Create new task -->
    <div class="w-full flex items-center justify-center p-2">
      <button class="btn btn-primary">
        Create new task
      </button>
    </div>

  </div>
</template>

<script>
import ProjectTask from './projectTask.vue'
import { useWorkspaceProjectsTasksStore } from '@/stores/workspace/projectsTasks'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'ProjectTaskList',

  components: {
    ProjectTask
  },

  props: {
    stage: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      tasksStore: useWorkspaceProjectsTasksStore(),
      projectsStore: useWorkspaceProjectsStore()
    }
  },

  mounted() {

  this.tasksStore.projectId =
    this.projectsStore.selectedProject.id

  this.tasksStore.getTasks(
    this.stage.id
  )

}
}
</script>