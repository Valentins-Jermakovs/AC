<template>
  <div class="flex flex-1 w-full h-full">
    <KanbanSideBar></KanbanSideBar>
    <div class="flex flex-col flex-1 w-full h-full overflow-auto">
      <!-- Panel: board/members -->
      <div class="w-full h-12 bg-base-100 flex" v-if="kanbanBoardStore.selectedBoard">
        <button
          class="btn h-full"
          :class="activeView === 'board' ? 'btn-primary' : 'btn-neutral'"
          @click="activeView = 'board'"
        >
          Board View
          <font-awesome-icon icon="fa-solid fa-table-cells" />
        </button>
        <button
          class="btn h-full"
          :class="activeView === 'members' ? 'btn-primary' : 'btn-neutral'"
          @click="activeView = 'members'"
        >
          Members View
          <font-awesome-icon icon="fa-solid fa-users" />
        </button>
      </div>

      <!-- ========== BOARD SPACE ========== -->
      <BoardSpace v-if="activeView === 'board' && kanbanBoardStore.selectedBoard"></BoardSpace>

      <!-- Screen for creating a new board -->
      <NullBoards v-if="activeView === 'board' && !kanbanBoardStore.selectedBoard"></NullBoards>

      <!-- ========== MEMBERS MANAGEMENT SPACE ========== -->
      <MembersSpace v-if="activeView === 'members'"></MembersSpace>
    </div>

    <LoadingScreen v-if="kanbanBoardStore.loading"></LoadingScreen>
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
