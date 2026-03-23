<template>
  <div class="drawer drawer-end">
    <input
      :id="'task-info-drawer-' + task.id"
      type="checkbox"
      class="drawer-toggle"
    />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div
        class="w-full bg-base-100 border border-base-300 
        rounded-box
        p-3 sm:p-4 
        flex flex-col sm:flex-row 
        gap-3"
      >
        <!-- LEFT -->
        <div class="flex flex-col gap-3 flex-1">

          <div class="flex items-start sm:items-center gap-3">
            <h3 class="font-medium text-sm sm:text-base wrap-break-word">
              {{ task.title }}
            </h3>
          </div>

          <!-- META -->
          <div class="flex flex-wrap gap-2 text-xs">

            <div class="badge badge-primary badge-outline gap-1">
              <font-awesome-icon icon="fa-solid fa-tag" />
              {{ task.status }}
            </div>

            <div class="badge badge-neutral gap-1">
              <font-awesome-icon icon="fa-solid fa-bolt" />
              SP {{ task.storyPoints }}
            </div>

            <div class="badge badge-secondary gap-1">
              <font-awesome-icon icon="fa-solid fa-sort" />
              P{{ task.priority }}
            </div>

            <div class="badge badge-neutral gap-1">
              <font-awesome-icon icon="fa-solid fa-calendar" />
              {{ task.createdAt }}
            </div>

            <div class="badge badge-warning gap-1">
              <font-awesome-icon icon="fa-solid fa-clock" />
              {{ task.dueDate }}
            </div>

          </div>

          <!-- DESCRIPTION -->
          <div
            class="p-3 sm:p-4 
            bg-base-200 
            border border-base-300 
            rounded-box"
          >
            <p class="text-sm line-clamp-3 wrap-break-word">
              {{ task.description }}
            </p>
          </div>

        </div>

        <!-- OPEN -->
        <div class="flex sm:flex-col justify-end">
          <label
            :for="'task-info-drawer-' + task.id"
            class="btn btn-neutral btn-circle"
          >
            <font-awesome-icon icon="fa-solid fa-link" />
          </label>
        </div>

      </div>
    </div>

    <!-- DRAWER -->
    <div class="drawer-side z-50">

      <label
        :for="'task-info-drawer-' + task.id"
        class="drawer-overlay"
      ></label>

      <div
        class="bg-base-100 border border-base-300 
        min-h-full 
        w-full sm:w-96
        p-4 sm:p-6
        flex flex-col gap-6
        overflow-y-auto"
      >

        <!-- HEADER -->
        <div class="flex justify-between items-start gap-3">
          <h2 class="text-lg sm:text-xl font-semibold wrap-break-word">
            {{ task.title }}
          </h2>

          <label
            :for="'task-info-drawer-' + task.id"
            class="btn btn-ghost btn-sm btn-circle"
          >
            ✕
          </label>
        </div>

        <!-- ACTIONS -->
        <div class="bg-base-200 border border-base-300 rounded-box">

          <ul class="menu w-full">

            <li>
              <button
                class="flex gap-3 items-center"
                @click="openCreateDialog"
              >
                <font-awesome-icon icon="fa-solid fa-plus"/>
                Create task
              </button>
            </li>

            <li>
              <button
                class="flex gap-3 items-center"
                @click="openEditDialog"
              >
                <font-awesome-icon icon="fa-solid fa-pen"/>
                Edit task
              </button>
            </li>

            <li class="border-t border-base-300 mt-2 pt-2">
              <button
                class="text-error flex gap-3 items-center"
                @click="openDeleteDialog"
              >
                <font-awesome-icon icon="fa-solid fa-trash"/>
                Delete task
              </button>
            </li>

          </ul>

        </div>

        <!-- DETAILS -->
        <div
          v-for="section in detailsSections"
          :key="section.title"
          class="bg-base-200 border border-base-300 rounded-box"
        >

          <div class="p-4">

            <h3 class="text-sm font-semibold opacity-70 mb-2">
              {{ section.title }}
            </h3>

            <template v-if="section.type === 'table'">

              <div class="overflow-x-auto">
                <table class="table table-sm">

                  <tbody>

                    <tr
                      v-for="row in section.rows"
                      :key="row.label"
                    >
                      <td class="opacity-60 whitespace-nowrap">
                        <font-awesome-icon :icon="row.icon"/>
                        {{ row.label }}
                      </td>

                      <td class="wrap-break-word">
                        {{ row.value }}
                      </td>

                    </tr>

                  </tbody>

                </table>
              </div>

            </template>

            <template v-else-if="section.type === 'text'">

              <p class="text-sm wrap-break-word">
                {{ section.value || 'No description' }}
              </p>

            </template>

          </div>

        </div>

        <!-- CLOSE -->
        <label
          :for="'task-info-drawer-' + task.id"
          class="btn btn-neutral mt-auto w-full"
        >
          Close
        </label>

      </div>

    </div>

    <!-- CREATE TASK DIALOG -->
    <BaseDialog v-model="createDialog" title="Create task" confirmText="Create" cancelText="Cancel"
      @confirm="createTask" @cancel="closeCreate">
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
        <label class="label" for="title">Title</label>
        <input v-model="form.title" class="input input-bordered w-full" placeholder="Task title" />
        <label class="label" for="description">Description</label>
        <textarea v-model="form.description" class="textarea textarea-bordered w-full min-h-52"
          placeholder="Description"></textarea>
        <div class="flex gap-2 w-full">
          <div class="flex-1">
            <label class="label" for="priority">Priority</label>
            <select v-model="form.priority" class="select select-bordered flex-1">
              <option :value="1">Priority 1</option>
              <option :value="2">Priority 2</option>
              <option :value="3">Priority 3</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="label" for="storyPoints">Story Points</label>
            <select v-model="form.storyPoints" class="select select-bordered flex-1">
              <option :value="1">1 SP</option>
              <option :value="3">3 SP</option>
              <option :value="5">5 SP</option>
            </select>
          </div>
        </div>
        <label class="label" for="dueDate">Due Date</label>
        <input type="date" v-model="form.dueDate" class="input input-bordered w-full" />
      </div>
    </BaseDialog>

    <!-- Delete -->
    <BaseDialog v-model="deleteDialog" title="Delete Task" confirmText="Delete" cancelText="Cancel"
      @confirm="confirmDelete">
      <p>Are you sure you want to delete this task? This action cannot be undone.</p>
    </BaseDialog>

    <!-- Edit -->
    <BaseDialog v-model="editDialog" title="Edit Task" confirmText="Save" cancelText="Cancel" @confirm="updateTask"
      @cancel="closeEdit">
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
        <label class="label" for="title">Title</label>
        <input v-model="form.title" class="input input-bordered w-full" placeholder="Task title" />
        <label class="label" for="description">Description</label>
        <textarea v-model="form.description" class="textarea textarea-bordered w-full min-h-52"
          placeholder="Description"></textarea>
        <div class="flex gap-2">
          <div class="flex-1">
            <label class="label" for="priority">Priority</label>
            <select v-model="form.priority" class="select select-bordered flex-1">
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
          <div class="flex-1">
            <label class="label" for="storyPoints">Story Points</label>
            <select v-model="form.storyPoints" class="select select-bordered flex-1">
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
        <label class="label" for="status">Status</label>
        <select v-model="form.status" class="select select-bordered w-full">
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <label class="label" for="dueDate">Due Date</label>
        <input type="date" v-model="form.dueDate" class="input input-bordered w-full" />
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useWorkspaceProjectsTasksStore } from '@/stores/workspace/projectsTasks'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'ProjectTask',
  components: { BaseDialog },
  props: { task: { type: Object, required: true } },
  data() {
    return {
      createDialog: false,
      deleteDialog: false,
      editDialog: false,
      tasksStore: useWorkspaceProjectsTasksStore(),
      projectsStore: useWorkspaceProjectsStore(),
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
    detailsSections() {
      return [
        {
          title: 'Task details',
          type: 'table',
          rows: [
            { label: 'Story points', value: this.task.storyPoints, icon: 'fa-solid fa-bolt' },
            { label: 'Priority', value: this.task.priority, icon: 'fa-solid fa-flag' },
            { label: 'Status', value: this.task.status, icon: 'fa-solid fa-check' },
          ],
        },
        {
          title: 'Dates',
          type: 'table',
          rows: [
            { label: 'Created', value: this.task.createdAt, icon: 'fa-solid fa-calendar' },
            { label: 'Due', value: this.task.dueDate, icon: 'fa-solid fa-clock' },
          ],
        },
        {
          title: 'Description',
          type: 'text',
          value: this.task.description,
        },
      ]
    },
  },
  methods: {
    closeCreate() {
      this.createDialog = false
      this.tasksStore.clearError()
    },
    closeEdit() {
      this.editDialog = false
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
      try {
        const payload = {
          title: this.form.title,
          description: this.form.description,
          priority: this.form.priority,
          storyPoints: this.form.storyPoints,
          status: this.form.status,
          dueDate: this.form.dueDate,
          projectId: this.projectsStore.selectedProject.id,
          stageId: this.task.stageId,
        }
        await this.tasksStore.createTask(payload)
        this.createDialog = false

        const drawer = document.getElementById('task-info-drawer-' + this.task.id)
        if (drawer) drawer.checked = false
      } catch (e) {
        console.error(e)
      }
    },
    openDeleteDialog() {
      this.deleteDialog = true
    },

    // Confirm deletion
    async confirmDelete() {
      try {
        await this.tasksStore.deleteTask({
          projectId: this.projectsStore.selectedProject.id,
          taskId: this.task.id,
          stageId: this.task.stageId,
        })
        this.deleteDialog = false
        // Optional: close drawer after deletion
        const drawer = document.getElementById('task-info-drawer-' + this.task.id)
        if (drawer) drawer.checked = false
      } catch (e) {
        console.error(e)
      }
    },
    openEditDialog() {
      // Ieliekam esošos datus formā
      this.form = {
        title: this.task.title,
        description: this.task.description,
        priority: this.task.priority,
        storyPoints: this.task.storyPoints,
        status: this.task.status,
        dueDate: this.task.dueDate,
      }
      this.editDialog = true
    },

    async updateTask() {
      try {
        const payload = {
          taskId: this.task.id,
          title: this.form.title,
          description: this.form.description,
          priority: this.form.priority,
          storyPoints: this.form.storyPoints,
          status: this.form.status,
          dueDate: this.form.dueDate,
          projectId: this.projectsStore.selectedProject.id,
          stageId: this.task.stageId,
        }
        await this.tasksStore.updateTask(payload)
        this.editDialog = false
        const drawer = document.getElementById('task-info-drawer-' + this.task.id)
        if (drawer) drawer.checked = false
      } catch (e) {
        console.error(e)
      }
    },
  },
}
</script>
