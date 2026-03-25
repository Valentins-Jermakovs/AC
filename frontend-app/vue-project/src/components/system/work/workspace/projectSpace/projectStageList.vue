<template>
  <div class="w-full flex justify-center p-2 sm:p-4">
    <div class="w-full max-w-7xl bg-base-200 border border-base-300 p-2 sm:p-4 flex flex-col gap-3">
      <!-- Stages list -->
      <div class="flex flex-col gap-3">
        <ProjectStage v-for="stage in stagesStore.projectStages" :key="stage.id" :stage="stage" />
      </div>

      <!-- Create stage -->
      <div class="w-full flex justify-center pt-2">
        <button class="btn btn-primary w-full sm:w-auto" @click="showDialog = true">
          <font-awesome-icon icon="fa-solid fa-plus" />

          <span class="hidden sm:inline">
            {{ $t('work.projects.common.create_new_sprint') }}
          </span>

          <span class="sm:hidden">
            {{ $t('work.projects.common.create_new_sprint') }}
          </span>
        </button>
      </div>
    </div>
  </div>

  <!-- Dialog -->
  <BaseDialog
    v-model="showDialog"
    :title="$t('work.projects.modals.create_new_sprint.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="handleCreate"
    @cancel="closeCreateDialog"
  >
    <div class="flex flex-col gap-3 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error">
            {{ error }}
          </h1>
        </div>
      </Transition>

      <div class="flex flex-col gap-1">
        <label class="label">
          {{ $t('work.projects.modals.create_new_sprint.name') }}
        </label>

        <input
          v-model="newStage.title"
          type="text"
          class="input w-full"
          :placeholder="$t('work.projects.modals.create_new_sprint.name_placeholder')"
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="label">
          {{ $t('work.projects.modals.create_new_sprint.description') }}
        </label>

        <textarea
          v-model="newStage.description"
          class="textarea w-full min-h-52"
          :placeholder="$t('work.projects.modals.create_new_sprint.description_placeholder')"
        ></textarea>
      </div>

      <div class="flex flex-col gap-1">
        <label class="label">
          {{ $t('work.projects.modals.create_new_sprint.start_date') }}
        </label>

        <input v-model="newStage.createdAt" type="date" class="input w-full" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="label">
          {{ $t('work.projects.modals.create_new_sprint.due_date') }}
        </label>

        <input v-model="newStage.dueDate" type="date" class="input w-full" />
      </div>
    </div>
  </BaseDialog>

  <LoadingScreen v-if="stagesStore.loading"></LoadingScreen>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import ProjectStage from './projectStage.vue'
import { useWorkspaceProjectStagesStore } from '@/stores/workspace/projectStages'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'ProjectStageList',
  components: { ProjectStage, BaseDialog, LoadingScreen },

  data() {
    return {
      stagesStore: useWorkspaceProjectStagesStore(),
      projectsStore: useWorkspaceProjectsStore(),

      showDialog: false,
      newStage: {
        title: '',
        description: '',
        dueDate: '',
        createdAt: '',
      },
    }
  },

  mounted() {
    this.stagesStore.projectId = this.projectsStore.selectedProject.id
    if (this.stagesStore.projectId) {
      this.stagesStore.getStages()
    }
  },

  methods: {
    closeCreateDialog() {
      this.showDialog = false
      this.newStage = {
        title: '',
        description: '',
        dueDate: '',
      }
      this.stagesStore.clearError()
    },
    async handleCreate() {
      if (!this.newStage.dueDate) {
        this.stagesStore.error = 'Stage due date is required'
        return
      }

      const payload = {
        title: this.newStage.title,
        description: this.newStage.description,
        dueDate: this.newStage.dueDate,
        createdAt: this.newStage.createdAt,
        projectId: this.stagesStore.projectId,
      }

      try {
        await this.stagesStore.createStage(payload)

        // Reset form and close dialog
        this.newStage = { title: '', description: '', dueDate: '', createdAt: '' }
        this.showDialog = false
      } catch (err) {
        console.error(err)
      }
    },
  },
  computed: {
    error() {
      return this.stagesStore.error
    },
  },
}
</script>

<style scoped></style>
