<template>
  <!-- Main wrapper -->
  <div class="flex flex-col md:flex-row flex-1 w-full min-h-full sm:h-full overflow-hidden">

    <!-- Main content: board + members -->
    <div class="flex flex-col flex-1 w-full h-full overflow-hidden order-1 md:order-1">

      <!-- View switch panel -->
      <div
        v-if="kanbanBoardStore.selectedBoard"
        class="w-full bg-base-100 border border-base-300 
        flex flex-wrap sm:flex-nowrap p-2 gap-2"
      >
        <button
          class="btn flex-1 sm:flex-none"
          :class="activeView === 'board' ? 'btn-primary' : 'btn-neutral'"
          @click="activeView = 'board'"
        >
          <font-awesome-icon icon="fa-solid fa-table-cells" />
          <span class="hidden sm:inline">Board View</span>
        </button>

        <button
          class="btn flex-1 sm:flex-none"
          :class="activeView === 'members' ? 'btn-primary' : 'btn-neutral'"
          @click="activeView = 'members'"
        >
          <font-awesome-icon icon="fa-solid fa-users" />
          <span class="hidden sm:inline">Members View</span>
        </button>
      </div>

      <!-- Content -->
      <div class="flex flex-col overflow-auto flex-1">

        <!-- BOARD -->
        <BoardSpace
          v-if="activeView === 'board' && kanbanBoardStore.selectedBoard"
          class="flex-1"
        />

        <!-- Empty state -->
        <NullBoards
          v-if="activeView === 'board' && !kanbanBoardStore.selectedBoard"
          class="flex-1"
        />

        <!-- MEMBERS -->
        <MembersSpace
          v-if="activeView === 'members'"
          class="flex-1"
        />

      </div>
    </div>

    <!-- Sidebar -->
    <KanbanSideBar
      class="w-full h-auto sm:h-full md:w-64 order-2 md:order-2 mt-2 md:mt-0"
    />

    <!-- Loading -->
    <LoadingScreen
      v-if="kanbanBoardStore.loading"
    />

  </div>
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import KanbanSideBar from './kanban/kanbanSideBar.vue'
import KanbanStage from './kanban/kanbanStage.vue'
import BoardSpace from './kanban/boardSpace.vue'
import MembersSpace from './kanban/membersSpace.vue'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import NullBoards from './kanban/nullBoards.vue'

export default {
  name: 'KanbanPage',
  components: {
    KanbanSideBar,
    KanbanStage,
    LoadingScreen,
    BoardSpace,
    MembersSpace,
    NullBoards,
  },
  data() {
    return {
      kanbanBoardStore: useKanbanBoardStore(),
      activeView: 'board',
    }
  },
}
</script>

<style scoped></style>
