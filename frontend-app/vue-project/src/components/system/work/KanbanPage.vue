<template>
  <div class="flex flex-1 w-full h-full">
    <KanbanSideBar></KanbanSideBar>
    <div class="flex flex-col flex-1 w-full h-full">
      <!-- Panel: board/members -->
      <div class="w-full h-12 bg-base-100 border border-base-300 flex">
        <button class="btn btn-primary h-full">
          Board View
          <font-awesome-icon icon="fa-solid fa-table-cells" />
        </button>
        <button class="btn h-full">
          Members View
          <font-awesome-icon icon="fa-solid fa-users" />
        </button>
      </div>

      <!-- ========== BOARD SPACE ========== -->

      <div class="w-full bg-base-200 border border-base-300 flex items-center">
        <button class="btn btn-neutral">Change board title</button>
        <button class="btn btn-secondary">Add Stage</button>
        <button class="btn btn-warning">Delete board</button>
        <button class="btn btn-warning">Leave board</button>
      </div>
      <!-- Board space -->
      <div class="flex-1 flex w-full overflow-auto p-5 bg-pattern">
        <KanbanStage></KanbanStage>
      </div>

      <!-- ========== MEMBERS MANAGEMENT SPACE ========== -->

      <!-- Members space -->
      <!-- <div class="flex-1 flex flex-col w-full h-full overflow-auto p-5 gap-2">

        <div class="w-full h-full flex flex-col items-center gap-4 p-4">

          <div class="w-3/5 flex justify-between items-center gap-2">

            <button class="btn btn-success h-full">
              <font-awesome-icon icon="fa-solid fa-user-plus" />
              Add member
            </button>

            <div class="flex flex-1 bg-base-200 border border-base-300
            px-4 py-2 items-center gap-4">

              <div class="flex-1">
                <select class="select select-bordered">
                  <option disabled selected>Limit</option>
                  <option>10</option>
                  <option>20</option>
                  <option>30</option>
                </select>
              </div>

              <div class="flex-1"></div>

              <div class="flex gap-4 text-sm">
                <p>Total: <span class="font-semibold">10</span></p>
                <p>Page: <span class="font-semibold">1/2</span></p>
              </div>

              <div class="flex-1"></div>

              <div class="flex gap-2">
                <button class="btn btn-sm btn-neutral">
                  <font-awesome-icon icon="fa-solid fa-arrow-left" />
                </button>

                <button class="btn btn-sm btn-neutral">
                  <font-awesome-icon icon="fa-solid fa-arrow-right" />
                </button>
              </div>

            </div>

          </div>

          <div class="w-3/5 bg-base-200 border border-base-300 
           flex flex-col gap-3 p-3">

            <div class="w-full p-4 bg-base-100 border border-base-300
            rounded-box flex items-center justify-between gap-3">

              <div class="flex items-center gap-3 font-medium flex-1 p-2">
                <div class="flex w-full bg-base-200 p-3 items-center gap-2
                rounded-box border border-base-300">
                  <font-awesome-icon icon="fa-solid fa-user" />
                  Member 1
                </div>
              </div>

              <div class="flex items-center gap-2 badge badge-primary
              rounded-box">
                Admin
              </div>

              <div class="dropdown dropdown-right">

                <div tabindex="0" role="button" class="btn btn-sm btn-ghost">
                  ⋮
                </div>
                <ul tabindex="0" class="dropdown-content menu bg-base-200 
                border border-base-300 rounded-box 
                w-48 p-2 shadow">
                  <li>
                    <button class="flex gap-2">
                      <font-awesome-icon icon="fa-solid fa-pencil" />
                      Update
                    </button>
                  </li>
                  <li>
                    <button class="flex gap-2 text-error">
                      <font-awesome-icon icon="fa-solid fa-trash" />
                      Delete
                    </button>
                  </li>
                </ul>
              </div>
            </div>

            <div class="w-full p-4 bg-base-100 border border-base-300
            rounded-box flex items-center justify-between gap-3">

              <div class="flex items-center gap-3 font-medium flex-1 p-2">
                <div class="flex w-full bg-base-200 p-3 items-center gap-2
                rounded-box border border-base-300">
                  <font-awesome-icon icon="fa-solid fa-user" />
                  Member 2
                </div>
              </div>

              <div class="flex items-center gap-2 badge badge-secondary
              rounded-box">
                Editor
              </div>
  
              <div class="dropdown dropdown-right">

                <div tabindex="0" role="button" class="btn btn-sm btn-ghost">
                  ⋮
                </div>
                <ul tabindex="0" class="dropdown-content menu bg-base-200 
                border border-base-300 rounded-box 
                w-48 p-2 shadow">
                  <li>
                    <button class="flex gap-2">
                      <font-awesome-icon icon="fa-solid fa-pencil" />
                      Update
                    </button>
                  </li>
                  <li>
                    <button class="flex gap-2 text-error">
                      <font-awesome-icon icon="fa-solid fa-trash" />
                      Delete
                    </button>
                  </li>
                </ul>
              </div>
            </div>

            <div class="w-full p-4 bg-base-100 border border-base-300
            rounded-box flex items-center justify-between gap-3">

              <div class="flex items-center gap-3 font-medium flex-1 p-2">
                <div class="flex w-full bg-base-200 p-3 items-center gap-2
                rounded-box border border-base-300">
                  <font-awesome-icon icon="fa-solid fa-user" />
                  Member 3
                </div>
              </div>

              <div class="flex items-center gap-2 badge badge-neutral
              rounded-box">
                Viewer
              </div>

              <div class="dropdown dropdown-right">

                <div tabindex="0" role="button" class="btn btn-sm btn-ghost">
                  ⋮
                </div>
                <ul tabindex="0" class="dropdown-content menu bg-base-200 
                border border-base-300 rounded-box 
                w-48 p-2 shadow">
                  <li>
                    <button class="flex gap-2">
                      <font-awesome-icon icon="fa-solid fa-pencil" />
                      Update
                    </button>
                  </li>
                  <li>
                    <button class="flex gap-2 text-error">
                      <font-awesome-icon icon="fa-solid fa-trash" />
                      Delete
                    </button>
                  </li>
                </ul>
              </div>
            </div>

          </div>

        </div>



      </div> -->
    </div>
    <LoadingScreen v-if="kanbanBoardStore.loading"></LoadingScreen>
  </div>
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import KanbanSideBar from './kanban/kanbanSideBar.vue'
import KanbanStage from './kanban/kanbanStage.vue'

import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'

export default {
  name: 'KanbanPage',
  components: {
    KanbanSideBar,
    KanbanStage,
    LoadingScreen,
  },

  data() {
    return {
      kanbanBoardStore: useKanbanBoardStore(),
    }
  },
}
</script>

<style scoped>
.bg-pattern {
  background-color: #07090b;
  opacity: 1;
  background-image: radial-gradient(#1d60c4 0.9px, #07090b 0.9px);
  background-size: 18px 18px;
}
</style>
