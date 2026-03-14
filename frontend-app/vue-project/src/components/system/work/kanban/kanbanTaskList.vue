<template>
    <!-- Tasks list (scrollable) -->
    <div class="w-full flex flex-col gap-2 p-2 bg-base-200">
        <kanban-task></kanban-task>
    </div>
</template>

<script>
import KanbanTask from './kanbanTask.vue';

export default {
    components: {
        KanbanTask
    }
}
</script>