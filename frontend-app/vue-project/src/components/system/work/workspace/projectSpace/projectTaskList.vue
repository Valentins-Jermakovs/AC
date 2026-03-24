<template>
  <div class="p-2 sm:p-3 flex flex-col bg-base-200 border border-base-300 rounded-box gap-3">
    <!-- Tasks -->
    <div class="flex flex-col gap-3 w-full">
      <ProjectTask
        v-for="task in tasksStore.getTasksByStage(stage.id)"
        :key="task.id"
        :task="task"
      />
    </div>

    <!-- Create -->
    <div class="w-full flex justify-center pt-2">
      <button class="btn btn-primary w-full sm:w-auto" @click="openCreateDialog">
        <font-awesome-icon icon="fa-solid fa-plus" />

        <span class="hidden sm:inline"> Create new task </span>

        <span class="sm:hidden"> New task </span>
      </button>
    </div>
  </div>

  <!-- CREATE -->
  <BaseDialog
    v-model="createDialog"
    title="Create task"
    confirmText="Create"
    cancelText="Cancel"
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
        <label class="label"> Title </label>

        <input v-model="form.title" class="input input-bordered w-full" placeholder="Task title" />
      </div>

      <div>
        <label class="label"> Description </label>

        <textarea
          v-model="form.description"
          class="textarea textarea-bordered w-full min-h-30 sm:min-h-52"
          placeholder="Description"
        ></textarea>
      </div>

      <!-- Priority + SP -->
      <div class="flex flex-col sm:flex-row gap-3">
        <div class="flex flex-col flex-1">
          <label class="label"> Priority </label>

          <select v-model="form.priority" class="select select-bordered w-full">
            <option :value="1">Priority 1</option>
            <option :value="2">Priority 2</option>
            <option :value="3">Priority 3</option>
            <option :value="4">Priority 4</option>
            <option :value="5">Priority 5</option>
            <option :value="6">Priority 6</option>
            <option :value="7">Priority 7</option>
            <option :value="8">Priority 8</option>
            <option :value="9">Priority 9</option>
            <option :value="10">Priority 10</option>
          </select>
        </div>

        <div class="flex flex-col flex-1">
          <label class="label"> Story Points </label>

          <select v-model="form.storyPoints" class="select select-bordered w-full">
            <option :value="1">1 SP</option>
            <option :value="2">2 SP</option>
            <option :value="3">3 SP</option>
            <option :value="5">5 SP</option>
            <option :value="8">8 SP</option>
            <option :value="13">13 SP</option>
            <option :value="21">21 SP</option>
            <option :value="34">34 SP</option>
            <option :value="55">55 SP</option>
            <option :value="89">89 SP</option>
            <option :value="144">144 SP</option>
          </select>
        </div>
      </div>

      <!-- Status -->
      <div>
        <label class="label"> Status </label>

        <select v-model="form.status" class="select select-bordered w-full">
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>

      <!-- Due date -->
      <div>
        <label class="label"> Due date </label>

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
import LoadingScreen from '@/components/common/LoadingScreen.vue';

export default {
  name: 'ProjectTaskList',

  components: {
    ProjectTask,
    BaseDialog,
    LoadingScreen
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

      createDialog: false,

      form: {
        title: '',
        description: '',
        priority: 1,
        storyPoints: 1,
        status: 'todo',
        dueDate: null,
      },
    }
  },

  computed: {
    error() {
      return this.tasksStore.error
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
          projectId: this.projectsStore.selectedProject.id,
          stageId: this.stage.id,
        }

        await this.tasksStore.createTask(payload)

        this.createDialog = false
      } catch (e) {
        console.error(e)
      }
    },
  },
}
</script>
