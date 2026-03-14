<template>
    <div class="w-full bg-base-200 flex items-center">
        <button class="btn btn-neutral">
          <font-awesome-icon icon="fa-solid fa-pen-to-square" />
          Change board title
        </button>
        <button class="btn btn-neutral">
          <font-awesome-icon icon="fa-solid fa-plus" />
          Add Stage
        </button>
        <button class="btn btn-neutral">
          <font-awesome-icon icon="fa-solid fa-trash" />
          Delete board
        </button>
      </div>
      <!-- Board space -->
      <div class="flex-1 flex w-full overflow-auto p-5">
        <kanbanStage></kanbanStage>
      </div>
</template>

<script>
import kanbanStage from './kanbanStage.vue';

export default {
    name: 'BoardSpace',
    components: {
        kanbanStage
    }
}
</script>

<style scoped>
</style>