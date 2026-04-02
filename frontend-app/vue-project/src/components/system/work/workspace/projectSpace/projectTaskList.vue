<template>
  <div class="p-2 sm:p-3 flex flex-col bg-base-200 border border-base-300 gap-3">
    <!-- Tasks -->
    <div class="flex flex-col gap-3 w-full">
      <ProjectTask
        v-for="task in tasksStore.getTasksByStage(stage.id)"
        :key="task.id"
        :task="task"
      />
    </div>

    <!-- Create -->
    <div class="w-full flex flex-col justify-center pt-2">
      <div
        v-if="tasksStore.getTasksByStage(stage.id).length === 0"
        class="flex flex-col items-center justify-center gap-4 text-center p-4"
      >
        <font-awesome-icon
          bounce
          icon="fa-solid fa-triangle-exclamation"
          size="3x"
          class="text-warning animate-spin-slow"
        />

        <h2 class="text-lg font-semibold flex items-center gap-2 text-base-content/80">
          <font-awesome-icon icon="fa-solid fa-list-check" />
          {{ $t('work.projects.errors.no_user_stories') }}
        </h2>

        <progress class="progress progress-warning w-32"></progress>
      </div>
      <button
        :disabled="membersStore.currentUser?.role === 'viewer'"
        class="btn btn-primary w-full sm:w-auto"
        @click="openCreateDialog"
      >
        <font-awesome-icon icon="fa-solid fa-plus" />

        <span class="hidden sm:inline">
          {{ $t('work.projects.common.create_new_user_story') }}
        </span>

        <span class="sm:hidden">
          {{ $t('work.projects.common.create_new_user_story') }}
        </span>
      </button>
    </div>
  </div>

  <!-- CREATE -->
  <BaseDialog
    v-model="createDialog"
    :title="$t('work.projects.modals.create_user_story.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="createTask"
    @cancel="closeCreateDialog"
  >
    <div class="flex flex-col gap-3 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <div>
        <label class="label">
          {{ $t('work.projects.modals.create_user_story.name') }}
        </label>

        <input
          v-model="form.title"
          class="input input-bordered w-full"
          :placeholder="$t('work.projects.modals.create_user_story.name_placeholder')"
        />
      </div>

      <div>
        <label class="label">
          {{ $t('work.projects.modals.create_user_story.description') }}
        </label>
        <div class="w-full flex justify-end text-sm opacity-70 pr-1">
          {{ descriptionRemainingChars }} / {{ descriptionMaxLength }}
        </div>
        <textarea
          maxlength="1000"
          v-model="form.description"
          class="textarea textarea-bordered w-full"
          :placeholder="$t('work.projects.modals.create_user_story.description_placeholder')"
        ></textarea>
      </div>

      <!-- Priority + SP -->
      <div class="flex flex-col sm:flex-row gap-3">
        <div class="flex flex-col flex-1">
          <label class="label">
            {{ $t('work.projects.modals.create_user_story.priority') }}
          </label>

          <select v-model="form.priority" class="select select-bordered w-full">
            <option :value="1">1</option>
            <option :value="2">2</option>
            <option :value="3">3</option>
            <option :value="4">4</option>
            <option :value="5">5</option>
            <option :value="6">6</option>
            <option :value="7">7</option>
            <option :value="8">8</option>
            <option :value="9">9</option>
            <option :value="10">10</option>
          </select>
        </div>

        <div class="flex flex-col flex-1">
          <label class="label">
            {{ $t('work.projects.modals.create_user_story.story_points') }}
          </label>

          <select v-model="form.storyPoints" class="select select-bordered w-full">
            <option :value="1">1</option>
            <option :value="2">2</option>
            <option :value="3">3</option>
            <option :value="5">5</option>
            <option :value="8">8</option>
            <option :value="13">13</option>
            <option :value="21">21</option>
            <option :value="34">34</option>
            <option :value="55">55</option>
            <option :value="89">89</option>
            <option :value="144">144</option>
          </select>
        </div>
      </div>

      <!-- Status -->
      <div>
        <label class="label">
          {{ $t('work.projects.modals.create_user_story.status') }}
        </label>

        <select v-model="form.status" class="select select-bordered w-full">
          <option value="todo">{{ $t('work.projects.common.todo') }}</option>
          <option value="in_progress">{{ $t('work.projects.common.in_progress') }}</option>
          <option value="done">{{ $t('work.projects.common.done') }}</option>
        </select>
      </div>

      <!-- Created at -->
      <div>
        <label class="label">
          {{ $t('work.projects.modals.create_user_story.start_date') }}
        </label>

        <input type="date" v-model="form.createdAt" class="input input-bordered w-full" />
      </div>

      <!-- Due date -->
      <div>
        <label class="label">
          {{ $t('work.projects.modals.create_user_story.due_date') }}
        </label>

        <input type="date" v-model="form.dueDate" class="input input-bordered w-full" />
      </div>
    </div>
  </BaseDialog>

  <LoadingScreen v-if="tasksStore.loading"></LoadingScreen>
</template>

<script>
import ProjectTask from './projectTask.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'

import { useWorkspaceProjectsTasksStore } from '@/stores/workspace/projectsTasks'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'ProjectTaskList',

  components: {
    ProjectTask,
    BaseDialog,
    LoadingScreen,
  },

  props: {
    stage: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      tasksStore: useWorkspaceProjectsTasksStore(),
      projectsStore: useWorkspaceProjectsStore(),
      membersStore: useWorkspaceProjectMembersStore(),
      descriptionMaxLength: 1000,

      createDialog: false,

      form: {
        title: '',
        description: '',
        priority: 1,
        storyPoints: 1,
        status: 'todo',
        dueDate: null,
        createdAt: null,
      },
    }
  },

  computed: {
    error() {
      return this.tasksStore.error
    },
    descriptionRemainingChars() {
      return this.descriptionMaxLength - (this.form.description?.length || 0)
    },
  },

  mounted() {
    this.tasksStore.projectId = this.projectsStore.selectedProject.id

    this.tasksStore.getTasks(this.stage.id)
  },

  methods: {
    closeCreateDialog() {
      this.createDialog = false

      this.form = {
        title: '',
        description: '',
        priority: 1,
        storyPoints: 1,
        status: 'todo',
        dueDate: null,
      }

      this.tasksStore.clearError()
    },
    openCreateDialog() {
      this.form = {
        title: '',
        description: '',
        priority: 1,
        storyPoints: 1,
        status: 'todo',
        dueDate: null,
      }

      this.createDialog = true
    },

    async createTask() {
      if (!this.form.dueDate) {
        this.tasksStore.error = 'Task due date is required'
        return
      }

      try {
        const payload = {
          title: this.form.title,
          description: this.form.description,
          priority: this.form.priority,
          storyPoints: this.form.storyPoints,
          status: this.form.status,
          dueDate: this.form.dueDate,
          createdAt: this.form.createdAt,
          projectId: this.projectsStore.selectedProject.id,
          stageId: this.stage.id,
        }

        await this.tasksStore.createTask(payload)

        this.createDialog = false

        this.form = {
          title: '',
          description: '',
          priority: 1,
          storyPoints: 1,
          status: 'todo',
          dueDate: null,
        }
      } catch (e) {
        console.error(e)
      }
    },
  },
}
</script>
