<template>
  <div class="drawer drawer-end">
    <!-- drawer toggle -->
    <input type="checkbox" class="drawer-toggle" v-model="drawerOpen" />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div class="w-full bg-base-100 border border-base-300 rounded-box p-4 flex flex-col gap-4 mt-5">
        <!-- HEADER -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <h3 class="font-semibold text-lg">{{ stage.title }}</h3>
            <div class="flex gap-2">
              <div class="badge badge-neutral gap-2">
                <font-awesome-icon icon="fa-solid fa-calendar" /> {{ stage.createdAt }}
              </div>
              <div class="badge badge-warning gap-2">
                <font-awesome-icon icon="fa-solid fa-clock" /> {{ stage.dueDate }}
              </div>
            </div>
          </div>
          <button class="btn btn-primary btn-sm gap-2" @click="drawerOpen = true">
            <font-awesome-icon icon="fa-solid fa-bars" /> Info
          </button>
        </div>

        <!-- TASKS -->
        <ProjectTaskList :stage="stage" />
      </div>
    </div>

    <!-- DRAWER -->
    <div class="drawer-side">
      <label class="drawer-overlay" @click="drawerOpen = false"></label>

      <div class="bg-base-200 min-h-full w-96 p-6 flex flex-col gap-6">
        <!-- TITLE -->
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-semibold">{{ stage.title }}</h2>
          <button class="btn btn-ghost btn-sm btn-circle" @click="drawerOpen = false">✕</button>
        </div>

        <!-- ACTIONS -->
        <div class="bg-base-100 border border-base-300 rounded-box w-full">
          <ul class="menu w-full">
            <li>
              <button class="flex gap-3" @click="showCreateDialog = true">
                <font-awesome-icon icon="fa-solid fa-plus" /> Add stage
              </button>
            </li>
            <li>
              <button class="flex gap-3" @click="openRelativeDialog">
                <font-awesome-icon icon="fa-solid fa-code-branch" /> Add relative stage
              </button>
            </li>
            <li>
              <button class="flex gap-3" @click="openEditDialog">
                <font-awesome-icon icon="fa-solid fa-pen" /> Edit stage
              </button>
            </li>
            <li>
              <button class="flex gap-3" @click="moveStage('up')">
                <font-awesome-icon icon="fa-solid fa-arrow-up" />
                Move up
              </button>
            </li>

            <li>
              <button class="flex gap-3" @click="moveStage('down')">
                <font-awesome-icon icon="fa-solid fa-arrow-down" />
                Move down
              </button>
            </li>
            <li class="border-t border-base-300 mt-2 pt-2">
              <button class="text-error flex gap-3" @click="showDelete = true">
                <font-awesome-icon icon="fa-solid fa-trash" /> Delete stage
              </button>
            </li>
          </ul>
        </div>

        <!-- DESCRIPTION -->
        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-4">
            <h3 class="font-semibold text-sm opacity-70">Description</h3>
            <p class="text-sm">{{ stage.description }}</p>
          </div>
        </div>

        <!-- META -->
        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-4">
            <h3 class="font-semibold text-sm opacity-70 mb-2">Metadata</h3>
            <table class="table table-sm">
              <tbody>
                <tr>
                  <td class="opacity-60">Created</td>
                  <td class="font-medium">{{ stage.createdAt }}</td>
                </tr>
                <tr>
                  <td class="opacity-60">Due date</td>
                  <td class="font-medium">{{ stage.dueDate }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- CLOSE -->
        <button class="btn btn-neutral mt-auto" @click="drawerOpen = false">Close</button>
      </div>
    </div>
  </div>

  <!-- Create stage dialog -->
  <BaseDialog v-model="showCreateDialog" title="Create new stage" confirmText="Create" cancelText="Cancel"
    @confirm="handleCreate">
    <div class="flex flex-col gap-2 w-full">
      <input v-model="newStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <textarea v-model="newStage.description" class="textarea w-full" placeholder="Stage description"></textarea>
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
    @confirm="handleUpdate">
    <div class="flex flex-col gap-2 w-full">
      <input v-model="editStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <textarea v-model="editStage.description" class="textarea w-full" placeholder="Stage description"></textarea>
      <input v-model="editStage.dueDate" type="date" class="input w-full" />
    </div>
  </BaseDialog>

  <!-- Relative stage dialog -->
  <BaseDialog v-model="showRelativeDialog" title="Add relative stage" confirmText="Create" cancelText="Cancel"
    @confirm="handleCreateRelative">
    <div class="flex flex-col gap-2 w-full">
      <input v-model="relativeStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <textarea v-model="relativeStage.description" class="textarea w-full" placeholder="Stage description"></textarea>
      <input v-model="relativeStage.dueDate" type="date" class="input w-full" />
      <div class="flex gap-2 items-center mt-2">
        <label class="flex items-center gap-1">
          <input type="radio" value="before" v-model="relativeStage.position" />
          Before
        </label>
        <label class="flex items-center gap-1">
          <input type="radio" value="after" v-model="relativeStage.position" />
          After
        </label>
      </div>
    </div>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';
import ProjectTaskList from './projectTaskList.vue'
import { useWorkspaceProjectStagesStore } from '@/stores/workspace/projectStages';

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
        dueDate: ''
      },
      editStage: {                   // ← form data for editing
        title: '',
        description: '',
        dueDate: ''
      },
      relativeStage: {                  // ← form dati relative stage
        title: '',
        description: '',
        dueDate: '',
        position: 'after'               // default: after
      }
    }
  },
  methods: {
    async handleCreate() {
      if (!this.newStage.title) return alert('Title is required');

      const payload = {
        title: this.newStage.title,
        description: this.newStage.description,
        dueDate: this.newStage.dueDate,
        projectId: this.stagesStore.projectId
      }

      try {
        await this.stagesStore.createStage(
          payload
        );

        // Reset form and close dialog
        this.newStage = { title: '', description: '', dueDate: '' };
        this.showCreateDialog = false;
        this.drawerOpen = false;
      } catch (err) {
        console.error(err);
        alert('Error creating stage: ' + err);
      }
    },
    async handleDelete() {
      const payload = {
        projectId: this.stagesStore.projectId,
        stageId: this.stage.id
      }
      try {
        await this.stagesStore.deleteStage(payload);
        this.showDelete = false;
        this.drawerOpen = false;
      } catch (err) {
        console.error(err);
        alert('Error deleting stage: ' + err);
      }
    },
    async openEditDialog() {
      this.editStage = {
        title: this.stage.title,
        description: this.stage.description,
        dueDate: this.stage.dueDate
      }
      this.showEditDialog = true
    },
    async handleUpdate() {
      if (!this.editStage.title) return alert('Title is required');

      const payload = {
        projectId: this.stagesStore.projectId,
        stageId: this.stage.id,
        title: this.editStage.title,
        description: this.editStage.description,
        dueDate: this.editStage.dueDate
      }

      try {
        await this.stagesStore.updateStage(payload)
        this.showEditDialog = false
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
        alert('Error updating stage: ' + err)
      }
    },
    openRelativeDialog() {
      this.relativeStage = {
        title: '',
        description: '',
        dueDate: '',
        position: 'after'
      }
      this.showRelativeDialog = true
    },
    async handleCreateRelative() {
      if (!this.relativeStage.title) return alert('Title is required');

      const payload = {
        projectId: this.stagesStore.projectId,
        referenceStageId: this.stage.id,   // esošā stage ID
        title: this.relativeStage.title,
        description: this.relativeStage.description,
        dueDate: this.relativeStage.dueDate,
        position: this.relativeStage.position
      }

      try {
        await this.stagesStore.createStageRelative(payload)
        this.showRelativeDialog = false
        this.drawerOpen = false
      } catch (err) {
        console.error(err)
        alert('Error creating relative stage: ' + err)
      }
    },
    async moveStage(direction) {

      const payload = {
        projectId: this.stagesStore.projectId,
        stageId: this.stage.id,
        direction: direction
      }

      try {
        await this.stagesStore.moveStage(payload)
        this.drawerOpen = false
      }
      catch (err) {
        console.error(err)
        alert('Error moving stage: ' + err)
      }

    }
  },
}
</script>
