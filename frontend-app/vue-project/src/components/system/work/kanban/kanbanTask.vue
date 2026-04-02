<template>
  <div class="w-full bg-base-100 p-1 border border-base-300">
    <!-- Task title and dropdown menu -->
    <div class="flex flex-col items-center">
      <div class="w-full flex justify-between items-center p-1">
        <h2 class="flex-1">{{ task.title }}</h2>
        <div class="dropdown dropdown-right z-10">
          <button
            tabindex="0"
            role="button"
            class="btn btn-sm btn-ghost"
            :disabled="
              kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'viewer'
            "
          >
            ⋮
          </button>
          <ul
            tabindex="0"
            class="dropdown-content menu bg-base-200 border border-base-300 w-48 p-2 shadow"
          >
            <li>
              <button class="flex gap-2 items-center" @click="openUpdateModal">
                <font-awesome-icon icon="fa-solid fa-pencil" />
                {{ $t('work.kanban.common.update_task') }}
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center" @click="openMoveInStageModal">
                <font-awesome-icon icon="fa-solid fa-arrow-up" />
                {{ $t('work.kanban.common.move_task_in_stage') }}
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center" @click="openMoveBetweenStagesModal">
                <font-awesome-icon icon="fa-solid fa-arrow-right" />
                {{ $t('work.kanban.common.move_task_to_another_stages') }}
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-error" @click="openDeleteModal">
                <font-awesome-icon icon="fa-solid fa-trash" />
                {{ $t('work.kanban.common.delete_task') }}
              </button>
            </li>
          </ul>
        </div>
      </div>
      <div class="w-full p-1">
        <p>{{ task.description }}</p>
      </div>
    </div>

    <!-- BaseDialogs -->
    <BaseDialog
      v-model="updateModal"
      :title="$t('work.kanban.modals.update_task.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmUpdateTask"
      @cancel="closeUpdateModal"
    >
      <div class="w-full flex flex-col gap-2">
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <label for="taskTitle" class="label">
          {{ $t('work.kanban.modals.update_task.title_name') }}
        </label>
        <input
          type="text"
          class="input w-full mb-2"
          v-model="newTaskTitle"
          :placeholder="$t('work.kanban.modals.update_task.title_name_placeholder')"
        />
        <label for="taskDescription" class="label">
          {{ $t('work.kanban.modals.update_task.description_name') }}
        </label>
        <div class="w-full flex justify-end text-sm opacity-70 pr-1">
          {{ descriptionRemainingChars }} / {{ descriptionMaxLength }}
        </div>
        <textarea
          class="input w-full"
          maxlength="1000"
          v-model="newTaskDescription"
          :placeholder="$t('work.kanban.modals.update_task.description_name_placeholder')"
        ></textarea>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="moveInStageModal"
      :title="$t('work.kanban.modals.move_task_in_stage.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmMoveInStage"
    >
      <div class="w-full flex flex-col gap-2">
        <label for="taskTitle" class="label">{{
          $t('work.kanban.modals.move_task_in_stage.name')
        }}</label>
        <select class="select select-bordered w-full" v-model="moveDirection">
          <option value="up">{{ $t('work.kanban.common.directions.up') }}</option>
          <option value="down">{{ $t('work.kanban.common.directions.down') }}</option>
        </select>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="moveBetweenStagesModal"
      :title="$t('work.kanban.modals.move_task_to_another_stages.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmMoveBetweenStages"
    >
      <div class="w-full flex flex-col gap-2">
        <label for="taskTitle" class="label">
          {{ $t('work.kanban.modals.move_task_to_another_stages.name') }}
        </label>
        <select class="select select-bordered w-full" v-model="targetStageId">
          <option v-for="stage in stages" :key="stage.id" :value="stage.id">
            {{ stage.title }}
          </option>
        </select>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="deleteModal"
      :title="$t('work.kanban.modals.delete_task.title')"
      :confirmText="$t('common.delete')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmDeleteTask"
    >
      {{ $t('work.kanban.modals.delete_task.content') }}
    </BaseDialog>
  </div>

  <LoadingScreen v-if="tasksStore.loading"></LoadingScreen>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanTasksStore } from '@/stores/kanban/kanbanTasks'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  props: { task: { type: Object, required: true } },
  components: { BaseDialog, LoadingScreen },
  data() {
    const boardStore = useKanbanBoardStore()
    return {
      tasksStore: useKanbanTasksStore(),
      stagesStore: useKanbanStagesStore(),
      boardStore,
      updateModal: false,
      moveInStageModal: false,
      moveBetweenStagesModal: false,
      deleteModal: false,
      newTaskTitle: '',
      newTaskDescription: '',
      moveDirection: 'up',
      targetStageId: null,
      kanbanMembersStore: useKanbanMembersStore(),
      stages: boardStore.selectedBoard ? [] : [],
      descriptionMaxLength: 1000,
    }
  },
  mounted() {
    if (this.boardStore.selectedBoard) {
      this.stages = this.stagesStore.stages
    }
  },
  methods: {
    async emitReload() {
      this.$emit('task-updated')
    },
    openUpdateModal() {
      this.newTaskTitle = this.task.title
      this.newTaskDescription = this.task.description
      this.updateModal = true
    },
    closeUpdateModal() {
      this.newTaskTitle = ''
      this.newTaskDescription = ''
      this.updateModal = false
      this.kanbanStore.clearError()
    },
    async confirmUpdateTask() {
      try {
        await this.tasksStore.updateKanbanTask({
          boardId: this.boardStore.selectedBoard.id,
          taskId: this.task.id,
          title: this.newTaskTitle,
          description: this.newTaskDescription,
        })
        this.updateModal = false
        this.emitReload()
      } catch (err) {
        console.error('Failed to update task:', err)
      }
    },
    openMoveInStageModal() {
      this.moveDirection = 'up'
      this.moveInStageModal = true
    },
    async confirmMoveInStage() {
      try {
        await this.tasksStore.moveKanbanTaskInStage({
          boardId: this.boardStore.selectedBoard.id,
          stageId: this.task.stageId,
          taskId: this.task.id,
          direction: this.moveDirection,
        })
        this.moveInStageModal = false
        this.emitReload()
      } catch (err) {
        console.error('Failed to move task in stage:', err)
      }
    },
    openMoveBetweenStagesModal() {
      this.targetStageId = this.stages.length ? this.stages[0].id : null
      this.moveBetweenStagesModal = true
    },
    async confirmMoveBetweenStages() {
      if (!this.targetStageId) return
      try {
        await this.tasksStore.moveKanbanTaskBetweenStages({
          boardId: this.boardStore.selectedBoard.id,
          taskId: this.task.id,
          targetStageId: this.targetStageId,
        })
        this.moveBetweenStagesModal = false

        // Emit uz vecāku komponentu, lai pārlādētu visus task listus
        this.$emit('task-moved')
      } catch (err) {
        console.error('Failed to move task between stages:', err)
      }
    },
    openDeleteModal() {
      this.deleteModal = true
    },
    async confirmDeleteTask() {
      try {
        await this.tasksStore.deleteKanbanTask({
          boardId: this.boardStore.selectedBoard.id,
          taskId: this.task.id,
        })
        this.deleteModal = false
        this.emitReload()
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    },
  },
  computed: {
    error() {
      return this.tasksStore.error
    },
    descriptionRemainingChars() {
      return this.descriptionMaxLength - this.newTaskDescription.length
    },
  },
}
</script>
