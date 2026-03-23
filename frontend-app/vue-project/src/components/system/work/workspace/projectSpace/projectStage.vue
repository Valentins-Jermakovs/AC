<template>
    <div class="drawer drawer-end">
    <!-- drawer toggle -->
    <input type="checkbox" class="drawer-toggle" v-model="drawerOpen" />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div
        class="w-full bg-base-100 border border-base-300 
        rounded-box p-3 sm:p-4 
        flex flex-col gap-4 mt-3 sm:mt-5"
      >
        <!-- HEADER -->
        <div
          class="flex flex-col sm:flex-row 
          sm:items-center sm:justify-between 
          gap-3"
        >
          <div class="flex flex-col sm:flex-row sm:items-center gap-2">
            <h3 class="font-semibold text-lg wrap-break-word">
              {{ stage.title }}
            </h3>

            <div class="flex flex-wrap gap-2">
              <div class="badge badge-neutral gap-2">
                <font-awesome-icon icon="fa-solid fa-calendar" />
                {{ stage.createdAt }}
              </div>

              <div class="badge badge-warning gap-2">
                <font-awesome-icon icon="fa-solid fa-clock" />
                {{ stage.dueDate }}
              </div>
            </div>
          </div>

          <button
            class="btn btn-primary btn-circle self-end sm:self-auto"
            @click="drawerOpen = true"
          >
            <font-awesome-icon icon="fa-solid fa-code-branch" />
          </button>
        </div>

        <!-- TASKS -->
        <ProjectTaskList :stage="stage" />
      </div>
    </div>

    <!-- DRAWER -->
    <div class="drawer-side z-50">
      <label
        class="drawer-overlay"
        @click="drawerOpen = false"
      ></label>

      <div
        class="bg-base-200 
        min-h-full 
        w-full sm:w-96
        p-4 sm:p-6
        flex flex-col gap-6
        overflow-y-auto"
      >
        <!-- TITLE -->
        <div class="flex items-center justify-between gap-2">
          <h2 class="text-xl sm:text-2xl font-semibold wrap-break-word">
            {{ stage.title }}
          </h2>

          <button
            class="btn btn-ghost btn-sm btn-circle"
            @click="drawerOpen = false"
          >
            ✕
          </button>
        </div>

        <!-- ACTIONS -->
        <div class="bg-base-100 border border-base-300 rounded-box w-full">
          <ul class="menu w-full">

            <li>
              <button
                class="flex gap-3 items-center"
                @click="showCreateDialog = true"
              >
                <font-awesome-icon icon="fa-solid fa-plus" />
                Add stage
              </button>
            </li>

            <li>
              <button
                class="flex gap-3 items-center"
                @click="openRelativeDialog"
              >
                <font-awesome-icon icon="fa-solid fa-code-branch" />
                Add relative stage
              </button>
            </li>

            <li>
              <button
                class="flex gap-3 items-center"
                @click="openEditDialog"
              >
                <font-awesome-icon icon="fa-solid fa-pen" />
                Edit stage
              </button>
            </li>

            <li>
              <button
                class="flex gap-3 items-center"
                @click="moveStage('up')"
              >
                <font-awesome-icon icon="fa-solid fa-arrow-up" />
                Move up
              </button>
            </li>

            <li>
              <button
                class="flex gap-3 items-center"
                @click="moveStage('down')"
              >
                <font-awesome-icon icon="fa-solid fa-arrow-down" />
                Move down
              </button>
            </li>

            <li class="border-t border-base-300 mt-2 pt-2">
              <button
                class="text-error flex gap-3 items-center"
                @click="showDelete = true"
              >
                <font-awesome-icon icon="fa-solid fa-trash" />
                Delete stage
              </button>
            </li>

          </ul>
        </div>

        <!-- DESCRIPTION -->
        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-4">
            <h3 class="font-semibold text-sm opacity-70">
              Description
            </h3>

            <p class="text-sm wrap-break-word">
              {{ stage.description }}
            </p>
          </div>
        </div>

        <!-- META -->
        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-4">

            <h3 class="font-semibold text-sm opacity-70 mb-2">
              Metadata
            </h3>

            <div class="overflow-x-auto">
              <table class="table table-sm">

                <tbody>

                  <tr>
                    <td class="opacity-60">
                      <font-awesome-icon icon="fa-solid fa-calendar" />
                      Created
                    </td>

                    <td class="font-medium">
                      {{ stage.createdAt }}
                    </td>
                  </tr>

                  <tr>
                    <td class="opacity-60">
                      <font-awesome-icon icon="fa-solid fa-clock" />
                      Due date
                    </td>

                    <td class="font-medium">
                      {{ stage.dueDate }}
                    </td>
                  </tr>

                </tbody>

              </table>
            </div>

          </div>
        </div>

        <!-- CLOSE -->
        <button
          class="btn btn-neutral mt-auto w-full"
          @click="drawerOpen = false"
        >
          Close
        </button>

      </div>
    </div>
  </div>

  <!-- Create stage dialog -->
  <BaseDialog v-model="showCreateDialog" title="Create new stage" confirmText="Create" cancelText="Cancel"
    @confirm="handleCreate" @cancel="closeCreateDialog">
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">Stage Title</label>
      <input v-model="newStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <label for="stageDescription" class="label">Stage Description</label>
      <textarea v-model="newStage.description" class="textarea w-full min-h-52" placeholder="Stage description"></textarea>
      <label for="stageDueDate" class="label">Stage Due Date</label>
      <input v-model="newStage.dueDate" type="date" class="input w-full" />
    </div>
  </BaseDialog>
  <!-- Delete confirmation dialog -->
  <BaseDialog v-model="showDelete" title="Delete stage" confirmText="Delete" cancelText="Cancel"
    @confirm="handleDelete">
    <p>Are you sure you want to delete this stage?</p>
  </BaseDialog>
  <!-- Edit stage dialog -->
  <BaseDialog v-model="showEditDialog" title="Edit stage" confirmText="Update" cancelText="Cancel"
    @confirm="handleUpdate" @cancel="closeEditDialog">
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">Stage Title</label>
      <input v-model="editStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <label for="stageDescription" class="label">Stage Description</label>
      <textarea v-model="editStage.description" class="textarea w-full min-h-52" placeholder="Stage description"></textarea>
      <label for="stageDueDate" class="label">Stage Due Date</label>
      <input v-model="editStage.dueDate" type="date" class="input w-full" />
    </div>
  </BaseDialog>

  <!-- Relative stage dialog -->
  <BaseDialog v-model="showRelativeDialog" title="Add relative stage" confirmText="Create" cancelText="Cancel"
    @confirm="handleCreateRelative" @cancel="closeRelativeDialog">
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">Stage Title</label>
      <input v-model="relativeStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <label for="stageDescription" class="label">Stage Description</label>
      <textarea v-model="relativeStage.description" class="textarea w-full min-h-52" placeholder="Stage description"></textarea>
      <label for="stageDueDate" class="label">Stage Due Date</label>
      <input v-model="relativeStage.dueDate" type="date" class="input w-full" />
      <div class="flex gap-2 items-center mt-2">
        <label class="flex items-center gap-1">
          <input type="radio" value="before" class="radio" v-model="relativeStage.position" />
          Before
        </label>
        <label class="flex items-center gap-1">
          <input type="radio" value="after" class="radio" v-model="relativeStage.position" />
          After
        </label>
      </div>
    </div>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import ProjectTaskList from './projectTaskList.vue'
