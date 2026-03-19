<template>
  <div class="w-full p-2 flex bg-base-200 border border-base-300 gap-2">
    <!-- Project view button -->
    <button
      class="btn"
      :class="activeView === 'project' ? 'btn-primary' : 'btn-neutral'"
      @click="$emit('update:activeView', 'project')"
    >
      <font-awesome-icon icon="fa-solid fa-list" /> Project view
    </button>

    <button
      v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'owner'"
      class="btn"
      :class="activeView === 'members' ? 'btn-primary' : 'btn-neutral'"
      @click="$emit('update:activeView', 'members')"
    >
      <font-awesome-icon icon="fa-solid fa-users" /> Members view
    </button>

    <!-- Delete / Leave buttons -->
    <button
      v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'owner'"
      class="btn btn-neutral"
      @click="showDelete = true"
    >
      <font-awesome-icon icon="fa-solid fa-trash" />
      Delete project
    </button>

    <button
      v-if="kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role !== 'owner'"
      class="btn btn-neutral"
    >
      <font-awesome-icon icon="fa-solid fa-arrow-right-from-bracket" />
      Leave project
    </button>

    <!-- Back button -->
    <button class="btn btn-neutral" @click="goToProjects">
      <font-awesome-icon icon="fa-solid fa-arrow-left" />
      Back to projects list
    </button>
  </div>

  <!-- Delete confirmation dialog -->
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
