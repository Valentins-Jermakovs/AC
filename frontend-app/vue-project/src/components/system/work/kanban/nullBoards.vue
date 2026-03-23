<template>
  <div class="w-full h-full flex items-center justify-center flex-col gap-5 p-1">
    <div class="flex items-center justify-center gap-2 text-red text-2xl">
      <font-awesome-icon icon="fa-solid fa-triangle-exclamation" size="2xl" />
      <h1>Boards not found or you don't have selected any board</h1>
    </div>
    <button class="btn btn-primary" @click="openCreateBoardModal">
      <font-awesome-icon icon="fa-solid fa-plus" />
      Create new board
    </button>
  </div>

  <!-- Create board modal -->
  <base-dialog v-model="createModal" title="Create New Board" confirmText="Create" cancelText="Cancel"
    @confirm="confirmCreateBoard">
    <div class="flex flex-col gap-2 w-full">
      <label for="boardTitle" class="label">Board Title</label>
      <input type="text" class="input w-full" v-model="newBoardTitle" placeholder="Enter board title" />
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
    async confirmCreateBoard() {
      if (!this.newBoardTitle.trim()) return
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
}
</script>

<style scoped></style>
