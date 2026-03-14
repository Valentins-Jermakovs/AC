<template>
    <div class="w-full flex gap-4 p-2 overflow-x-auto">
        <div v-for="stage in stagesStore.stages" :key="stage.id" class="min-w-72 flex flex-col rounded-box">
            <kanban-stage-title :stage="stage"></kanban-stage-title>

            <!-- Pārsūti event uz task list -->
            <kanban-task-list
  :stage-id="stage.id"
  :board-id="boardStore.selectedBoard?.id"
  ref="taskLists"
  @task-updated="onTaskUpdated"
  @task-moved="reloadStageTasks"
/>

<kanban-create-task
  :stage-id="stage.id"
  :board-id="boardStore.selectedBoard?.id"
  @task-created="onTaskCreated"
/>
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
    },
methods: {
  async onTaskCreated() {
    await this.reloadStageTasks()
  },
  async onTaskUpdated() {
    await this.reloadStageTasks()
  },
  async reloadStageTasks() {
    if (!this.$refs.taskLists) return
    const lists = Array.isArray(this.$refs.taskLists)
        ? this.$refs.taskLists
        : [this.$refs.taskLists]
    for (const list of lists) await list.loadTasks()
  }
}
}
</script>

<style scoped></style>
