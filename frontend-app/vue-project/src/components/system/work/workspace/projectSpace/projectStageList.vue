<template>
  <div class="w-full flex justify-center">
    <div class="w-4/5 bg-base-200 border border-base-300 p-1 mt-10">

      <!-- List of stages -->
      <ProjectStage
        v-for="stage in stagesStore.projectStages"
        :key="stage.id"
        :stage="stage"
      ></ProjectStage>

      <!-- Create new stage button -->
      <div class="w-full flex items-center justify-center p-2">
        <button class="btn btn-primary" @click="showDialog = true">Create new stage</button>
      </div>
    </div>
  </div>

  <!-- Create stage dialog -->
  <BaseDialog v-model="showDialog" title="Create new stage" confirmText="Create" cancelText="Cancel" @confirm="handleCreate">
    <div class="flex flex-col gap-2 w-full">
      <input v-model="newStage.title" type="text" class="input w-full" placeholder="Stage title" />
      <textarea v-model="newStage.description" class="textarea w-full" placeholder="Stage description"></textarea>
      <input v-model="newStage.dueDate" type="date" class="input w-full" />
    </div>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';
import ProjectStage from './projectStage.vue';
import { useWorkspaceProjectStagesStore } from '@/stores/workspace/projectStages';
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects';

export default {
  name: 'ProjectStageList',
  components: { ProjectStage, BaseDialog },

  data() {
    return {
      stagesStore: useWorkspaceProjectStagesStore(),
      projectsStore: useWorkspaceProjectsStore(),

      showDialog: false,
      newStage: {
        title: '',
        description: '',
        dueDate: ''
      }
    }
  },

  mounted() {
    this.stagesStore.projectId = this.projectsStore.selectedProject.id;
    if (this.stagesStore.projectId) {
      this.stagesStore.getStages();
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
        this.showDialog = false;
      } catch (err) {
        console.error(err);
        alert('Error creating stage: ' + err);
      }
    }
  }
}
</script>

<style scoped></style>