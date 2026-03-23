<template>
  <div class="drawer drawer-end">
    <input :id="'task-info-drawer-' + task.id" type="checkbox" class="drawer-toggle" />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div class="w-full bg-base-100 border border-base-300 p-3 flex">
        <!-- LEFT -->
        <div class="flex flex-col gap-2 flex-1">
          <div class="flex items-center gap-3">
            <h3 class="font-medium">{{ task.title }}</h3>
          </div>

          <!-- META -->
          <div class="flex flex-wrap gap-2 text-xs">
            <div class="badge badge-primary badge-outline">
              <font-awesome-icon icon="fa-solid fa-tag" />
              Status: {{ task.status }}
            </div>
            <div class="badge badge-neutral gap-2">
              <font-awesome-icon icon="fa-solid fa-bolt" /> SP: {{ task.storyPoints }}
            </div>
            <div class="badge badge-secondary gap-2">
              <font-awesome-icon icon="fa-solid fa-sort" />
              Priority: {{ task.priority }}
            </div>
            <div class="badge badge-neutral gap-2">
              <font-awesome-icon icon="fa-solid fa-calendar" />
              {{ task.createdAt }}
            </div>
            <div class="badge badge-warning gap-2">
              <font-awesome-icon icon="fa-solid fa-clock" />
              {{ task.dueDate }}
            </div>
          </div>

          <!-- DESCRIPTION -->
          <div class="p-5 bg-base-200 border border-base-300">
            <p class="text-sm line-clamp-3">{{ task.description }}</p>
          </div>
        </div>

        <!-- OPEN DRAWER -->
        <label :for="'task-info-drawer-' + task.id" class="btn btn-neutral btn-circle">
          <font-awesome-icon icon="fa-solid fa-link" />
        </label>
      </div>
    </div>

    <!-- DRAWER -->
    <div class="drawer-side">
      <label :for="'task-info-drawer-' + task.id" class="drawer-overlay"></label>

      <div class="bg-base-100 border border-base-300 min-h-full w-96 p-6 flex flex-col gap-6">
        <!-- HEADER -->
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">{{ task.title }}</h2>
          <label :for="'task-info-drawer-' + task.id" class="btn btn-ghost btn-sm btn-circle">✕</label>
        </div>

        <!-- ACTIONS -->
        <div class="bg-base-200 border border-base-300 w-full">
          <ul class="menu w-full">
            <li>
              <button class="flex gap-3" @click="openCreateDialog">
                <font-awesome-icon icon="fa-solid fa-plus" /> Create task
              </button>
            </li>
            <li>
              <button class="flex gap-3" @click="openEditDialog">
                <font-awesome-icon icon="fa-solid fa-pen" /> Edit Task
              </button>
            </li>
            <li class="border-t border-base-300 mt-2 pt-2">
              <button class="text-error flex gap-3" @click="openDeleteDialog">
                <font-awesome-icon icon="fa-solid fa-trash" /> Delete Task
              </button>
            </li>
          </ul>
        </div>

        <!-- DETAILS, DATES, DESCRIPTION -->
        <div class="bg-base-200 border border-base-300" v-for="section in detailsSections" :key="section.title">
          <div class=" p-4">
            <h3 class="text-sm font-semibold opacity-70">{{ section.title }}</h3>
            <template v-if="section.type === 'table'">
              <table class="table table-sm">
                <tbody>
                  <tr v-for="row in section.rows" :key="row.label">
                    <td class="opacity-60">
                      <font-awesome-icon :icon="row.icon" />
                      {{ row.label }}
                    </td>
                    <td>{{ row.value }}</td>
                  </tr>
                </tbody>
              </table>
            </template>
            <template v-else-if="section.type === 'text'">
              <p class="text-sm">{{ section.value || 'No description' }}</p>
            </template>
          </div>
        </div>

        <!-- CLOSE -->
        <label :for="'task-info-drawer-' + task.id" class="btn btn-neutral mt-auto"> Close </label>
      </div>
    </div>

    <!-- CREATE TASK DIALOG -->
    <BaseDialog v-model="createDialog" title="Create task" confirmText="Create" cancelText="Cancel"
      @confirm="createTask">
      <div class="flex flex-col gap-2 w-full">
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
    <BaseDialog v-model="editDialog" title="Edit Task" confirmText="Save" cancelText="Cancel" @confirm="updateTask">
      <div class="flex flex-col gap-2 w-full">
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
      if (!this.form.title) return
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
      if (!this.form.title) return
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
