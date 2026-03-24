<template>
  <div class="flex flex-col flex-1 items-center justify-center gap-5">
    <h2 class="text-2xl flex items-center gap-3">
      <font-awesome-icon icon="fa-solid fa-triangle-exclamation" size="2xl" class="text-warning" />

      You don't have any projects
    </h2>

    <button class="btn btn-primary" @click="showCreateDialog = true">Create project</button>
  </div>

  <base-dialog
    v-model="showCreateDialog"
    title="Create project"
    confirmText="Create"
    cancelText="Cancel"
    @confirm="createProject"
    @cancel="resetForm"
  >
    <div class="flex flex-col w-full gap-2">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="projectTitle" class="label">Project title</label>
      <input
        v-model="newProject.title"
        type="text"
        class="input input-bordered w-full"
        placeholder="Project title"
      />
      <label for="projectDescription" class="label">Project description</label>
      <textarea
        v-model="newProject.description"
        class="textarea textarea-bordered w-full min-h-52"
        placeholder="Project description"
      ></textarea>
    </div>
  </base-dialog>
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useUserStore } from '@/stores/user'
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'EmptyProjectsList',

  components: {
    BaseDialog,
  },

  data() {
    return {
      store: useWorkspaceProjectsStore(),
      userStore: useUserStore(),

      showCreateDialog: false,

      newProject: {
        title: '',
        description: '',
      },
    }
  },

  methods: {
    async createProject() {

      const payload = {
        title: this.newProject.title,
        description: this.newProject.description,
        email: this.userStore.email,
      }

      try {
        await this.store.createProject(payload)
        this.showCreateDialog = false
      } catch (err) {
        throw err
      }
    },

    resetForm() {
      this.newProject = {
        title: '',
        description: '',
      }
      this.store.clearError()
    },
  },

  computed: {
    error() {
      return this.store.error
    },
  },
}
</script>
