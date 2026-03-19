<template>
    <div class="flex-1 flex flex-col items-center gap-3 overflow-y-scroll p-2">
        <projects-list-item v-for="project in projectsStore.projects" :key="project.id" :project="project">
        </projects-list-item>
    </div>
</template>

<script>
import ProjectsListItem from './projectsListItem.vue';
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects';
export default {
    name: 'ProjectsList',
    components: {
        ProjectsListItem
    },

    data() {
        return {
            projectsStore: useWorkspaceProjectsStore(),
        }
    }
}
</script>

<style scoped>
</style>