<template>
  <div class="border border-base-300 rounded-box p-4 bg-base-100 flex flex-col gap-5 
  h-full overflow-y-auto">
    <!-- Title & Metadata -->
    <div class="flex flex-col gap-5">
      <h1 class="font-semibold text-2xl wrap-break-word whitespace-pre-line">{{ task.title }}</h1>
      <div class="flex flex-wrap gap-4 text-sm text-base-content/70">
        <div class="flex gap-1 items-center">
          <span class="font-medium">{{ $t('work.task_detail.status') }}:</span>
          <span :class="statusClass(task.completed)">
            {{ task.completed ? $t('work.task_detail.complete') : $t('work.task_detail.pending') }}
          </span>
        </div>
        <div class="flex gap-1 items-center">
          <span class="font-medium">{{ $t('work.task_detail.created_at') }}:</span>
          <span class="text-info">{{ task.createdAt }}</span>
        </div>
        <div class="flex gap-1 items-center">
          <span class="font-medium">{{ $t('work.task_detail.due_date') }}:</span>
          <span class="text-warning">{{ task.dueDate }}</span>
        </div>
      </div>
    </div>

    <!-- Description -->
    <div>
      <p class="text-base text-base-content/70 wrap-break-word whitespace-pre-line">
        {{ task.description }}
      </p>
      <div class="divider"></div>
    </div>

    <div class="flex-1"></div>

    <!-- Action Buttons -->
    <div class="flex flex-wrap justify-end gap-2 mt-2">
      <button class="btn btn-md btn-error" @click="showDelete = true">
        <font-awesome-icon icon="fa-solid fa-trash" />
        {{ $t('common.delete') }}
      </button>

      <button class="btn btn-md btn-success" @click="openComplete" :disabled="task.completed">
        <font-awesome-icon icon="fa-solid fa-check" />
        {{ $t('common.complete') }}
      </button>

      <button class="btn btn-md btn-secondary" @click="openEdit">
        <font-awesome-icon icon="fa-solid fa-pen-to-square" />
        {{ $t('common.edit') }}
      </button>

      <button class="btn btn-md btn-primary" @click="showCreate = true">
        <font-awesome-icon icon="fa-solid fa-plus" />
        {{ $t('common.create') }}
      </button>
    </div>

    <!-- DELETE -->
    <BaseDialog v-model="showDelete" :title="$t('work.modals.delete_task.title')" :confirm-text="$t('common.delete')"
      :cancel-text="$t('common.cancel')" @confirm="$emit('delete-task', task.id)" @cancel="closeDelete">
      {{ $t('work.modals.delete_task.content') }}
    </BaseDialog>

    <!-- COMPLETE -->
    <BaseDialog v-model="showComplete" :title="$t('work.modals.complete_task.title')"
      :confirm-text="$t('common.complete')" :cancel-text="$t('common.cancel')" @confirm="completeTask"
      @cancel="closeComplete">
      {{ $t('work.modals.complete_task.content') }}
    </BaseDialog>

    <!-- EDIT -->
    <BaseDialog v-model="showEdit" :title="$t('work.modals.edit_task.title')" :confirm-text="$t('common.edit')"
      :cancel-text="$t('common.cancel')" @cancel="closeEdit" @confirm="editTask">
      <div class="w-full flex flex-col gap-2">
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
          <input class="input input-bordered w-full" v-model="editForm.title"
            :placeholder="$t('work.task_form.title_placeholder')" />
        </div>
        <!-- Description -->
        <div>
          <label class="label">
            <span class="label-text">{{ $t('work.task_form.description') }}:</span>
          </label>
          <textarea class="textarea textarea-bordered w-full min-h-52" v-model="editForm.description"
            :placeholder="$t('work.task_form.description_placeholder')">
          </textarea>
        </div>
        <!-- Due date -->
        <div>
          <label class="label">
            <span class="label-text">{{ $t('work.task_form.due_date') }}:</span>
          </label>
          <input class="input input-bordered w-full" type="date" v-model="editForm.dueDate" />
        </div>
        <!-- Status -->
        <div>
          <label class="label">
            <span class="label-text">{{ $t('work.task_form.status') }}:</span>
          </label>
          <select class="select select-bordered w-full" v-model="editForm.completed">
            <option :value="true">{{ $t('work.task_form.status_complete') }}</option>
            <option :value="false">{{ $t('work.task_form.status_pending') }}</option>
          </select>
        </div>
      </div>
    </BaseDialog>

    <!-- CREATE -->
    <BaseDialog v-model="showCreate" :title="$t('work.modals.create_task.title')" :confirm-text="$t('common.create')"
      :cancel-text="$t('common.cancel')" @cancel="closeCreate" @confirm="createTask">
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
          <textarea class="textarea textarea-bordered w-full min-h-52"
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
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { usePrivateTasksStore } from '@/stores/privateTasks'

