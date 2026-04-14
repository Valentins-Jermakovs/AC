<template>
  <!-- Main wrapper -->
  <div class="flex flex-col sm:flex-row flex-1 w-full min-h-full sm:h-full overflow-hidden">
    <!-- Main content: board + members -->
    <div class="flex flex-col flex-1 w-full h-full overflow-hidden order-1 md:order-1">
      <!-- View switch panel -->
      <div
        v-if="kanbanBoardStore.selectedBoard"
        class="w-full bg-base-100 border border-base-300 flex flex-wrap sm:flex-nowrap p-2 gap-2"
      >
        <button
          class="btn flex-1 sm:flex-none"
          :class="activeView === 'board' ? 'btn-primary' : 'btn-neutral'"
          @click="activeView = 'board'"
        >
          <font-awesome-icon icon="fa-solid fa-table-cells" />
          <span class="hidden sm:inline">{{ $t('work.kanban.board_view') }}</span>
        </button>

        <button
          class="btn flex-1 sm:flex-none"
          :class="activeView === 'members' ? 'btn-primary' : 'btn-neutral'"
          @click="activeView = 'members'"
          :disabled="
            kanbanMembersStore.currentUser && (kanbanMembersStore.currentUser.role === 'viewer' || kanbanMembersStore.currentUser.role === 'editor')
          "
        >
          <font-awesome-icon icon="fa-solid fa-users" />
          <span class="hidden sm:inline">{{ $t('work.kanban.member_view') }}</span>
        </button>
      </div>

      <!-- Content -->
      <div class="flex flex-col overflow-auto flex-1">
        <!-- BOARD -->
        <BoardSpace v-if="activeView === 'board' && kanbanBoardStore.selectedBoard" />

        <!-- Empty state -->
        <NullBoards v-if="activeView === 'board' && !kanbanBoardStore.selectedBoard" />

        <!-- MEMBERS -->
        <MembersSpace v-if="activeView === 'members'" />
      </div>
    </div>

    <!-- Sidebar -->
    <KanbanSideBar />

    <!-- Loading -->
    <LoadingScreen v-if="kanbanBoardStore.loading" />
  </div>
</template>

<script>
import { watch } from 'vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import KanbanSideBar from './kanban/kanbanSideBar.vue'
import KanbanStage from './kanban/kanbanStage.vue'
import BoardSpace from './kanban/boardSpace.vue'
import MembersSpace from './kanban/membersSpace.vue'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'
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
      kanbanMembersStore: useKanbanMembersStore(),
      activeView: 'board',
    }
  },
  mounted() {
    watch(
      () => this.kanbanBoardStore.selectedBoard,
      async (newBoard) => {
        if (newBoard) {
          this.kanbanMembersStore.boardId = newBoard.id
          try {
            await this.kanbanMembersStore.fetchMe()
          } catch (e) {
            console.error('Failed to fetch currentUser:', e)
          }
        }
      },
      { immediate: true },
    )
  },
}
</script>

<style scoped></style>
