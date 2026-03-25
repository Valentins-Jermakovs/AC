<template>
  <div
    class="w-full bg-base-100 border border-base-300 flex flex-col gap-3 p-3 sm:p-4 hover:border-info hover:bg-base-300 transition-all duration-300"
  >
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 sm:gap-3">
      <div class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
        <h2 class="text-lg sm:text-xl font-semibold truncate">
          {{ project.title }}
        </h2>

        <p class="text-xs sm:text-sm badge badge-neutral rounded-box">
          {{ project.createdAt }}
        </p>
      </div>
    </div>

    <!-- Description -->
    <p class="text-base-content/70 text-sm sm:text-base line-clamp-3">
      {{ project.description }}
    </p>

    <!-- Actions -->
    <div class="flex justify-end">
      <button class="btn btn-primary w-full sm:w-auto btn-sm gap-2" @click="openProject">
        <font-awesome-icon icon="fa-solid fa-arrow-right" />
        {{ $t('work.projects.common.enter_project') }}
      </button>
    </div>
  </div>

  
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import { useSelectedProjectStore } from '@/stores/selectedProject';
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'ProjectsListItem',

  components: {
    BaseDialog,
  },

  props: {
    project: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      store: useWorkspaceProjectsStore(),
      kanbanMembersStore: useWorkspaceProjectMembersStore(),
      selectedProjectStore: useSelectedProjectStore(),
    }
  },

  methods: {
    openProject() {
      this.store.selectedProject = this.project
      this.kanbanMembersStore.projectId = this.project.id

      const payload = {
        workspaceId: this.project.id,
        workspaceTitle: this.project.title
      }

      this.selectedProjectStore.setSelectedProject(payload)
    },
  },
  computed: {
    error() {
      return this.store.error
    },
  },
}
</script>
