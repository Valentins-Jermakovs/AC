<template>
  <div
    class="w-full p-2 flex flex-wrap bg-base-100 border border-base-300 gap-2 items-center"
  >
    <!-- Project view -->
    <button
      class="btn flex-1 sm:flex-none"
      :class="activeView === 'project' ? 'btn-primary' : 'btn-neutral'"
      @click="$emit('update:activeView', 'project')"
    >
      <font-awesome-icon icon="fa-solid fa-list" />
      <span class="hidden sm:inline">Project view</span>
    </button>

    <!-- Members -->
    <button
      v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'owner'"
      class="btn flex-1 sm:flex-none"
      :class="activeView === 'members' ? 'btn-primary' : 'btn-neutral'"
      @click="$emit('update:activeView', 'members')"
    >
      <font-awesome-icon icon="fa-solid fa-users" />
      <span class="hidden sm:inline">Members view</span>
    </button>

    <!-- Delete -->
    <button
      v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'owner'"
      class="btn btn-neutral flex-1 sm:flex-none sm:ml-auto"
      @click="showDelete = true"
    >
      <font-awesome-icon icon="fa-solid fa-trash" />
      <span class="hidden md:inline">Delete project</span>
    </button>

    <!-- Leave -->
    <button
      v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role !== 'owner'"
      class="btn btn-neutral flex-1 sm:flex-none sm:ml-auto"
    >
      <font-awesome-icon icon="fa-solid fa-arrow-right-from-bracket" />
      <span class="hidden md:inline">Leave project</span>
    </button>

    <!-- Back -->
    <button
      class="btn btn-neutral w-full sm:w-auto"
      @click="goToProjects"
    >
      <font-awesome-icon icon="fa-solid fa-arrow-left" />
      <span>Back</span>
      <span class="hidden md:inline">to projects list</span>
    </button>
  </div>

  <!-- Delete dialog -->
  <base-dialog
    v-model="showDelete"
    title="Delete project"
    confirmText="Delete"
    cancelText="Cancel"
    @confirm="deleteProject"
  >
    <p>Are you sure you want to delete this project?</p>
  </base-dialog>
</template>

<script>
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  components: { BaseDialog },

  props: {
    activeView: {
      type: String,
      default: 'project',
    },
  },

  data() {
    return {
      kanbanMembersStore: useWorkspaceProjectMembersStore(),
      store: useWorkspaceProjectsStore(),

      showDelete: false,
    }
  },

  methods: {
    goToProjects() {
      this.store.selectedProject = null
      this.kanbanMembersStore.projectId = null
    },
    async deleteProject() {
      await this.store.deleteProject({
        projectId: this.store.selectedProject.id,
      })
      this.showDelete = false
      this.goToProjects()
    },
  },

  mounted() {
    this.kanbanMembersStore.fetchMe()
  },
}
</script>
