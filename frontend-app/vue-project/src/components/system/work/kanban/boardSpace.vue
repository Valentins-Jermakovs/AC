<template>
  <!-- Toolbar -->
  <div
    class="w-full bg-base-100 border border-base-300 
    flex flex-wrap items-center gap-2 p-2"
  >
    <!-- Create -->
    <button
      class="btn btn-neutral flex-1 sm:flex-none"
      @click="openCreateModal"
    >
      <font-awesome-icon icon="fa-solid fa-plus" />
      <span class="hidden sm:inline">Create Board</span>
    </button>

    <!-- Change title -->
    <button
      class="btn btn-neutral flex-1 sm:flex-none"
      @click="openChangeTitleModal"
    >
      <font-awesome-icon icon="fa-solid fa-pen-to-square" />
      <span class="hidden md:inline">
        Change board title
      </span>
    </button>

    <!-- Add stage -->
    <button
      class="btn btn-neutral flex-1 sm:flex-none"
      @click="openAddStageModal"
    >
      <font-awesome-icon icon="fa-solid fa-plus" />
      <span class="hidden md:inline">
        Add Stage
      </span>
    </button>

    <!-- Right side actions -->
    <div class="flex gap-2 sm:ml-auto w-full sm:w-auto">

      <!-- Delete -->
      <button
        v-if="kanbanMembersStore.currentUser 
        && kanbanMembersStore.currentUser.role == 'owner'"
        class="btn btn-neutral flex-1 sm:flex-none"
        @click="openDeleteModal"
      >
        <font-awesome-icon icon="fa-solid fa-trash" />
        <span class="hidden md:inline">
          Delete board
        </span>
      </button>

      <!-- Leave -->
      <button
        v-if="kanbanMembersStore.currentUser 
        && kanbanMembersStore.currentUser.role !== 'owner'"
        class="btn btn-neutral flex-1 sm:flex-none"
        @click="openLeaveBoardModal"
      >
        <font-awesome-icon icon="fa-solid fa-sign-out" />
        <span class="hidden md:inline">
          Leave board
        </span>
      </button>

    </div>
  </div>

  <!-- Board space -->
  <div class="flex-1 flex w-full overflow-auto p-3 sm:p-5">
    <kanbanStage />
  </div>

  <!-- Modals -->

  <!-- Create board -->
  <BaseDialog v-model="createModal" title="Create New Board" confirmText="Create" cancelText="Cancel"
    @confirm="confirmCreateBoard" @cancel="closeCreateModal">
    <div class="flex flex-col w-full gap-2">
      <Transition name="error-slide">
        <div v-if="errorBoard">
          <h1 class="text-error mb-2">{{ errorBoard }}</h1>
        </div>
      </Transition>
      <label for="boardTitle" class="label">Board Title</label>
      <input type="text" class="input w-full" v-model="newBoardTitle" placeholder="Enter board title" />
    </div>
  </BaseDialog>

  <!-- Change board title -->
  <BaseDialog v-model="changeTitleModal" title="Change Board Title" confirmText="Save" cancelText="Cancel"
    @confirm="confirmChangeTitle" @cancel="closeChangeTitleModal">
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorBoard">
          <h1 class="text-error mb-2">{{ errorBoard }}</h1>
        </div>
      </Transition>
      <label for="boardTitle" class="label">Board Title</label>
      <input type="text" class="input w-full" v-model="newTitle" placeholder="Enter new board title" />
    </div>
  </BaseDialog>

  <!-- Add stage -->
  <BaseDialog v-model="addStageModal" title="Add Stage" confirmText="Add" cancelText="Cancel"
    @confirm="confirmAddStage" @cancel="closeAddStageModal">
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorStage">
          <h1 class="text-error mb-2">{{ errorStage }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">Stage Title</label>
      <input type="text" class="input w-full" v-model="newStageTitle" placeholder="Enter stage title" />
    </div>
  </BaseDialog>

  <!-- Delete board -->
  <BaseDialog v-model="deleteModal" title="Confirm Delete" confirmText="Delete" cancelText="Cancel"
    @confirm="confirmDeleteBoard">
    Are you sure you want to delete this board?
  </BaseDialog>

  <!-- Leave board -->
  <BaseDialog v-model="leaveModal" title="Confirm Leave" confirmText="Leave" cancelText="Cancel"
    @confirm="confirmLeaveBoard">
    Are you sure you want to leave this board?
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import kanbanStage from './kanbanStage.vue'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'
import { useUserStore } from '@/stores/user'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'

export default {
  name: 'BoardSpace',
  components: { kanbanStage, BaseDialog },
  data() {
    return {
      createModal: false,
      changeTitleModal: false,
      addStageModal: false,
      deleteModal: false,
      leaveModal: false,
      newBoardTitle: '',
      newTitle: '',
      newStageTitle: '',

      kanbanStore: useKanbanBoardStore(),
      stagesStore: useKanbanStagesStore(),
      userStore: useUserStore(),
      kanbanMembersStore: useKanbanMembersStore(),
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
    closeCreateModal() {
      this.newBoardTitle = ''
      this.createModal = false
      this.kanbanStore.clearError()
    },
    async confirmCreateBoard() {
      try {
        await this.kanbanStore.createBoard({
          title: this.newBoardTitle.trim(),
          email: this.userStore.email,
        })
        this.createModal = false
      } catch (err) {
        console.error('Failed to create board:', err)
      }
    },

    // ===== Leave board =====
    openLeaveBoardModal() {
      this.leaveModal = true
    },
    async confirmLeaveBoard() {
      if (!this.kanbanStore.selectedBoard) return
      try {
        const payload = {
          boardId: this.kanbanStore.selectedBoard.id,
          userId: this.kanbanMembersStore.currentUser.userId,
        }
        await this.kanbanMembersStore.deleteMember(payload)
        await this.kanbanStore.repeatLastRequest()
        this.leaveModal = false
        this.kanbanStore.selectedBoard = null
      } catch (err) {
        console.error('Failed to leave board:', err)
      }
    },

    // ===== Change Board Title =====
    openChangeTitleModal() {
      if (!this.kanbanStore.selectedBoard) return
      this.newTitle = this.kanbanStore.selectedBoard.title
      this.changeTitleModal = true
    },
    closeChangeTitleModal() {
      this.newTitle = ''
      this.changeTitleModal = false
      this.kanbanStore.clearError()
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
    closeAddStageModal() {
      this.newStageTitle = ''
      this.addStageModal = false
      this.stagesStore.clearError()
    },
    async confirmAddStage() {
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

        this.kanbanStore.selectedBoard = null
      } catch (err) {
        console.error('Failed to delete board:', err)
      }
    },
  },
  computed: {
    errorBoard() {
      return this.kanbanStore.error
    },
    errorStage() {
      return this.stagesStore.error
    },
  }
}
</script>
