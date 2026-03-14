<template>
  <div class="w-full flex gap-4 p-2 overflow-x-auto">
    <div
      v-for="stage in stagesStore.stages"
      :key="stage.id"
      class="w-72 h-24 bg-base-100 border border-base-300 p-2 gap-2 rounded-box"
    >
      <div class="flex items-center justify-between">
        <h2 class="flex-1">{{ stage.title }}</h2>

        <!-- Stage options dropdown -->
        <div class="dropdown dropdown-right">
          <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
          <ul
            tabindex="0"
            class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow"
          >
            <li>
              <button class="flex gap-2 items-center text-blue-500">
                <font-awesome-icon icon="fa-solid fa-pencil" />
                Update stage
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-green-500">
                <font-awesome-icon icon="fa-solid fa-arrow-up" />
                Insert stage before
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-green-500">
                <font-awesome-icon icon="fa-solid fa-arrow-down" />
                Insert stage after
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-purple-500">
                <font-awesome-icon icon="fa-solid fa-arrow-right" />
                Move stage to right
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-purple-500">
                <font-awesome-icon icon="fa-solid fa-arrow-left" />
                Move stage to left
              </button>
            </li>
            <li>
              <button class="flex gap-2 items-center text-red-500">
                <font-awesome-icon icon="fa-solid fa-trash" />
                Delete stage
              </button>
            </li>
          </ul>
        </div>
      </div>
      <!-- Create task button -->
      <button class="btn btn-primary btn-sm w-full mt-2">+ Create task</button>
    </div>
  </div>
</template>

<script>
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages';
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards';

export default {
  name: 'KanbanStage',
  data() {
    return {
      stagesStore: useKanbanStagesStore(),
      boardStore: useKanbanBoardStore(),
    }
  },
  watch: {
    // Watch selectedBoard un ielādē stages automātiski
    'boardStore.selectedBoard'(newBoard) {
      if (newBoard) {
        this.stagesStore.boardId = newBoard.id
        this.stagesStore.getStages()
      } else {
        this.stagesStore.stages = []
      }
    }
  },
  mounted() {
    // ja jau ir selectedBoard
    if (this.boardStore.selectedBoard) {
      this.stagesStore.boardId = this.boardStore.selectedBoard.id
      this.stagesStore.getStages()
    }
  }
}
</script>

<style scoped></style>
