<template>
  <div class="h-full flex flex-col w-64 bg-base-200 border border-base-300 p-1 gap-2">
    <!-- Search bar -->
    <div class="w-full p-1 bg-base-100 border border-base-300 flex flex-col items-center gap-2">
      <div class="w-full">
        <input
          type="text"
          class="input"
          placeholder="Search..."
          v-model="kanbanBoardStore.searchQuery"
          @keyup.enter="searchBoards"
          :disabled="kanbanBoardStore.searchMode === 'all'"
        />
      </div>
      <div class="w-full flex items-center gap-2">
        <select class="select select-bordered flex-1" v-model="kanbanBoardStore.searchMode">
          <option value="all">All</option>
          <option value="title">By title</option>
        </select>
        <button
          class="btn btn-primary"
          @click="searchBoards"
          :disabled="
            kanbanBoardStore.searchMode === 'title' && !kanbanBoardStore.searchQuery.trim()
          "
        >
          <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
        </button>
      </div>
    </div>

    <!-- List of boards -->
    <div
      class="w-full flex flex-1 flex-col bg-base-100 border border-base-300 overflow-y-auto p-3 gap-2"
    >
      <!-- If list is empty -->
      <div v-if="boards.length === 0" class="w-full h-full flex items-center justify-center">
        <font-awesome-icon icon="fa-solid fa-triangle-exclamation" size="2xl" />
        Boards not found!
      </div>

      <div
        v-for="board in boards"
        :key="board.id"
        class="w-full bg-base-200 border border-base-300 rounded-box p-3 flex items-center hover:cursor-pointer hover:border-info hover:bg-base-300 duration-300 transition-all"
        @click="selectBoard(board)"
      >
        <h1>{{ board.title }}</h1>
      </div>
    </div>

    <!-- Footer -->
    <div class="bg-base-100 border border-base-300 flex flex-col p-1 gap-2">
      <select class="select select-bordered w-full" @change="setLimit">
        <option disabled selected>Limit</option>
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="30">30</option>
      </select>

      <div
        class="w-full p-1 flex flex-col items-start bg-base-100 border border-base-300 gap-1 text-base-content/60"
      >
        <p>Current page {{ meta.page }} / {{ meta.totalPages }}</p>
        <p>Limit: {{ meta.limit }}</p>
      </div>

      <div class="w-full gap-1 flex items-center p-1 justify-center">
        <button
          class="btn btn-neutral w-1/2"
          @click="prevPage"
          :disabled="meta.page === 1 || boards.length === 0"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-left" />
        </button>

        <button
          class="btn btn-neutral w-1/2"
          @click="nextPage"
          :disabled="meta.page === meta.totalPages || boards.length === 0"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-right" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'

export default {
  name: 'KanbanSidebar',

  data() {
    return {
      kanbanBoardStore: useKanbanBoardStore(),
      kanbanStagesStore: useKanbanStagesStore(),
    }
  },

  mounted() {
    this.kanbanBoardStore.fetchKanbanBoards()
  },

  computed: {
    boards() {
      return this.kanbanBoardStore.boards
    },
    meta() {
      return this.kanbanBoardStore.meta
    },
    loading() {
      return this.kanbanBoardStore.loading
    },
  },

  methods: {
    async searchBoards() {
      this.kanbanBoardStore.meta.page = 1

      switch (this.kanbanBoardStore.searchMode) {
        case 'all':
          await this.kanbanBoardStore.fetchKanbanBoards()
          break
        case 'title':
          await this.kanbanBoardStore.findKanbanBoardsByTitle()
          break
      }
    },
    selectBoard(board) {
      this.kanbanBoardStore.selectedBoard = board

      this.kanbanStagesStore.boardId = board.id
      this.kanbanStagesStore.getStages()
    },

    nextPage() {
      this.kanbanBoardStore.nextPage()
    },

    prevPage() {
      this.kanbanBoardStore.prevPage()
    },

    setLimit(event) {
      this.kanbanBoardStore.setLimit(event.target.value)
    },
  },

  watch: {
    // Watch searchMode: ja izvēlas "all", notīra input lauku
    'kanbanBoardStore.searchMode'(newMode) {
      if (newMode === 'all') {
        this.kanbanBoardStore.searchQuery = ''
      }
    },
  },
}
</script>

<style scoped></style>