export default {
  components: { BaseDialog },
  name: 'TaskCard',
  data() {
    const privateTasksStore = usePrivateTasksStore()

    return {
      privateTasksStore,

      showDelete: false,
      showComplete: false,
      showEdit: false,
      showCreate: false,

      editForm: {
        title: '',
        description: '',
      },

      createForm: {
        title: '',
        description: '',
        dueDate: '',
      },
    }
  },
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
  computed: {
    error() {
      return this.privateTasksStore.error
    },
  },
  methods: {
    statusClass(completed) {
      return completed
        ? 'px-2 py-0.5 rounded-full bg-green-100 text-green-800 text-xs'
        : 'px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs'
    },

    closeEdit() {
      this.showEdit = false
      this.privateTasksStore.clearError()
    },

    closeCreate() {
      this.showCreate = false
      this.privateTasksStore.clearError()

      this.createForm = {
        title: '',
        description: '',
        dueDate: '',
      }
    },

    closeDelete() {
      this.showDelete = false
      this.privateTasksStore.clearError()
    },

    closeComplete() {
      this.showComplete = false
      this.privateTasksStore.clearError()
    },

    async deleteTask() {
      await this.privateTasksStore.removePrivateTask(this.task.id)

      this.showDelete = false
    },

    async completeTask() {
      try {
        await this.privateTasksStore.updatePrivateTask({
          taskId: this.task.id,
          completed: true,
        })

        this.showComplete = false
        this.task.completed = true
      } catch (err) {
        console.error('Failed to complete task:', err)
      }
    },

    async openComplete() {
      this.editForm = {
        title: this.task.title,
        description: this.task.description,
        dueDate: this.task.dueDate,
        completed: this.task.completed,
      }

      this.showComplete = true
    },

    async editTask() {
      try {
        await this.privateTasksStore.updatePrivateTask({
          taskId: this.task.id,
          title: this.editForm.title,
          description: this.editForm.description,
          dueDate: this.editForm.dueDate,
          completed: this.editForm.completed,
        })
        // atjaunojam vietējo task objektu, lai UI uzreiz atspoguļojas
        this.task.title = this.editForm.title
        this.task.description = this.editForm.description
        this.task.dueDate = this.editForm.dueDate
        this.task.completed = this.editForm.completed

        this.showEdit = false
      } catch (err) {
        console.error('Failed to update task:', err)
      }
    },

    async createTask() {
      if (!this.createForm.dueDate) {
        this.privateTasksStore.error = 'Due date is required'
        return
      }

      await this.privateTasksStore.createPrivateTask(this.createForm)

      this.showCreate = false

      // clean form data
      this.createForm = { title: '', description: '', dueDate: '' }
    },

    openEdit() {
      this.editForm = {
        title: this.task.title,
        description: this.task.description,
        dueDate: this.task.dueDate,
        completed: this.task.completed,
      }
      this.showEdit = true
    },
  },
}
</script>

<style scoped>
.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 100px;
}
</style>
