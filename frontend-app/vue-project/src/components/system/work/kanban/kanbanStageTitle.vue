<template>
  <!-- Stage header -->
  <div class="flex items-center justify-between p-2 border border-base-300 bg-base-100">
    <h2 class="flex-1 font-semibold text-lg">{{ stage.title }}</h2>

    <!-- Stage options dropdown -->
    <div class="dropdown dropdown-right">
      <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
      <ul
        tabindex="0"
        class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow"
      >
        <li>
          <button class="flex gap-2 items-center text-blue-500" @click="openUpdateModal">
            <font-awesome-icon icon="fa-solid fa-pencil" />
            Update stage
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center text-green-500" @click="openInsertModal('before')">
            <font-awesome-icon icon="fa-solid fa-arrow-up" />
            Insert stage before
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center text-green-500" @click="openInsertModal('after')">
            <font-awesome-icon icon="fa-solid fa-arrow-down" />
            Insert stage after
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center text-purple-500" @click="moveStage('right')">
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
            Move stage to right
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center text-purple-500" @click="moveStage('left')">
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
            Move stage to left
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center text-red-500" @click="openDeleteModal">
            <font-awesome-icon icon="fa-solid fa-trash" />
            Delete stage
          </button>
        </li>
      </ul>
    </div>
  </div>

  <!-- BaseDialogs -->
  <BaseDialog
    v-model="updateModal"
    title="Update Stage Title"
    confirmText="Save"
    cancelText="Cancel"
    @confirm="confirmUpdateStage"
    @cancel="closeUpdateModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorStage">
          <h1 class="text-error mb-2">{{ errorStage }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">Stage Title</label>
      <input type="text" class="input w-full" v-model="newStageTitle" />
    </div>
  </BaseDialog>

  <BaseDialog
    v-model="insertModal"
    title="Insert Stage"
    confirmText="Insert"
    cancelText="Cancel"
    @confirm="confirmInsertStage"
    @cancel="closeInsertModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorStage">
          <h1 class="text-error mb-2">{{ errorStage }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">Stage Title</label>
      <input type="text" class="input w-full" v-model="newStageTitle" placeholder="Stage title" />
    </div>
  </BaseDialog>

  <BaseDialog
    v-model="deleteModal"
    title="Delete Stage"
    confirmText="Delete"
    cancelText="Cancel"
    @confirm="confirmDeleteStage"
  >
    Are you sure you want to delete this stage?
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'

export default {
  name: 'kanbanStageTitle',
  props: {
    stage: { type: Object, required: true },
  },
  components: { BaseDialog },
  data() {
    return {
      updateModal: false,
      insertModal: false,
      deleteModal: false,
      newStageTitle: '',
      insertPosition: 'before',
      stagesStore: useKanbanStagesStore(),
      kanbanStore: useKanbanBoardStore(),
    }
  },
  methods: {
    // ===== Update Stage =====
    openUpdateModal() {
      this.newStageTitle = this.stage.title
      this.updateModal = true
    },
    closeUpdateModal() {
      this.newStageTitle = ''
      this.updateModal = false
      this.kanbanStore.clearError()
    },
    async confirmUpdateStage() {
      try {
        await this.stagesStore.updateStage({
          boardId: this.kanbanStore.selectedBoard.id,
          stageId: this.stage.id,
          title: this.newStageTitle.trim(),
        })
        this.updateModal = false
      } catch (err) {
        console.error('Failed to update stage:', err)
      }
    },

    // ===== Insert Relative Stage =====
    openInsertModal(position) {
      this.insertPosition = position
      this.newStageTitle = ''
      this.insertModal = true
    },
    closeInsertModal() {
      this.newStageTitle = ''
      this.insertModal = false
      this.stagesStore.clearError()
    },
    async confirmInsertStage() {
      try {
        await this.stagesStore.createStageRelative({
          boardId: this.kanbanStore.selectedBoard.id,
          title: this.newStageTitle.trim(),
          referenceStageId: this.stage.id,
          position: this.insertPosition,
        })
        this.insertModal = false
      } catch (err) {
        console.error(`Failed to insert stage ${this.insertPosition}:`, err)
      }
    },

    // ===== Move Stage =====
    async moveStage(direction) {
      try {
        await this.stagesStore.moveStage({
          boardId: this.kanbanStore.selectedBoard.id,
          stageId: this.stage.id,
          direction: direction === 'left' ? 'up' : 'down',
        })
      } catch (err) {
        console.error('Failed to move stage:', err)
      }
    },

    // ===== Delete Stage =====
    openDeleteModal() {
      this.deleteModal = true
    },
    async confirmDeleteStage() {
      try {
        await this.stagesStore.deleteStage({
          boardId: this.kanbanStore.selectedBoard.id,
          stageId: this.stage.id,
        })
        this.deleteModal = false
      } catch (err) {
        console.error('Failed to delete stage:', err)
      }
    },
  },
  computed: {
    errorStage() {
      return this.stagesStore.error
    },
  },
}
</script>
