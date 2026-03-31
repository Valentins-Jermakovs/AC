<template>
  <div class="w-full h-full flex items-center justify-center flex-col gap-6 flex-1">
    <!-- Icon block -->
    <div
      class="flex flex-col items-center gap-4 p-8 bg-base-200 border border-base-300 w-full max-w-md"
    >
      <!-- Animated icon -->
      <div class="relative">
        <font-awesome-icon icon="fa-solid fa-layer-group" class="text-6xl text-base-content/20" />

        <font-awesome-icon
          icon="fa-solid fa-triangle-exclamation"
          class="text-error text-2xl absolute -top-2 -right-3"
          bounce
        />
      </div>

      <!-- Text -->
      <div class="text-center flex flex-col gap-2">
        <h1 class="text-xl font-semibold text-error flex items-center gap-2 justify-center">
          <font-awesome-icon icon="fa-solid fa-circle-exclamation" />
          {{ $t('work.kanban.errors.boards_not_found') }}
        </h1>
      </div>

      <div class="divider my-1"></div>

      <!-- Action -->
      <button class="btn btn-primary gap-2" @click="openCreateBoardModal">
        <font-awesome-icon icon="fa-solid fa-plus" />

        {{ $t('work.kanban.controls.create_board') }}
      </button>
    </div>
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
