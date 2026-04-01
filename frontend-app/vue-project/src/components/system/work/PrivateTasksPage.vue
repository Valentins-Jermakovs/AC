<template>
  <div class="h-full bg-base-100 p-1 flex flex-col lg:flex-row">
    <!-- Left screen: task list with search bar and pagination -->
    <div class="w-full lg:w-1/2 bg-base-200 border border-base-300 flex flex-col gap-1 p-1">
      <SearchBar @search="handleSearch" />
      <TaskList :tasks="privateTasksStore.privateTasks" @select-task="selectTask" :selectedTask="selectedTask" />

      <!-- Pagination -->
      <div
        class="w-full p-4 border border-base-300 bg-base-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div class="flex flex-col sm:flex-row sm:items-center sm:gap-6 w-full sm:w-auto">
          <div class="flex flex-col sm:flex-row sm:items-center gap-2">
            <label class="text-sm opacity-70">{{ $t('cabinet.admin.table_footer.limit') }}</label>
            <select class="select select-bordered mt-1 w-full sm:w-auto sm:mt-0" v-model="limit">
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
          </div>
          <div class="text-sm opacity-80 whitespace-nowrap">
            {{ $t('cabinet.admin.table_footer.total') }}
            <span class="font-semibold">{{ total }}</span>
          </div>
          <div class="text-sm opacity-80 whitespace-nowrap">
            {{ $t('cabinet.admin.table_footer.page') }}
            <span class="font-semibold">{{ page }}</span> /
            <span class="font-semibold">{{ totalPages }}</span>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row sm:gap-3 gap-2 w-full sm:w-auto">
          <button class="btn btn-neutral hover:btn-primary flex-1 p-2" @click="prevPage" :disabled="page <= 1">
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
          </button>
          <button class="btn btn-neutral hover:btn-primary flex-1 p-2" @click="nextPage"
            :disabled="page >= totalPages || totalPages === 0">
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
          </button>
        </div>
      </div>
    </div>

    <!-- Right screen: task details / empty states -->
    <div class="w-full lg:w-1/2 bg-base-200 border border-base-300 flex flex-col gap-1 p-1 h-1/2 md:h-full">
      <!-- Atlasīts uzdevums -->
      <TaskDetails v-if="selectedTask" :task="selectedTask" @delete-task="handleDelete" />

      <!-- Saraksts nav tukšs, bet nav atlasīts uzdevums -->
      <div v-else-if="privateTasksStore.privateTasks.length > 0"
        class="flex flex-col items-center justify-center h-full text-base-content/50 gap-3 text-center">
        <!-- Rotējoša brīdinājuma ikona -->
        <font-awesome-icon icon="fa-solid fa-triangle-exclamation" size="4x" class="text-warning animate-spin-slow"
          bounce />

        <!-- Teksts ar papildikonu -->
        <h2 class="text-xl font-semibold text-base-content/80 flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-list" />
          {{ $t('errors.tasks_not_found') }}
        </h2>

        <progress class="progress progress-warning w-32"></progress>
        <button class="btn btn-primary" @click="showCreate = true">
          {{ $t('common.create') }}
        </button>
      </div>

      <!-- Saraksts tukšs -->
      <div v-else class="flex flex-col items-center justify-center h-full gap-4 bg-base-100 rounded p-4">
        <div class="flex flex-col items-center gap-2 font-semibold text-2xl text-base-content/60">
          <font-awesome-icon icon="fa-solid fa-file-pen" size="2xl text-base-content/40 animate-bounce" />
          <p class="text-lg text-base-content/40">
            {{ $t('work.errors.not_found_description') }}
          </p>
        </div>

        <button class="btn btn-primary btn-md" @click="showCreate = true">
          {{ $t('common.create') }}
        </button>


      </div>
    </div>

    <LoadingScreen v-if="privateTasksStore.loading" />
  </div>
  <!-- CREATE dialog -->
  <BaseDialog v-model="showCreate" :title="$t('work.modals.create_task.title')" :confirm-text="$t('common.create')"
    :cancel-text="$t('common.cancel')" @confirm="createTask" @cancel="closeCreate">
    <div class="flex flex-col gap-2 w-full">
      <!-- Error message transition -->
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <!-- Title -->
      <div>
        <label class="label">
          <span class="label-text">{{ $t('work.task_form.title') }}:</span>
        </label>
        <input class="input input-bordered w-full" :placeholder="$t('work.task_form.title_placeholder')"
          v-model="createForm.title" />
      </div>
      <!-- Description -->
      <div>
        <label class="label">
          <span class="label-text">{{ $t('work.task_form.description') }}:</span>
        </label>
        <textarea class="textarea textarea-bordered w-full h-40 resize-none"
          :placeholder="$t('work.task_form.description_placeholder')" v-model="createForm.description"></textarea>
      </div>
      <!-- Due date -->
      <div>
        <label class="label">
          <span class="label-text">{{ $t('work.task_form.due_date') }}:</span>
        </label>
        <input class="input input-bordered w-full" type="date" v-model="createForm.dueDate" />
      </div>
    </div>
  </BaseDialog>
