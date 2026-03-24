<template>
  <!-- Toolbar -->
  <div
    class="w-full bg-base-100 border border-base-300 flex flex-wrap items-center gap-2 p-2 flex-1"
  >
    <!-- Create -->
    <button class="btn btn-neutral flex-1 sm:flex-none" @click="openCreateModal">
      <font-awesome-icon icon="fa-solid fa-plus" />
      <span class="hidden sm:inline">{{ $t('work.kanban.controls.create_board') }}</span>
    </button>

    <!-- Change title -->
    <button
      class="btn btn-neutral flex-1 sm:flex-none"
      @click="openChangeTitleModal"
      :disabled="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'viewer'"
    >
      <font-awesome-icon icon="fa-solid fa-pen-to-square" />
      <span class="hidden md:inline">{{ $t('work.kanban.controls.change_board_title') }}</span>
    </button>

    <!-- Add stage -->
    <button
      class="btn btn-neutral flex-1 sm:flex-none"
      @click="openAddStageModal"
      :disabled="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'viewer'"
    >
      <font-awesome-icon icon="fa-solid fa-plus" />
      <span class="hidden md:inline">{{ $t('work.kanban.controls.create_stage') }}</span>
    </button>

    <!-- Right side actions -->
    <div class="flex gap-2 sm:ml-auto w-full sm:w-auto">
      <!-- Delete -->
      <button
        :disabled="
          (kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'viewer') ||
          kanbanMembersStore.currentUser.role === 'editor'
        "
        class="btn btn-neutral flex-1 sm:flex-none"
        @click="openDeleteModal"
      >
        <font-awesome-icon icon="fa-solid fa-trash" />
        <span class="hidden md:inline">{{ $t('work.kanban.controls.delete_board') }}</span>
      </button>

      <!-- Leave -->
      <button
        v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role != 'owner'"
        class="btn btn-neutral flex-1 sm:flex-none"
        @click="openLeaveBoardModal"
      >
        <font-awesome-icon icon="fa-solid fa-sign-out" />
        <span class="hidden md:inline">{{ $t('work.kanban.controls.leave_board') }}</span>
      </button>
    </div>
  </div>

  <!-- Board space -->
  <div class="flex-1 flex w-full min-h-screen p-3 sm:p-5">
    <kanbanStage />
  </div>

  <!-- Modals -->

  <!-- Create board -->
  <BaseDialog
    v-model="createModal"
    :title="$t('work.kanban.modals.create_board.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmCreateBoard"
    @cancel="closeCreateModal"
  >
    <div class="flex flex-col w-full gap-2">
      <Transition name="error-slide">
        <div v-if="errorBoard">
          <h1 class="text-error mb-2">{{ errorBoard }}</h1>
        </div>
      </Transition>
      <label for="boardTitle" class="label">{{ $t('work.kanban.modals.create_board.name') }}</label>
      <input
        type="text"
        class="input w-full"
        v-model="newBoardTitle"
        :placeholder="$t('work.kanban.modals.create_board.name_placeholder')"
      />
    </div>
  </BaseDialog>

  <!-- Change board title -->
  <BaseDialog
    v-model="changeTitleModal"
    :title="$t('work.kanban.modals.change_board_title.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmChangeTitle"
    @cancel="closeChangeTitleModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorBoard">
          <h1 class="text-error mb-2">{{ errorBoard }}</h1>
        </div>
      </Transition>
      <label for="boardTitle" class="label">{{
        $t('work.kanban.modals.change_board_title.name')
      }}</label>
      <input
        type="text"
        class="input w-full"
        v-model="newTitle"
        :placeholder="$t('work.kanban.modals.change_board_title.name_placeholder')"
      />
    </div>
  </BaseDialog>

  <!-- Add stage -->
  <BaseDialog
    v-model="addStageModal"
    :title="$t('work.kanban.modals.create_stage.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmAddStage"
    @cancel="closeAddStageModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorStage">
          <h1 class="text-error mb-2">{{ errorStage }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">{{ $t('work.kanban.modals.create_stage.name') }}</label>
      <input
        type="text"
        class="input w-full"
        v-model="newStageTitle"
        :placeholder="$t('work.kanban.modals.create_stage.name_placeholder')"
      />
    </div>
  </BaseDialog>

  <!-- Delete board -->
  <BaseDialog
    v-model="deleteModal"
    :title="$t('work.kanban.modals.delete_board.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmDeleteBoard"
  >
    {{ $t('work.kanban.modals.delete_board.content') }}
  </BaseDialog>

  <!-- Leave board -->
  <BaseDialog
    v-model="leaveModal"
    :title="$t('work.kanban.modals.leave_board.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmLeaveBoard"
  >
    {{ $t('work.kanban.modals.leave_board.content') }}
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
  },
}
</script>
