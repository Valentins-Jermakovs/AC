<template>
  <div class="w-full p-2 flex flex-wrap bg-base-100 border border-base-300 gap-2 items-center">
    <!-- Project view -->
    <button
      class="btn flex-1 sm:flex-none"
      :class="activeView === 'project' ? 'btn-primary' : 'btn-neutral'"
      @click="$emit('update:activeView', 'project')"
    >
      <font-awesome-icon icon="fa-solid fa-list" />
      <span class="hidden sm:inline">
        {{ $t('work.projects.controls.project_view') }}
      </span>
    </button>

    <!-- Members -->
    <button
      v-if="projectMemberStore.currentUser && projectMemberStore.currentUser.role === 'owner'"
      class="btn flex-1 sm:flex-none"
      :class="activeView === 'members' ? 'btn-primary' : 'btn-neutral'"
      @click="$emit('update:activeView', 'members')"
    >
      <font-awesome-icon icon="fa-solid fa-users" />
      <span class="hidden sm:inline">
        {{ $t('work.projects.controls.members_view') }}
      </span>
    </button>

    <!-- Edit -->
    <button
      class="btn btn-neutral flex-1 sm:flex-none sm:ml-auto"
      @click="openEdit"
      v-if="projectMemberStore.currentUser && projectMemberStore.currentUser.role === 'owner'"
    >
      <font-awesome-icon icon="fa-solid fa-pen-to-square" />
      <span class="hidden md:inline">
        {{ $t('work.projects.controls.edit_project') }}
      </span>
    </button>
    <!-- Delete -->
    <button
      v-if="projectMemberStore.currentUser && projectMemberStore.currentUser.role === 'owner'"
      class="btn btn-neutral flex-1 sm:flex-none"
      @click="showDelete = true"
    >
      <font-awesome-icon icon="fa-solid fa-trash" />
      <span class="hidden md:inline">
        {{ $t('work.projects.controls.delete_project') }}
      </span>
    </button>

    <!-- Leave -->
    <button
      v-if="projectMemberStore.currentUser && projectMemberStore.currentUser.role !== 'owner'"
      @click="showLeave = true"
      class="btn btn-neutral flex-1 sm:flex-none sm:ml-auto"
    >
      <font-awesome-icon icon="fa-solid fa-arrow-right-from-bracket" />
      <span class="hidden md:inline">
        {{ $t('work.projects.controls.leave_project') }}
      </span>
    </button>

    <!-- Back -->
    <button class="btn btn-neutral w-full sm:w-auto" @click="goToProjects">
      <font-awesome-icon icon="fa-solid fa-arrow-left" />
      <span class="hidden md:inline">
        {{ $t('work.projects.controls.back_to_list') }}
      </span>
    </button>
  </div>

  <base-dialog
    v-model="showEdit"
    :title="$t('work.projects.modals.edit_project.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="updateProject"
  >
    <div class="flex flex-col w-full gap-2">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label class="label">
        <span class="label-text">
          {{ $t('work.projects.modals.edit_project.name') }}
        </span>
      </label>
      <input
        v-model="editProject.title"
        type="text"
        class="input input-bordered w-full"
        :placeholder="$t('work.projects.modals.edit_project.name_placeholder')"
      />
      <label class="label">
        <span class="label-text">
          {{ $t('work.projects.modals.edit_project.description') }}
        </span>
      </label>
      <textarea
        v-model="editProject.description"
        maxlength="1000"
        class="textarea textarea-bordered w-full"
        :placeholder="$t('work.projects.modals.edit_project.description_placeholder')"
      ></textarea>
    </div>
  </base-dialog>

  <!-- Delete dialog -->
  <base-dialog
    v-model="showDelete"
    :title="$t('work.projects.modals.delete_project.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="deleteProject"
  >
    <p>
      {{ $t('work.projects.modals.delete_project.content') }}
    </p>
  </base-dialog>

  <!-- Leave dialog -->
  <base-dialog
    v-model="showLeave"
    :title="$t('work.projects.modals.leave_project.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="leaveProject"
  >
    <p>
      {{ $t('work.projects.modals.leave_project.content') }}
    </p>
  </base-dialog>
</template>

<script>
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import { useSelectedProjectStore } from '@/stores/selectedProject'
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  components: { BaseDialog },

  props: {
    activeView: {
      type: String,
      default: 'project',
    },
  },

  data() {
    return {
      projectMemberStore: useWorkspaceProjectMembersStore(),
      store: useWorkspaceProjectsStore(),
      selectedProjectStore: useSelectedProjectStore(),

      showDelete: false,
      showEdit: false,
      showLeave: false,
      error: '',

      editProject: {
        title: '',
        description: '',
        projectId: '',
      },
    }
  },

  methods: {
    goToProjects() {
      this.store.selectedProject = null
      this.projectMemberStore.projectId = null
    },
    async deleteProject() {
      await this.store.deleteProject({
        projectId: this.store.selectedProject.id,
      })

      this.selectedProjectStore.clearSelectedProject()

      this.showDelete = false
      this.goToProjects()
    },
    openEdit() {
      const project = this.store.selectedProject

      this.editProject = {
        title: project.title,
        description: project.description,
        projectId: project.id,
      }

      this.showEdit = true
    },
    async updateProject() {
      if (!this.editProject.title) {
        this.store.error = 'Title is required'
        return
      }

      try {
        await this.store.updateProject(this.editProject)

        this.store.selectedProject.title = this.editProject.title
        this.store.selectedProject.description = this.editProject.description

        this.showEdit = false

        const payload = {
          workspaceId: this.store.selectedProject.id,
          workspaceTitle: this.store.selectedProject.title,
        }

        this.selectedProjectStore.setSelectedProject(payload)
      } catch (err) {
        console.error(err)
      }
    },
    async leaveProject() {
      if (!this.projectMemberStore.currentUser || !this.store.selectedProject) return
      const payload = {
        userId: this.projectMemberStore.currentUser.userId,
        projectId: this.store.selectedProject.id,
      }

      await this.projectMemberStore.deleteMember(payload)
      this.showLeave = false
      this.goToProjects()
      this.store.getAllProjects()
    },
  },

  mounted() {
    this.projectMemberStore.fetchMe()
  },
}
</script>
