<template>
  <div
    class="w-full max-w-xl bg-base-100 border border-base-300 rounded-box flex flex-col gap-3 p-3 sm:p-4 hover:border-info hover:bg-base-200 transition-all duration-300">
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

      <div class="flex flex-row sm:gap-2 justify-start sm:justify-end gap-1 flex-wrap">
        <button class="btn btn-ghost btn-sm" @click="openEdit">
          <font-awesome-icon icon="fa-solid fa-pen-to-square" />
        </button>

        <button class="btn btn-ghost btn-sm text-error" @click="openDelete">
          <font-awesome-icon icon="fa-solid fa-trash" />
        </button>
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
        Enter project
      </button>
    </div>
  </div>

  <!-- EDIT -->
  <base-dialog v-model="showEdit" title="Edit project" confirmText="Save" cancelText="Cancel" @confirm="updateProject"
    @cancel="resetEdit">
    <div class="flex flex-col w-full gap-2">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label class="label">
        <span class="label-text">Title</span>
      </label>
      <input v-model="editProject.title" type="text" class="input input-bordered w-full" />
      <label class="label">
        <span class="label-text">Description</span>
      </label>
      <textarea v-model="editProject.description"
        class="textarea textarea-bordered w-full min-h-40 sm:min-h-52"></textarea>
    </div>
  </base-dialog>

  <!-- DELETE -->
  <base-dialog v-model="showDelete" title="Delete project" confirmText="Delete" cancelText="Cancel"
    @confirm="deleteProject">
    <p>Are you sure you want to delete this project?</p>
  </base-dialog>
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
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

      showEdit: false,
      showDelete: false,

      editProject: {
        title: '',
        description: '',
        projectId: '',
      },
    }
  },

  methods: {
    openEdit() {
      this.editProject = {
        title: this.project.title,
        description: this.project.description,
        projectId: this.project.id,
      }

      this.showEdit = true
    },

    openDelete() {
      this.showDelete = true
    },

    async updateProject() {

      if (!this.editProject.title) {
        this.store.error = 'Title is required'
        return
      }

      try {
        await this.store.updateProject(this.editProject)
        this.showEdit = false
        this.showEdit = false
      } catch (err) {
        console.error(err)
      }
    },

    async deleteProject() {
      await this.store.deleteProject({
        projectId: this.project.id,
      })

      this.showDelete = false
    },

    async resetEdit() {
      this.editProject = {
        title: '',
        description: '',
        projectId: '',
      }
      await this.store.clearError()
    },

    openProject() {
      this.store.selectedProject = this.project
      this.kanbanMembersStore.projectId = this.project.id
    },
  },
  computed: {
    error() {
      return this.store.error
    },
  },
}
</script>
