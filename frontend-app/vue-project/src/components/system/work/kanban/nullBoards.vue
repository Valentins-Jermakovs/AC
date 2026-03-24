<template>
  <div class="w-full h-full flex items-center justify-center flex-col gap-5 p-1 flex-1">
    <div class="flex items-center justify-center gap-2 text-red text-2xl">
      <font-awesome-icon icon="fa-solid fa-triangle-exclamation" size="2xl" />
      <h1>{{ $t('work.kanban.errors.boards_not_found') }}</h1>
    </div>
    <button class="btn btn-primary" @click="openCreateBoardModal">
      <font-awesome-icon icon="fa-solid fa-plus" />
      {{ $t('work.kanban.controls.create_board') }}
    </button>
  </div>

  <!-- Create board modal -->
  <base-dialog
    v-model="createModal"
    :title="$t('work.kanban.modals.create_board.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmCreateBoard"
    @cancel="closeCreateModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
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
  </base-dialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useUserStore } from '@/stores/user'

export default {
  name: 'NullBoards',
  components: { BaseDialog },

  data() {
    return {
      kanbanBoardStore: useKanbanBoardStore(),
      userStore: useUserStore(),
      createModal: false,
      newBoardTitle: '',
    }
  },
  methods: {
    openCreateBoardModal() {
      this.newBoardTitle = ''
      this.createModal = true
    },
    closeCreateModal() {
      this.newBoardTitle = ''
      this.createModal = false
      this.kanbanBoardStore.clearError()
    },
    async confirmCreateBoard() {
      try {
        await this.kanbanBoardStore.createBoard({
          title: this.newBoardTitle.trim(),
          email: this.userStore.email,
        })
        this.createModal = false
      } catch (err) {
        console.error('Failed to create board:', err)
      }
    },
  },
  mounted() {
    if (!this.userStore.isLoaded) {
      this.userStore.fetchMe()
    }
  },
  computed: {
    error() {
      return this.kanbanBoardStore.error
    },
  },
}
</script>

<style scoped></style>
