<template>
  <div class="w-full flex justify-center p-2 sm:p-4">
    <div class="w-full max-w-7xl bg-base-200 border border-base-300 p-2 sm:p-4 flex flex-col gap-3">
      <!-- Stages list -->
      <div class="flex flex-col gap-3">
        <ProjectStage v-for="stage in stagesStore.projectStages" :key="stage.id" :stage="stage" />
      </div>

      <!-- Create stage -->
      <div class="w-full flex flex-col gap-2 justify-center pt-2">
        <!-- Empty state -->
        <div
          v-if="!stagesStore.loading && stagesStore.projectStages.length === 0"
          class="flex flex-col items-center gap-3 text-base-content/60 p-6 border border-base-300 w-full bg-base-100"
        >
          <!-- Icon -->
          <div class="relative">
            <font-awesome-icon
              icon="fa-solid fa-flag-checkered"
              class="text-6xl text-base-content/20"
            />

            <font-awesome-icon
              icon="fa-solid fa-circle-exclamation"
              class="text-warning text-xl absolute -top-1 -right-2"
              bounce
            />
          </div>

          <!-- Text -->
          <div class="flex flex-col items-center text-center">
            <h3 class="font-semibold text-lg flex items-center gap-2">
              <font-awesome-icon icon="fa-solid fa-list" />
              {{ $t('work.projects.errors.no_sprints') }}
            </h3>
          </div>

          <!-- Animated progress -->
          <progress class="progress progress-warning w-32"></progress>
        </div>

        <button
          class="btn btn-primary w-full md:w-auto"
          @click="showDialog = true"
          :disabled="membersStore.currentUser?.role === 'viewer'"
        >
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
        <div class="w-full flex justify-end text-sm opacity-70 pr-1">
          {{ descriptionRemainingChars }} / {{ descriptionMaxLength }}
        </div>
        <textarea
          maxlength="1000"
          v-model="newStage.description"
          class="textarea w-full"
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
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'ProjectStageList',
  components: { ProjectStage, BaseDialog, LoadingScreen },

  data() {
    return {
      stagesStore: useWorkspaceProjectStagesStore(),
      projectsStore: useWorkspaceProjectsStore(),
      membersStore: useWorkspaceProjectMembersStore(),
      descriptionMaxLength: 1000,

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
    descriptionRemainingChars() {
      return this.descriptionMaxLength - (this.newStage.description?.length || 0)
    },
    error() {
      return this.stagesStore.error
    },
  },
}
</script>

<style scoped></style>
