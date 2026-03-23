<template>
  <div class="w-full bg-base-100 rounded-box p-1 border border-base-300">
    <!-- Task title and dropdown menu -->
    <div class="flex flex-col items-center">
      <div class="w-full flex justify-between items-center p-1">
        <h2 class="flex-1">{{ task.title }}</h2>
        <div class="dropdown dropdown-right z-10">
          <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
          <ul
            tabindex="0"
            class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow"
          >
            <li>
              <button class="flex gap-2 items-center text-blue-500" @click="openUpdateModal">
                <font-awesome-icon icon="fa-solid fa-pencil" /> Update task
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-green-500" @click="openMoveInStageModal">
                <font-awesome-icon icon="fa-solid fa-arrow-up" /> Move in stage
              </button>
            </li>
            <li>
              <button
                class="flex gap-2 items-center text-purple-500"
                @click="openMoveBetweenStagesModal"
              >
                <font-awesome-icon icon="fa-solid fa-arrow-right" /> Move to another stage
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-red-500" @click="openDeleteModal">
                <font-awesome-icon icon="fa-solid fa-trash" /> Delete task
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
      title="Update Task"
      confirmText="Save"
      cancelText="Cancel"
      @confirm="confirmUpdateTask"
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
          class="input w-full min-h-52"
          v-model="newTaskDescription"
          placeholder="Task description"
        ></textarea>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="moveInStageModal"
      title="Move Task in Stage"
      confirmText="Move"
      cancelText="Cancel"
      @confirm="confirmMoveInStage"
    >
      <div class="w-full flex flex-col gap-2">
        <label for="taskTitle" class="label">Move task:</label>
        <select class="select select-bordered w-full" v-model="moveDirection">
          <option value="up">Up</option>
          <option value="down">Down</option>
        </select>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="moveBetweenStagesModal"
      title="Move Task to Another Stage"
      confirmText="Move"
      cancelText="Cancel"
      @confirm="confirmMoveBetweenStages"
    >
      <div class="w-full flex flex-col gap-2">
        <label for="taskTitle" class="label">Move task to:</label>
        <select class="select select-bordered w-full" v-model="targetStageId">
          <option v-for="stage in stages" :key="stage.id" :value="stage.id">
            {{ stage.title }}
          </option>
        </select>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="deleteModal"
      title="Delete Task"
      confirmText="Delete"
      cancelText="Cancel"
      @confirm="confirmDeleteTask"
    >
      Are you sure you want to delete this task?
    </BaseDialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanTasksStore } from '@/stores/kanban/kanbanTasks'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'

export default {
  props: { task: { type: Object, required: true } },
  components: { BaseDialog },
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
      stages: boardStore.selectedBoard ? [] : [],
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
}
</script>
