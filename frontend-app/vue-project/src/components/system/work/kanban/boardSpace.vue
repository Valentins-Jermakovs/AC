<template>
  <div class="w-full bg-base-200 flex items-center border border-base-300">
    <!-- Create Board button -->
    <button class="btn btn-neutral" @click="openCreateModal">
      <font-awesome-icon icon="fa-solid fa-plus" />
      Create Board
    </button>

    <!-- Change title -->
    <button class="btn btn-neutral" @click="openChangeTitleModal">
      <font-awesome-icon icon="fa-solid fa-pen-to-square" />
      Change board title
    </button>

    <!-- Add stage -->
    <button class="btn btn-neutral" @click="openAddStageModal">
      <font-awesome-icon icon="fa-solid fa-plus" />
      Add Stage
    </button>

    <!-- Delete board -->
    <button class="btn btn-neutral" @click="openDeleteModal">
      <font-awesome-icon icon="fa-solid fa-trash" />
      Delete board
    </button>
  </div>

  <!-- Board space -->
  <div class="flex-1 flex w-full overflow-auto p-5">
    <kanbanStage></kanbanStage>
  </div>

  <!-- Modals -->

  <!-- Create board -->
  <BaseDialog v-model="createModal" title="Create New Board" confirmText="Create" cancelText="Cancel"
    @confirm="confirmCreateBoard">
    <input type="text" class="input w-full" v-model="newBoardTitle" placeholder="Enter board title" />
  </BaseDialog>

  <!-- Change board title -->
  <BaseDialog v-model="changeTitleModal" title="Change Board Title" confirmText="Save" cancelText="Cancel"
    @confirm="confirmChangeTitle">
    <input type="text" class="input w-full" v-model="newTitle" placeholder="Enter new board title" />
  </BaseDialog>

  <!-- Add stage -->
  <BaseDialog v-model="addStageModal" title="Add Stage" confirmText="Add" cancelText="Cancel"
    @confirm="confirmAddStage">
    <input type="text" class="input w-full" v-model="newStageTitle" placeholder="Enter stage title" />
  </BaseDialog>

  <!-- Delete board -->
  <BaseDialog v-model="deleteModal" title="Confirm Delete" confirmText="Delete" cancelText="Cancel"
    @confirm="confirmDeleteBoard">
    Are you sure you want to delete this board?
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import kanbanStage from './kanbanStage.vue'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'

export default {
  name: 'BoardSpace',
  components: { kanbanStage, BaseDialog },
  data() {
    return {
      createModal: false,
      changeTitleModal: false,
      addStageModal: false,
      deleteModal: false,
      newBoardTitle: '',
      newTitle: '',
      newStageTitle: '',
      kanbanStore: useKanbanBoardStore(),
      stagesStore: useKanbanStagesStore(),
    }
  },
  watch: {
    'kanbanStore.selectedBoard': {
      handler(board) {
        if (board) this.newTitle = board.title
      },
      immediate: true,
    },
  },
  methods: {
    
    // ===== Create Board =====
    openCreateModal() {
      this.newBoardTitle = ''
      this.createModal = true
    },
    async confirmCreateBoard() {
      if (!this.newBoardTitle.trim()) return
      try {
        await this.kanbanStore.createBoard({ title: this.newBoardTitle.trim() })
        this.createModal = false
      } catch (err) {
        console.error('Failed to create board:', err)
      }
    },

    // ===== Change Board Title =====
    openChangeTitleModal() {
      if (!this.kanbanStore.selectedBoard) return
      this.newTitle = this.kanbanStore.selectedBoard.title
      this.changeTitleModal = true
    },
    async confirmChangeTitle() {
      if (!this.kanbanStore.selectedBoard) return
      try {
        await this.kanbanStore.updateBoard({
          boardId: this.kanbanStore.selectedBoard.id,
          title: this.newTitle,
        })
        this.changeTitleModal = false
      } catch (err) {
        console.error('Failed to change title:', err)
      }
    },

    // ===== Add Stage =====
    openAddStageModal() {
      if (!this.kanbanStore.selectedBoard) return
      this.newStageTitle = ''
      this.addStageModal = true
    },
    async confirmAddStage() {
      if (!this.newStageTitle.trim() || !this.kanbanStore.selectedBoard) return
      try {
        await this.stagesStore.createStage({
          boardId: this.kanbanStore.selectedBoard.id,
          title: this.newStageTitle.trim(),
        })
        this.addStageModal = false
      } catch (err) {
        console.error('Failed to add stage:', err)
      }
    },

    // ===== Delete Board =====
    openDeleteModal() {
      if (!this.kanbanStore.selectedBoard) return
      this.deleteModal = true
    },
    async confirmDeleteBoard() {
      if (!this.kanbanStore.selectedBoard) return
      try {
        await this.kanbanStore.deleteBoard(this.kanbanStore.selectedBoard.id)
        this.deleteModal = false
      } catch (err) {
        console.error('Failed to delete board:', err)
      }
    },
  },
}
</script>