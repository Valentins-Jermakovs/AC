<template>
    <div class="p-2 flex flex-col items-center bg-base-200 rounded-box border
    border-base-300">
        <ProjectTask></ProjectTask>
        <!-- Create new task -->
        <div class="w-full flex items-center justify-center p-2">
            <button class="btn btn-primary">Create new task</button>
        </div>
    </div>
</template>

<script>
import ProjectTask from './projectTask.vue';

export default {
    name: 'ProjectTaskList',
    components: { ProjectTask }
}
</script>

<style scoped></style>