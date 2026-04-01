<template>
  <div class="drawer drawer-end">
    <input :id="'task-info-drawer-' + task.id" type="checkbox" class="drawer-toggle" />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div
        class="w-full bg-base-100 border border-base-300 rounded-box p-3 sm:p-4 flex flex-col sm:flex-row gap-3"
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
              <p v-if="task.status == 'todo'">{{ $t('work.projects.common.todo') }}</p>
              <p v-if="task.status == 'in_progress'">
                {{ $t('work.projects.common.in_progress') }}
              </p>
              <p v-if="task.status == 'done'">{{ $t('work.projects.common.done') }}</p>
            </div>

            <div class="badge badge-neutral gap-1">
              <font-awesome-icon icon="fa-solid fa-bolt" />
              {{ $t('work.projects.modals.create_user_story.story_points') }}:
              {{ task.storyPoints }}
            </div>

            <div class="badge badge-secondary gap-1">
              <font-awesome-icon icon="fa-solid fa-sort" />
              {{ $t('work.projects.modals.create_user_story.priority') }}: {{ task.priority }}
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
          <div class="p-3 sm:p-4 bg-base-200 border border-base-300 rounded-box">
            <pre class="text-sm line-clamp-3 wrap-break-word">{{ task.description }}</pre>
          </div>
        </div>

        <!-- OPEN -->
        <div class="flex sm:flex-col justify-end">
          <label :for="'task-info-drawer-' + task.id" class="btn btn-neutral btn-circle">
            <font-awesome-icon icon="fa-solid fa-ellipsis-vertical" />
          </label>
        </div>
      </div>
    </div>

    <!-- DRAWER -->
    <div class="drawer-side z-50">
      <label :for="'task-info-drawer-' + task.id" class="drawer-overlay"></label>

      <div
        class="bg-base-100 border border-base-300 min-h-full w-full sm:w-96 p-4 sm:p-6 flex flex-col gap-6 overflow-y-auto"
      >
        <!-- HEADER -->
        <div class="flex justify-between items-start gap-3">
          <h2 class="text-lg sm:text-xl font-semibold wrap-break-word">
            {{ task.title }}
          </h2>

          <label :for="'task-info-drawer-' + task.id" class="btn btn-ghost btn-sm btn-circle">
            ✕
          </label>
        </div>

        <!-- ACTIONS -->
        <div
          class="bg-base-200 border border-base-300"
          v-if="membersStore.currentUser && membersStore.currentUser.role !== 'viewer'"
        >
          <ul class="menu w-full">
            <li>
              <button class="flex gap-3 items-center" @click="openCreateDialog">
                <font-awesome-icon icon="fa-solid fa-plus" />
                {{ $t('work.projects.common.create_new_user_story') }}
              </button>
            </li>

            <li>
              <button class="flex gap-3 items-center" @click="openEditDialog">
                <font-awesome-icon icon="fa-solid fa-pen" />
                {{ $t('work.projects.common.edit_user_story') }}
              </button>
            </li>

            <li class="border-t border-base-300 mt-2 pt-2">
              <button class="text-error flex gap-3 items-center" @click="openDeleteDialog">
                <font-awesome-icon icon="fa-solid fa-trash" />
                {{ $t('work.projects.common.delete_user_story') }}
              </button>
            </li>
          </ul>
        </div>

        <!-- DETAILS -->
        <div
          v-for="section in detailsSections"
          :key="section.title"
          class="bg-base-200 border border-base-300"
        >
          <div class="p-4">
            <h3 class="text-sm font-semibold opacity-70 mb-2">
              {{ section.title }}
            </h3>

            <template v-if="section.type === 'table'">
              <div class="overflow-x-auto">
                <table class="table table-sm">
                  <tbody>
                    <tr v-for="row in section.rows" :key="row.label">
                      <td class="opacity-60 whitespace-nowrap">
                        <font-awesome-icon :icon="row.icon" />
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
              <pre class="text-sm wrap-break-word">{{ section.value }}</pre>
            </template>
          </div>
        </div>

        <!-- CLOSE -->
        <label :for="'task-info-drawer-' + task.id" class="btn btn-neutral mt-auto w-full">
          {{ $t('common.close') }}
        </label>
      </div>
    </div>

    <!-- CREATE TASK DIALOG -->
    <BaseDialog
      v-model="createDialog"
      :title="$t('work.projects.modals.create_user_story.title')"
      :confirmText="$t('common.create')"
      :cancelText="$t('common.cancel')"
      @confirm="createTask"
      @cancel="closeCreate"
    >
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <label class="label" for="title">
          {{ $t('work.projects.modals.create_user_story.name') }}
        </label>
        <input
          v-model="form.title"
          class="input input-bordered w-full"
          :placeholder="$t('work.projects.modals.create_user_story.name_placeholder')"
        />
        <label class="label" for="description">
          {{ $t('work.projects.modals.create_user_story.description') }}
        </label>
        <textarea
          v-model="form.description"
          maxlength="1000"
          class="textarea textarea-bordered w-full"
          :placeholder="$t('work.projects.modals.create_user_story.description_placeholder')"
        ></textarea>
        <div class="flex gap-2 w-full">
          <div class="flex-1">
            <label class="label" for="priority">
              {{ $t('work.projects.modals.create_user_story.priority') }}
            </label>
            <select v-model="form.priority" class="select select-bordered flex-1">
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
          <div class="flex-1">
            <label class="label" for="storyPoints">
              {{ $t('work.projects.modals.create_user_story.story_points') }}
            </label>
            <select v-model="form.storyPoints" class="select select-bordered flex-1">
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
        <label class="label" for="status">
          {{ $t('work.projects.modals.create_user_story.status') }}
        </label>
        <select v-model="form.status" class="select select-bordered w-full">
          <option value="todo">{{ $t('work.projects.common.todo') }}</option>
          <option value="in_progress">{{ $t('work.projects.common.in_progress') }}</option>
          <option value="done">{{ $t('work.projects.common.done') }}</option>
        </select>
        <!-- Created at -->
        <div>
          <label class="label">
            {{ $t('work.projects.modals.create_user_story.start_date') }}
          </label>

          <input type="date" v-model="form.createdAt" class="input input-bordered w-full" />
        </div>
        <label class="label" for="dueDate">
          {{ $t('work.projects.modals.create_user_story.due_date') }}
        </label>
        <input type="date" v-model="form.dueDate" class="input input-bordered w-full" />
      </div>
    </BaseDialog>

    <!-- Delete -->
    <BaseDialog
      v-model="deleteDialog"
      :title="$t('work.projects.modals.delete_user_story.title')"
      :confirmText="$t('common.delete')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmDelete"
    >
      <p>
        {{ $t('work.projects.modals.delete_user_story.content') }}
      </p>
    </BaseDialog>

    <!-- Edit -->
    <BaseDialog
      v-model="editDialog"
      :title="$t('work.projects.modals.edit_user_story.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="updateTask"
      @cancel="closeEdit"
    >
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <label class="label" for="title">
          {{ $t('work.projects.modals.create_user_story.name') }}
        </label>
        <input
          v-model="form.title"
          class="input input-bordered w-full"
          :placeholder="$t('work.projects.modals.create_user_story.name_placeholder')"
        />
        <label class="label" for="description">
          {{ $t('work.projects.modals.create_user_story.description') }}
        </label>
        <textarea
          v-model="form.description"
          class="textarea textarea-bordered w-full"
          maxlength="1000"
          :placeholder="$t('work.projects.modals.create_user_story.description_placeholder')"
        ></textarea>
        <div class="flex gap-2">
          <div class="flex-1">
            <label class="label" for="priority">
              {{ $t('work.projects.modals.create_user_story.priority') }}
            </label>
            <select v-model="form.priority" class="select select-bordered flex-1">
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
          <div class="flex-1">
            <label class="label" for="storyPoints">
              {{ $t('work.projects.modals.create_user_story.story_points') }}
            </label>
            <select v-model="form.storyPoints" class="select select-bordered flex-1">
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
        <label class="label" for="status">
          {{ $t('work.projects.modals.create_user_story.status') }}
        </label>
        <select v-model="form.status" class="select select-bordered w-full">
          <option value="todo">
            {{ $t('work.projects.common.todo') }}
          </option>
          <option value="in_progress">
            {{ $t('work.projects.common.in_progress') }}
          </option>
          <option value="done">
            {{ $t('work.projects.common.done') }}
          </option>
        </select>
        <!-- Created at -->
        <div>
          <label class="label">
            {{ $t('work.projects.modals.create_user_story.start_date') }}
          </label>

          <input type="date" v-model="form.createdAt" class="input input-bordered w-full" />
        </div>
        <label class="label" for="dueDate">
          {{ $t('work.projects.modals.create_user_story.due_date') }}
        </label>
        <input type="date" v-model="form.dueDate" class="input input-bordered w-full" />
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useWorkspaceProjectsTasksStore } from '@/stores/workspace/projectsTasks'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'

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
      membersStore: useWorkspaceProjectMembersStore(),
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
    detailsSections() {
      return [
        {
          title: this.$t('work.projects.drawer.metadata'),
          type: 'table',
          rows: [
            {
              label: this.$t('work.projects.modals.create_user_story.story_points'),
              value: this.task.storyPoints,
              icon: 'fa-solid fa-bolt',
            },
            {
              label: this.$t('work.projects.modals.create_user_story.priority'),
              value: this.task.priority,
              icon: 'fa-solid fa-flag',
            },
            {
              label: this.$t('work.projects.modals.create_user_story.status'),
              value: this.$t(`work.projects.common.${this.task.status}`),
              icon: 'fa-solid fa-check',
            },
          ],
        },
        {
          title: this.$t('work.projects.common.dates'),
          type: 'table',
          rows: [
            {
              label: this.$t('work.projects.drawer.start_date'),
              value: this.task.createdAt,
              icon: 'fa-solid fa-calendar',
            },
            {
              label: this.$t('work.projects.drawer.end_date'),
              value: this.task.dueDate,
              icon: 'fa-solid fa-clock',
            },
          ],
        },
        {
          title: this.$t('work.projects.drawer.description'),
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
        createdAt: null,
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
          createdAt: this.form.createdAt,
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
        createdAt: this.task.createdAt,
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
          createdAt: this.form.createdAt,
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
