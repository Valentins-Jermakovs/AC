<template>
    <div class="w-4/5 bg-base-200 border border-base-300 p-1 mt-10">
        <ProjectStage></ProjectStage>
        <!-- Create new stage -->
        <div class="w-full flex items-center justify-center p-2">
            <button class="btn btn-primary">Create new stage</button>
        </div>
    </div>
</template>

<script>
import ProjectStage from './projectStage.vue';

export default {
    name: 'ProjectStageList',
    components: { ProjectStage }
}
</script>

<style scoped>
</style>