import { useWorkspaceProjectStagesStore } from '@/stores/workspace/projectStages'

export default {
  name: 'KanbanStageInfoDrawer',
  components: { ProjectTaskList, BaseDialog },
  props: {
    stage: { type: Object, required: true },
  },
  data() {
    return {
      drawerOpen: false,
      showCreateDialog: false,
      showDelete: false,
      showEditDialog: false,
      showRelativeDialog: false,
      stagesStore: useWorkspaceProjectStagesStore(),
      newStage: {
        title: '',
        description: '',
        dueDate: '',
      },
      editStage: {
        // ← form data for editing
        title: '',
        description: '',
        dueDate: '',
      },
      relativeStage: {
        // ← form dati relative stage
        title: '',
        description: '',
        dueDate: '',
        position: 'after', // default: after
      },
    }
  },
  methods: {
    closeCreateDialog() {
      this.showCreateDialog = false
      this.newStage = {
        title: '',
        description: '',
        dueDate: '',
      }
      this.stagesStore.clearError()
    },
    closeRelativeDialog() {
      this.showRelativeDialog = false
      this.relativeStage = {
        title: '',
        description: '',
        dueDate: '',
        position: 'after', // default: after
      }
      this.stagesStore.clearError()
    },
    closeEditDialog() {
      this.showEditDialog = false
      this.editStage = {
        title: '',
        description: '',
        dueDate: '',
      }
      this.stagesStore.clearError()
    },
    async handleCreate() {
      const payload = {
        title: this.newStage.title,
        description: this.newStage.description,
        dueDate: this.newStage.dueDate,
        projectId: this.stagesStore.projectId,
      }

      try {
        await this.stagesStore.createStage(payload)

        // Reset form and close dialog
        this.newStage = { title: '', description: '', dueDate: '' }
        this.showCreateDialog = false
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
      }
    },
    async handleDelete() {
      const payload = {
        projectId: this.stagesStore.projectId,
        stageId: this.stage.id,
      }
      try {
        await this.stagesStore.deleteStage(payload)
        this.showDelete = false
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
      }
    },
    async openEditDialog() {
      this.editStage = {
        title: this.stage.title,
        description: this.stage.description,
        dueDate: this.stage.dueDate,
      }
      this.showEditDialog = true
    },
    async handleUpdate() {

      const payload = {
        projectId: this.stagesStore.projectId,
        stageId: this.stage.id,
        title: this.editStage.title,
        description: this.editStage.description,
        dueDate: this.editStage.dueDate,
      }

      try {
        await this.stagesStore.updateStage(payload)
        this.showEditDialog = false
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
      }
    },
    openRelativeDialog() {
      this.relativeStage = {
        title: '',
        description: '',
        dueDate: '',
        position: 'after',
      }
      this.showRelativeDialog = true
    },
    async handleCreateRelative() {

      const payload = {
        projectId: this.stagesStore.projectId,
        referenceStageId: this.stage.id, // esošā stage ID
        title: this.relativeStage.title,
        description: this.relativeStage.description,
        dueDate: this.relativeStage.dueDate,
        position: this.relativeStage.position,
      }

      try {
        await this.stagesStore.createStageRelative(payload)
        this.showRelativeDialog = false
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
      }
    },
    async moveStage(direction) {
      const payload = {
        projectId: this.stagesStore.projectId,
        stageId: this.stage.id,
        direction: direction,
      }

      try {
        await this.stagesStore.moveStage(payload)
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
      }
    },
  },
  computed: {
    error() {
      return this.stagesStore.error
    }
  }
}
</script>
