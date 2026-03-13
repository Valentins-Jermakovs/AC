<template>
  <div class="flex flex-1 w-full h-full">
    <KanbanSideBar></KanbanSideBar>
    <div class="flex flex-col flex-1 w-full h-full">
      <div class="w-full bg-base-200 border border-base-300 h-14 flex gap-2
      items-center pl-3 p-1">
        <button class="btn btn-neutral">
          Change board title
        </button>
        <button class="btn btn-secondary">
          Add Stage
        </button>
        <button class="btn btn-warning">
          Delete board
        </button>
        <button class="btn btn-warning">
          Leave board
        </button>
      </div>
      <!-- Board space -->
      <div class="flex-1 flex w-full h-full overflow-auto p-5">
        <KanbanStage></KanbanStage>
      </div>
    </div>
  </div>
</template>

<script>
import KanbanSideBar from './kanban/kanbanSideBar.vue';
import KanbanStage from './kanban/kanbanStage.vue';

export default {
  name: 'KanbanPage',
  components: {
    KanbanSideBar,
    KanbanStage,
  },
};

</script>

<style scoped></style>
