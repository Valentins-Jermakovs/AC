<template>
    <div class="w-full flex gap-4 p-2 overflow-x-auto">
        <div v-for="stage in stagesStore.stages" :key="stage.id" class="min-w-72 flex flex-col rounded-box">
            <kanban-stage-title :stage="stage"></kanban-stage-title>
            <kanban-task-list :stage-id="stage.id" :board-id="boardStore.selectedBoard?.id"></kanban-task-list>
            <kanban-create-task></kanban-create-task>
        </div>
    </div>
</template>

<script>
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages';
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards';
import KanbanTask from './kanbanTask.vue';
import KanbanStageTitle from './kanbanStageTitle.vue';
import KanbanTaskList from './kanbanTaskList.vue';
import KanbanCreateTask from './kanbanCreateTask.vue';

export default {
    components: {
        KanbanTask,
        KanbanStageTitle,
        KanbanTaskList,
        KanbanCreateTask
    },
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
