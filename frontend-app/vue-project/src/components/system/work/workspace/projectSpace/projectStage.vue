<template>
  <div class="drawer drawer-end">
    <!-- drawer toggle -->
    <input type="checkbox" class="drawer-toggle" v-model="drawerOpen" />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div
        class="w-full bg-base-100 border border-base-300 p-3 sm:p-4 flex flex-col gap-4 mt-3 sm:mt-5"
      >
        <!-- HEADER -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
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
      <label class="drawer-overlay" @click="drawerOpen = false"></label>

      <div
        class="bg-base-200 min-h-full w-full sm:w-96 p-4 sm:p-6 flex flex-col gap-6 overflow-y-auto"
      >
        <!-- TITLE -->
        <div class="flex items-center justify-between gap-2">
          <h2 class="text-xl sm:text-2xl font-semibold wrap-break-word">
            {{ stage.title }}
          </h2>

          <button class="btn btn-ghost btn-sm btn-circle" @click="drawerOpen = false">✕</button>
        </div>

        <!-- ACTIONS -->
        <div class="bg-base-100 border border-base-300 w-full">
          <ul class="menu w-full">
            <li>
              <button class="flex gap-3 items-center" @click="showCreateDialog = true">
                <font-awesome-icon icon="fa-solid fa-plus" />
                {{ $t('work.projects.drawer.add_sprint') }}
              </button>
            </li>

            <li>
              <button class="flex gap-3 items-center" @click="openRelativeDialog">
                <font-awesome-icon icon="fa-solid fa-code-branch" />
                {{ $t('work.projects.drawer.add_relative_sprint') }}
              </button>
            </li>

            <li>
              <button class="flex gap-3 items-center" @click="openEditDialog">
                <font-awesome-icon icon="fa-solid fa-pen" />
                {{ $t('work.projects.drawer.edit_sprint') }}
              </button>
            </li>

            <li>
              <button class="flex gap-3 items-center" @click="moveStage('up')">
                <font-awesome-icon icon="fa-solid fa-arrow-up" />
                {{ $t('work.projects.drawer.move_up') }}
              </button>
            </li>

            <li>
              <button class="flex gap-3 items-center" @click="moveStage('down')">
                <font-awesome-icon icon="fa-solid fa-arrow-down" />
                {{ $t('work.projects.drawer.move_down') }}
              </button>
            </li>

            <li class="border-t border-base-300 mt-2 pt-2">
              <button class="text-error flex gap-3 items-center" @click="showDelete = true">
                <font-awesome-icon icon="fa-solid fa-trash" />
                {{ $t('work.projects.drawer.delete_sprint') }}
              </button>
            </li>
          </ul>
        </div>

        <!-- DESCRIPTION -->
        <div class="bg-base-100 border border-base-300">
          <div class="p-4">
            <h3 class="font-semibold text-sm opacity-70">
              {{ $t('work.projects.drawer.description') }}
            </h3>

            <p class="text-sm wrap-break-word">
              {{ stage.description }}
            </p>
          </div>
        </div>

        <!-- META -->
        <div class="bg-base-100 border border-base-300">
          <div class="p-4">
            <h3 class="font-semibold text-sm opacity-70 mb-2">
              {{ $t('work.projects.drawer.metadata') }}
            </h3>

            <div class="overflow-x-auto">
              <table class="table table-sm">
                <tbody>
                  <tr>
                    <td class="opacity-60">
                      <font-awesome-icon icon="fa-solid fa-calendar" />
                      {{ $t('work.projects.drawer.start_date') }}
                    </td>

                    <td class="font-medium">
                      {{ stage.createdAt }}
                    </td>
                  </tr>

                  <tr>
                    <td class="opacity-60">
                      <font-awesome-icon icon="fa-solid fa-clock" />
                      {{ $t('work.projects.drawer.end_date') }}
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
        <button class="btn btn-neutral mt-auto w-full" @click="drawerOpen = false">
          {{ $t('common.close') }}
        </button>
      </div>
    </div>
  </div>

  <!-- Create stage dialog -->
  <BaseDialog
    v-model="showCreateDialog"
    :title="$t('work.projects.modals.create_new_sprint.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="handleCreate"
    @cancel="closeCreateDialog"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">
        {{ $t('work.projects.modals.create_new_sprint.name') }}
      </label>
      <input
        v-model="newStage.title"
        type="text"
        class="input w-full"
        :placeholder="$t('work.projects.modals.create_new_sprint.name_placeholder')"
      />
      <label for="stageDescription" class="label">
        {{ $t('work.projects.modals.create_new_sprint.description') }}
      </label>
      <textarea
        v-model="newStage.description"
        class="textarea w-full min-h-52"
        :placeholder="$t('work.projects.modals.create_new_sprint.description_placeholder')"
      ></textarea>
      <div class="flex flex-col gap-1">
        <label class="label">
          {{ $t('work.projects.modals.create_new_sprint.start_date') }}
        </label>

        <input v-model="newStage.createdAt" type="date" class="input w-full" />
      </div>
      <label for="stageDueDate" class="label">
        {{ $t('work.projects.modals.create_new_sprint.due_date') }}
      </label>
      <input v-model="newStage.dueDate" type="date" class="input w-full" />
    </div>
  </BaseDialog>
  <!-- Delete confirmation dialog -->
  <BaseDialog
    v-model="showDelete"
    :title="$t('work.projects.modals.delete_sprint.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="handleDelete"
  >
    <p>
      {{ $t('work.projects.modals.delete_sprint.content') }}
    </p>
  </BaseDialog>
  <!-- Edit stage dialog -->
  <BaseDialog
    v-model="showEditDialog"
    :title="$t('work.projects.modals.edit_sprint.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="handleUpdate"
    @cancel="closeEditDialog"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">
        {{ $t('work.projects.modals.edit_sprint.name') }}
      </label>
      <input
        v-model="editStage.title"
        type="text"
        class="input w-full"
        :placeholder="$t('work.projects.modals.edit_sprint.name_placeholder')"
      />
      <label for="stageDescription" class="label">
        {{ $t('work.projects.modals.edit_sprint.description') }}
      </label>
      <textarea
        v-model="editStage.description"
        class="textarea w-full min-h-52"
        :placeholder="$t('work.projects.modals.edit_sprint.description_placeholder')"
      ></textarea>
      <label for="stageDueDate" class="label">
        {{ $t('work.projects.modals.edit_sprint.due_date') }}
      </label>
      <input v-model="editStage.createdAt" type="date" class="input w-full" />
      <label for="stageDueDate" class="label">
        {{ $t('work.projects.modals.edit_sprint.due_date') }}
      </label>
      <input v-model="editStage.dueDate" type="date" class="input w-full" />
    </div>
  </BaseDialog>

  <!-- Relative stage dialog -->
  <BaseDialog
    v-model="showRelativeDialog"
    :title="$t('work.projects.modals.create_sprint_relative.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="handleCreateRelative"
    @cancel="closeRelativeDialog"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">
        {{ $t('work.projects.modals.create_sprint_relative.name') }}
      </label>
      <input
        v-model="relativeStage.title"
        type="text"
        class="input w-full"
        :placeholder="$t('work.projects.modals.create_sprint_relative.name_placeholder')"
      />
      <label for="stageDescription" class="label">
        {{ $t('work.projects.modals.create_sprint_relative.description') }}
      </label>
      <textarea
        v-model="relativeStage.description"
        class="textarea w-full min-h-52"
        :placeholder="$t('work.projects.modals.create_sprint_relative.description_placeholder')"
      ></textarea>
      <div class="flex flex-col gap-1">
        <label class="label">
          {{ $t('work.projects.modals.create_new_sprint.start_date') }}
        </label>

        <input v-model="relativeStage.createdAt" type="date" class="input w-full" />
      </div>
      <label for="stageDueDate" class="label">
        {{ $t('work.projects.modals.create_sprint_relative.due_date') }}
      </label>
      <input v-model="relativeStage.dueDate" type="date" class="input w-full" />
      <div class="flex gap-2 items-center mt-2">
        <label class="flex items-center gap-1">
          <input type="radio" value="before" class="radio" v-model="relativeStage.position" />
          {{ $t('work.projects.modals.create_sprint_relative.before') }}
        </label>
        <label class="flex items-center gap-1">
          <input type="radio" value="after" class="radio" v-model="relativeStage.position" />
          {{ $t('work.projects.modals.create_sprint_relative.after') }}
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
        createdAt: '',
      },
      editStage: {
        // ← form data for editing
        title: '',
        description: '',
        dueDate: '',
        createdAt: '',
      },
      relativeStage: {
        // ← form dati relative stage
        title: '',
        description: '',
        dueDate: '',
        createdAt: '',
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
        createdAt: this.newStage.createdAt,
        projectId: this.stagesStore.projectId,
      }

      try {
        await this.stagesStore.createStage(payload)

        // Reset form and close dialog
        this.newStage = { title: '', description: '', dueDate: '', createdAt: '' }
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
        createdAt: this.stage.createdAt,
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
        createdAt: this.editStage.createdAt,
      }

      try {
        await this.stagesStore.updateStage(payload)
        this.showEditDialog = false
        this.drawerOpen = false

        this.editStage = {
          title: '',
          description: '',
          dueDate: '',
          createdAt: '',
        }
      } catch (err) {
        console.error(err)
      }
    },
    openRelativeDialog() {
      this.relativeStage = {
        title: '',
        description: '',
        dueDate: '',
        createdAt: '',
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
        createdAt: this.relativeStage.createdAt,
        position: this.relativeStage.position,
      }

      try {
        await this.stagesStore.createStageRelative(payload)
        this.showRelativeDialog = false
        this.drawerOpen = false

        this.relativeStage = {
          title: '',
          description: '',
          dueDate: '',
          createdAt: '',
          position: 'after',
        }
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
    },
  },
}
</script>
