<template>
  <div class="border border-base-300 rounded-box p-4 bg-base-100 flex flex-col gap-5 h-full">

    <!-- Title & Metadata -->
    <div class="flex flex-col gap-5">
      <h1 class="font-semibold text-2xl">{{ task.title }}</h1>
      <div class="flex flex-wrap gap-4 text-sm text-base-content/70">
        <div class="flex gap-1 items-center">
          <span class="font-medium">Status:</span>
          <span :class="statusClass(task.completed)">
            {{ task.completed ? 'Completed' : 'Pending' }}
          </span>
        </div>
        <div class="flex gap-1 items-center">
          <span class="font-medium">Created:</span>
          <span class="text-info">{{ task.createdAt }}</span>
        </div>
        <div class="flex gap-1 items-center">
          <span class="font-medium">Due date:</span>
          <span class="text-warning">{{ task.dueDate }}</span>
        </div>
      </div>
    </div>

    <!-- Description -->
    <div>
      <p class="text-base text-base-content/70">{{ task.description }}</p>
      <div class="divider"></div>
    </div>

    <div class="flex-1"></div>

    <!-- Action Buttons -->
    <div class="flex flex-wrap justify-end gap-2 mt-2">
      <button class="btn btn-md btn-error" @click="showDelete = true">
        Delete
      </button>

      <button class="btn btn-md btn-success" @click="openComplete">
        Complete
      </button>

      <button class="btn btn-md btn-secondary" @click="openEdit">
        Edit
      </button>

      <button class="btn btn-md btn-primary" @click="showCreate = true">
        Create new
      </button>
    </div>

    <!-- DELETE -->
    <BaseDialog v-model="showDelete" title="Delete task" confirmText="Delete" cancelText="Cancel"
      @confirm="$emit('delete-task', task.id)"
      @cancel="closeDelete">
      Are you sure you want to delete this task?
    </BaseDialog>


    <!-- COMPLETE -->
    <BaseDialog v-model="showComplete" title="Complete task" confirmText="Complete" cancelText="Cancel"
      @confirm="completeTask"
      @cancel="closeComplete">
      Mark task as completed?
    </BaseDialog>


    <!-- EDIT -->
    <BaseDialog v-model="showEdit" title="Edit task" confirmText="Save" cancelText="Cancel" @cancel="closeEdit" @confirm="editTask">

      <div class="w-full flex flex-col gap-2">
        <!-- Error message transition -->
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <!-- Title -->
        <div> <label class="label"> <span class="label-text">Title:</span> </label> <input
            class="input input-bordered w-full" v-model="editForm.title" /> </div> <!-- Description -->
        <div> <label class="label"><span class="label-text">Description:</span></label> <textarea
            class="textarea textarea-bordered w-full h-40 resize-none" v-model="editForm.description"></textarea> </div>
        <!-- Due date -->
        <div> <label class="label"><span class="label-text">Due date:</span></label> <input
            class="input input-bordered w-full" type="date" v-model="editForm.dueDate" /> </div> <!-- Status -->
        <div> <label class="label"><span class="label-text">Status:</span></label> <select
            class="select select-bordered w-full" v-model="editForm.completed">
            <option :value="true">Completed</option>
            <option :value="false">Pending</option>
          </select> </div>
      </div>

    </BaseDialog>


    <!-- CREATE -->
    <BaseDialog v-model="showCreate" title="Create task" confirmText="Create" cancelText="Cancel" @cancel="closeCreate" @confirm="createTask">

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
            <span class="label-text">Title:</span>
          </label>
          <input class="input input-bordered w-full" placeholder="Title" v-model="createForm.title" />
        </div>
        <!-- Description -->
        <div>
          <label class="label">
            <span class="label-text">Description:</span>
          </label>
          <textarea class="textarea textarea-bordered w-full h-40 resize-none" placeholder="Description"
            v-model="createForm.description"></textarea>
        </div>
        <!-- Due date -->
        <div>
          <label class="label">
            <span class="label-text">Due date:</span>
          </label>
          <input class="input input-bordered w-full" type="date" v-model="createForm.dueDate" />
        </div>
      </div>

    </BaseDialog>

  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';
import { usePrivateTasksStore } from '@/stores/privateTasks';

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
        description: ''
      },

      createForm: {
        title: '',
        description: '',
        dueDate: ''
      }
    }
  },
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  computed: {
    error() {
      return this.privateTasksStore.error
    }
  },
  methods: {
    statusClass(completed) {
      return completed
        ? 'px-2 py-0.5 rounded-full bg-green-100 text-green-800 text-xs'
        : 'px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs';
    },

    closeEdit() {
      this.showEdit = false
      this.privateTasksStore.clearError()
    },

    closeCreate() {
      this.showCreate = false
      this.privateTasksStore.clearError()
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
          completed: true
        });

        this.showComplete = false
        this.task.completed = true
      }
      catch (err) {
        console.error('Failed to complete task:', err);
      }
    },

    async openComplete() {
      this.editForm = {
        title: this.task.title,
        description: this.task.description,
        dueDate: this.task.dueDate,
        completed: this.task.completed
      };

      this.showComplete = true
    },

    async editTask() {
      try {
        await this.privateTasksStore.updatePrivateTask({
          taskId: this.task.id,
          title: this.editForm.title,
          description: this.editForm.description,
          dueDate: this.editForm.dueDate,
          completed: this.editForm.completed
        });
        // atjaunojam vietējo task objektu, lai UI uzreiz atspoguļojas
        this.task.title = this.editForm.title;
        this.task.description = this.editForm.description;
        this.task.dueDate = this.editForm.dueDate;
        this.task.completed = this.editForm.completed;

        this.showEdit = false;
      } catch (err) {
        console.error('Failed to update task:', err);
      }
    },

    async createTask() {

      await this.privateTasksStore.createPrivateTask(
        this.createForm
      )

      this.showCreate = false

    },

    openEdit() {
      this.editForm = {
        title: this.task.title,
        description: this.task.description,
        dueDate: this.task.dueDate,
        completed: this.task.completed
      };
      this.showEdit = true;
    },

  },
};
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