</template>

<script>
// Import loading component
import LoadingScreen from '@/components/common/LoadingScreen.vue'

import SearchBar from './tasks/SearchBar.vue'
import TaskList from './tasks/TaskList.vue'
import TaskDetails from './tasks/TaskDetails.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'
import { usePrivateTasksStore } from '@/stores/privateTasks'

export default {
  name: 'PrivateTasksPage',
  components: { SearchBar, TaskList, TaskDetails, BaseDialog, LoadingScreen },
  data() {
    const privateTasksStore = usePrivateTasksStore()
    return {
      privateTasksStore,
      selectedTask: null,
      showCreate: false,
      createForm: { title: '', description: '', dueDate: '' },
    }
  },
  mounted() {
    this.privateTasksStore.fetchPrivateTasks()
  },
  computed: {
    page() {
      return this.privateTasksStore.meta.page
    },
    limit: {
      get() {
        return this.privateTasksStore.meta.limit
      },
      set(value) {
        this.privateTasksStore.setLimit(value)
      },
    },
    total() {
      return this.privateTasksStore.meta.totalItems
    },
    totalPages() {
      return this.privateTasksStore.meta.totalPages
    },

    error() {
      return this.privateTasksStore.error
    },
  },
  methods: {
    nextPage() {
      this.privateTasksStore.nextPage()
    },
    prevPage() {
      this.privateTasksStore.prevPage()
    },
    closeCreate() {
      this.showCreate = false
      this.privateTasksStore.clearError()
    },
    async handleSearch({ query, filter }) {
      this.privateTasksStore.searchQuery = query
      this.privateTasksStore.meta.page = 1
      switch (filter) {
        case 'all':
          await this.privateTasksStore.fetchPrivateTasks()
          break
        case 'title':
          await this.privateTasksStore.findPrivateTasksByTitle()
          break
        case 'description':
          await this.privateTasksStore.findPrivateTasksByDescription()
          break
        case 'duedate':
          await this.privateTasksStore.findPrivateTasksByDueDate()
          break
        case 'monthyear':
          await this.privateTasksStore.findPrivateTasksByMonth()
          break
        default:
          await this.privateTasksStore.fetchPrivateTasks()
      }
    },
    selectTask(task) {
      this.selectedTask = task
    },
    async createTask() {
      if (!this.createForm.dueDate) {
        this.privateTasksStore.error = 'Due date is required'
        return
      }

      const newTask = await this.privateTasksStore.createPrivateTask(this.createForm)

      this.showCreate = false
      this.createForm = { title: '', description: '', dueDate: '' }

      if (!this.selectedTask) {
        this.selectedTask = newTask
      }
    },
    async handleDelete(taskId) {
      await this.privateTasksStore.removePrivateTask(taskId)
      // ja dzēstais task bija atlasīts, atiestatām
      if (this.selectedTask?.id === taskId) {
        this.selectedTask = null
      }
    },
  },
}
</script>

<style scoped></style>
