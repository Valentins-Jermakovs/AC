<template>
  <div class="w-full bg-base-100 border border-base-300 flex items-center justify-center p-1">
    <button class="btn btn-primary btn-sm w-full" @click="openCreateModal">+ Create task</button>

    <!-- Create Task Dialog -->
    <BaseDialog
      v-model="createModal"
      title="Create Task"
      confirmText="Create"
      cancelText="Cancel"
      @confirm="confirmCreateTask"
    >
      <div class="w-full flex flex-col gap-2">
        <label for="taskTitle" class="label">Task Title</label>
        <input
          type="text"
          class="input w-full mb-2"
          v-model="newTaskTitle"
          placeholder="Task title"
        />
        <label for="taskDescription" class="label">Task Description</label>
        <textarea
          class="textarea w-full"
          v-model="newTaskDescription"
          placeholder="Task description"
        ></textarea>
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanTasksStore } from '@/stores/kanban/kanbanTasks'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'

export default {
  name: 'kanbanCreateTask',
  components: { BaseDialog },
  props: {
    stageId: { type: String, required: true },
    boardId: { type: String, required: true },
  },
  data() {
    return {
      createModal: false,
      newTaskTitle: '',
      newTaskDescription: '',
      tasksStore: useKanbanTasksStore(),
      kanbanStore: useKanbanBoardStore(),
    }
  },
  methods: {
    openCreateModal() {
      this.newTaskTitle = ''
      this.newTaskDescription = ''
      this.createModal = true
    },
    async confirmCreateTask() {
      if (!this.newTaskTitle.trim()) return

      try {
        await this.tasksStore.createKanbanTask({
          boardId: this.boardId,
          stageId: this.stageId,
          title: this.newTaskTitle.trim(),
          description: this.newTaskDescription.trim(),
        })

        // Atsvaidzini UI – izmet eventu vecākai komponentei
        this.$emit('task-created')

        this.createModal = false
        this.newTaskTitle = ''
        this.newTaskDescription = ''
      } catch (err) {
        console.error('Failed to create task:', err)
      }
    },
  },
}
</script>

<style scoped></style>
