<template>
  <div class="flex flex-col flex-1 items-center justify-center">
    <div class="flex flex-col items-center gap-5 p-8 bg-base-100 border border-base-300 w-full max-w-lg">
      <!-- Icon composition -->
      <div class="relative">
        <font-awesome-icon icon="fa-solid fa-diagram-project" class="text-7xl text-base-content/20" />

        <font-awesome-icon icon="fa-solid fa-triangle-exclamation"
          class="text-warning text-2xl absolute -top-2 -right-3" bounce />
      </div>

      <!-- Text -->
      <div class="text-center flex flex-col gap-2">
        <h2 class="text-xl font-semibold flex items-center justify-center gap-2 text-warning">
          <font-awesome-icon icon="fa-solid fa-folder-open" />

          {{ $t('work.projects.errors.projects_not_found') }}
        </h2>
      </div>

      <div class="divider my-1"></div>

      <!-- Action -->
      <button class="btn btn-primary gap-2" @click="showCreateDialog = true">
        <font-awesome-icon icon="fa-solid fa-plus" />

        {{ $t('work.projects.common.create_project') }}
      </button>

      <!-- Visual animation -->
      <progress class="progress progress-warning w-40"></progress>
    </div>
  </div>

  <base-dialog v-model="showCreateDialog" :title="$t('work.projects.modals.create_project.title')"
    :confirmText="$t('common.create')" :cancelText="$t('common.cancel')" @confirm="createProject" @cancel="resetForm">
    <div class="flex flex-col w-full gap-2">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="projectTitle" class="label">{{
        $t('work.projects.modals.create_project.name')
        }}</label>
      <input v-model="newProject.title" type="text" class="input input-bordered w-full"
        :placeholder="$t('work.projects.modals.create_project.name_placeholder')" />
      <label for="projectDescription" class="label">{{
        $t('work.projects.modals.create_project.description')
        }}</label>
      <div class="w-full flex justify-end text-sm opacity-70 pr-1">
        {{ descriptionRemainingChars }} / {{ descriptionMaxLength }}
      </div>
      <textarea v-model="newProject.description" class="textarea textarea-bordered w-full" maxlength="1000"
        :placeholder="$t('work.projects.modals.create_project.description_placeholder')"></textarea>
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
      descriptionMaxLength: 1000,
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

    descriptionRemainingChars() {
      return this.descriptionMaxLength - this.newProject.description.length
    },
  },
}
</script>
