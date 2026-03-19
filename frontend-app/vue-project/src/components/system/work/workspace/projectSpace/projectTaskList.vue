<template>

  <div class="p-2 flex flex-col items-center bg-base-200 rounded-box border border-base-300">

    <ProjectTask
      v-for="task in tasksStore.getTasksByStage(stage.id)"
      :key="task.id"
      :task="task"
    />

    <div class="w-full flex items-center justify-center p-2">

      <button
        class="btn btn-primary"
        @click="openCreateDialog"
      >
        Create new task
      </button>

    </div>

  </div>


  <!-- CREATE -->
  <BaseDialog

    v-model="createDialog"

    title="Create task"

    confirmText="Create"
    cancelText="Cancel"

    @confirm="createTask"

  >

    <div class="flex flex-col gap-3 w-full">

      <input
        v-model="form.title"
        class="input input-bordered w-full"
        placeholder="Task title"
      >

      <textarea
        v-model="form.description"
        class="textarea textarea-bordered"
        placeholder="Description"
      ></textarea>


      <div class="flex gap-2">

        <select
          v-model="form.priority"
          class="select select-bordered flex-1"
        >
          <option :value="1">Priority 1</option>
          <option :value="2">Priority 2</option>
          <option :value="3">Priority 3</option>
        </select>

        <select
          v-model="form.storyPoints"
          class="select select-bordered flex-1"
        >
          <option :value="1">1 SP</option>
          <option :value="3">3 SP</option>
          <option :value="5">5 SP</option>
        </select>

      </div>


      <input
        type="date"
        v-model="form.dueDate"
        class="input input-bordered"
      >

    </div>

  </BaseDialog>

</template>

<script>

import ProjectTask from './projectTask.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'

import { useWorkspaceProjectsTasksStore } from '@/stores/workspace/projectsTasks'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {

  name:'ProjectTaskList',

  components:{
    ProjectTask,
    BaseDialog
  },

  props:{
    stage:{
      type:Object,
      required:true
    }
  },

  data(){
    return{

      tasksStore:useWorkspaceProjectsTasksStore(),
      projectsStore:useWorkspaceProjectsStore(),

      createDialog:false,

      form:{
        title:'',
        description:'',
        priority:1,
        storyPoints:1,
        status:'todo',
        dueDate:null
      }

    }
  },

  mounted(){

    this.tasksStore.projectId =
      this.projectsStore.selectedProject.id

    this.tasksStore.getTasks(
      this.stage.id
    )

  },

  methods:{

    openCreateDialog(){

      this.form={
        title:'',
        description:'',
        priority:1,
        storyPoints:1,
        status:'todo',
        dueDate:null
      }

      this.createDialog=true

    },

    async createTask(){

      if(!this.form.title) return

      try{

        const payload = {
          title: this.form.title,
          description: this.form.description,
          priority: this.form.priority,
          storyPoints: this.form.storyPoints,
          status: this.form.status,
          dueDate: this.form.dueDate,
          projectId: this.projectsStore.selectedProject.id,
          stageId: this.stage.id
        }

        await this.tasksStore.createTask(payload)

        this.createDialog=false

      }
      catch(e){

        console.error(e)

      }

    }

  }

}
</script>