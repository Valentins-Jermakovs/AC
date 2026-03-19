<template>
    <div class="flex-1 flex flex-col items-center gap-3 overflow-y-scroll p-2">
        <projects-list-item></projects-list-item>
    </div>
</template>

<script>
import ProjectsListItem from './projectsListItem.vue';

export default {
    name: 'ProjectsList',
    components: {
        ProjectsListItem
    }
}
</script>

<style scoped>
</style>