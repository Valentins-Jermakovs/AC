<template>
  <div
    class="w-full flex flex-col md:flex-row items-center gap-3 md:gap-5 justify-between p-2 bg-base-100 border border-base-300"
  >
    <!-- Create -->
    <button class="btn btn-primary w-full md:w-auto" @click="showCreateDialog = true">
      <font-awesome-icon icon="fa-solid fa-plus" />
      {{ $t('work.projects.common.create_project') }}
    </button>

    <!-- Search -->
    <div class="flex flex-col md:flex-row gap-2 flex-1 w-full sm:justify-between">
      <input
        v-model="store.searchQuery"
        type="text"
        class="input input-bordered w-full"
        :placeholder="$t('common.search')"
        @keyup.enter="search"
        :disabled="store.searchMode === 'all'"
      />
      <select
        v-model="store.searchMode"
        class="select select-bordered w-full bg-neutral text-neutral-content md:w-auto"
      >
        <option value="all">{{ $t('filters.all') }}</option>
        <option value="title">{{ $t('filters.by_title') }}</option>
      </select>
      <button
        class="btn btn-primary w-full md:w-auto"
        @click="search"
        :disabled="store.searchMode === 'title' && store.searchQuery.length < 3"
      >
        <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
      </button>
    </div>
  </div>

  <!-- Create dialog -->
  <base-dialog
    v-model="showCreateDialog"
    :title="$t('work.projects.modals.create_project.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="createProject"
    @cancel="closeCreateProject"
  >
    <div class="flex flex-col w-full gap-3">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label class="label">
        <span class="label-text">
          {{ $t('work.projects.modals.create_project.name') }}
        </span>
      </label>
      <input
        v-model="newProject.title"
        type="text"
        class="input input-bordered w-full"
        :placeholder="$t('work.projects.modals.create_project.name_placeholder')"
      />
      <label class="label">
        <span class="label-text">
          {{ $t('work.projects.modals.create_project.description') }}
        </span>
      </label>
      <textarea
        v-model="newProject.description"
        class="textarea textarea-bordered w-full min-h-52"
        :placeholder="$t('work.projects.modals.create_project.description_placeholder')"
      ></textarea>
    </div>
  </base-dialog>
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useUserStore } from '@/stores/user'
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'TopBar',

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
    async search() {
      this.store.meta.page = 1

      if (this.store.searchMode === 'all') {
        await this.store.getAllProjects()
        return
      }

      if (this.store.searchMode === 'title') {
        await this.store.getProjectsByTitle()
      }
    },

    async closeCreateProject() {
      this.showCreateDialog = false
      this.resetForm()
      await this.store.clearError()
    },

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
        console.error(err)
      } finally {
        this.resetForm()
      }
    },

    resetForm() {
      this.newProject = {
        title: '',
        description: '',
      }
    },
  },

  mounted() {
    this.userStore.fetchMe()
  },

  computed: {
    error() {
      return this.store.error
    },
  },
}
</script>
