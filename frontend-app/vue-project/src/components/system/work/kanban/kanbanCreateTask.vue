<template>
  <div class="w-full bg-base-100 border border-base-300 flex items-center justify-center p-1">
    <button
      class="btn btn-primary btn-sm w-full"
      @click="openCreateModal"
      :disabled="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'viewer'"
    >
      <font-awesome-icon icon="fa-solid fa-plus" /> {{ $t('work.kanban.controls.create_task') }}
    </button>

    <!-- Create Task Dialog -->
    <BaseDialog
      v-model="createModal"
      :title="$t('work.kanban.modals.create_task.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmCreateTask"
      @cancel="closeCreateModal"
    >
      <div class="w-full flex flex-col gap-2">
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <label for="taskTitle" class="label">
          {{ $t('work.kanban.modals.create_task.title_name') }}
        </label>
        <input
          type="text"
          class="input w-full mb-2"
          v-model="newTaskTitle"
          :placeholder="$t('work.kanban.modals.create_task.title_name_placeholder')"
        />
        <label for="taskDescription" class="label">
          {{ $t('work.kanban.modals.create_task.description_name') }}
        </label>
        <textarea
          class="textarea w-full"
          maxlength="200"
          v-model="newTaskDescription"
          :placeholder="$t('work.kanban.modals.create_task.description_name_placeholder')"
        ></textarea>
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanTasksStore } from '@/stores/kanban/kanbanTasks'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'

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
      kanbanMembersStore: useKanbanMembersStore(),
    }
  },
  methods: {
    closeCreateModal() {
      this.newTaskTitle = ''
      this.newTaskDescription = ''
      this.tasksStore.clearError()
      this.createModal = false
    },
    openCreateModal() {
      this.newTaskTitle = ''
      this.newTaskDescription = ''
      this.createModal = true
    },
    async confirmCreateTask() {
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
  computed: {
    error() {
      return this.tasksStore.error
    },
  },
}
</script>

<style scoped></style>
