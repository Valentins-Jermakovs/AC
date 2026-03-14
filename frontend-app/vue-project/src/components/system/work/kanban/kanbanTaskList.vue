<template>
  <div class="flex flex-col gap-2 p-1 bg-base-200 border border-base-300">
    <kanban-task v-for="task in tasks" :key="task.id" :task="task"></kanban-task>
  </div>
</template>

<script>
import { useKanbanTasksStore } from '@/stores/kanban/kanbanTasks'
import kanbanTask from './kanbanTask.vue'

export default {
  name: 'KanbanTaskList',
  components: { kanbanTask },
  props: {
    stageId: { type: String, required: true },
    boardId: { type: String, required: true },
  },
  data() {
    return {
      tasks: [],
      tasksStore: useKanbanTasksStore(),
    }
  },
  methods: {
    async loadTasks() {
      if (!this.stageId || !this.boardId) return
      this.tasksStore.stageId = this.stageId
      this.tasksStore.boardId = this.boardId
      await this.tasksStore.getKanbanTasks()
      this.tasks = [...this.tasksStore.tasks]
    }
  },
  mounted() {
    this.loadTasks()
  },
  watch: {
    stageId: 'loadTasks',
    boardId: 'loadTasks',
  },
}
</script>