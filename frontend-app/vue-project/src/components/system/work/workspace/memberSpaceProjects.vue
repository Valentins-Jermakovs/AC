<template>
  <div
    v-if="workspaceProjectMembersStore.accessDenied"
    class="w-full h-full flex items-center justify-center"
  >
    <div class="bg-base-200 border border-base-300 p-10  text-center">
      <font-awesome-icon icon="fa-solid fa-lock" class="text-4xl mb-4 text-error" />

      <h2 class="text-xl font-bold">Access denied</h2>

      <p class="text-base-content/60">You don't have permission to view members</p>
    </div>
  </div>
  <!-- Members space -->
  <div v-else class="flex-1 flex flex-col w-full h-full p-5 gap-2">
    <div class="w-full h-full flex flex-col items-center gap-4 p-4">
      <div class="w-full flex justify-between items-center gap-2">
        <button class="btn btn-success h-full" @click="openAddMemberModal">
          <font-awesome-icon icon="fa-solid fa-user-plus" />
          Add member
        </button>

        <div class="w-full flex items-center gap-2 border border-base-300 bg-base-200 p-1">
          <input
            type="text"
            class="input w-full"
            placeholder="Search..."
            v-model="workspaceProjectMembersStore.searchQuery"
            @keyup.enter="searchMembers"
          />
          <!-- Filters -->
          <select
            class="select select-bordered bg-neutral text-neutral-content"
            v-model="workspaceProjectMembersStore.searchType"
          >
            <option value="all">All</option>
            <option value="email">By email</option>
            <option value="role">By role</option>
          </select>
          <button class="btn btn-primary btn-square" @click="searchMembers">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>

      <!-- Members list -->
      <div class="w-full bg-base-200 border border-base-300 flex flex-col gap-3 p-1">
        <div
          v-for="member in workspaceProjectMembersStore.projectMembers"
          :key="member.id"
          class="w-full p-1 bg-base-100 border border-base-300  flex items-center justify-between gap-3"
        >
          <div class="flex items-center gap-3 font-medium flex-1 p-2">
            <div
              class="flex w-full bg-base-200 p-3 items-center gap-2  border border-base-300"
            >
              <font-awesome-icon icon="fa-solid fa-user" />
              {{ member.email }}
            </div>
          </div>

          <div class="flex items-center gap-2 badge badge-primary ">
            {{ member.role }}
          </div>

          <div class="dropdown dropdown-left">
            <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
            <ul
              tabindex="0"
              class="dropdown-content menu bg-base-200 border border-base-300  w-48 p-2 shadow"
            >
              <li>
                <button class="flex gap-2" @click="openUpdateMemberModal(member)">
                  <font-awesome-icon icon="fa-solid fa-pencil" />
                  Update
                </button>
              </li>
              <li>
                <button class="flex gap-2 text-error" @click="openDeleteMemberModal(member)">
                  <font-awesome-icon icon="fa-solid fa-trash" />
                  Delete
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div
          v-if="
            !workspaceProjectMembersStore.loading &&
            workspaceProjectMembersStore.projectMembers.length === 0
          "
          class="p-4 text-center text-base-content/60"
        >
          No members found.
        </div>
      </div>

      <!-- Footer: limit & pagination -->
      <div class="w-full flex bg-base-200 border border-base-300 px-4 py-2 items-center gap-4">
        <div class="flex-1">
          <select
            class="select select-bordered"
            v-model="workspaceProjectMembersStore.meta.limit"
            @change="changeLimit($event.target.value)"
          >
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
          </select>
        </div>

        <div class="flex gap-4 text-sm">
          <p>
            Total:
            <span class="font-semibold">{{ workspaceProjectMembersStore.meta.totalItems }}</span>
          </p>
          <p>
            Page:
            <span class="font-semibold"
              >{{ workspaceProjectMembersStore.meta.page }}/{{
                workspaceProjectMembersStore.meta.totalPages
              }}</span
            >
          </p>
        </div>

        <div class="flex gap-2 ml-auto">
          <button
            class="btn btn-sm btn-neutral"
            @click="workspaceProjectMembersStore.prevPage"
            :disabled="workspaceProjectMembersStore.meta.page === 1"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
          </button>
          <button
            class="btn btn-sm btn-neutral"
            @click="workspaceProjectMembersStore.nextPage"
            :disabled="
              workspaceProjectMembersStore.meta.page ===
              workspaceProjectMembersStore.meta.totalPages
            "
          >
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modals -->

  <!-- Add member modal -->
  <base-dialog
    v-model="addMemberModal"
    title="Add Member"
    confirmText="Add"
    cancelText="Cancel"
    @confirm="confirmAddMember"
  >
    <div class="w-full flex flex-col gap-5">
      <!-- Text input - member email -->
      <input
        type="email"
        class="input w-full"
        placeholder="Enter member email"
        v-model="newMemberEmail"
      />
      <!-- Select input - member role -->
      <select class="select select-bordered w-full" v-model="newMemberRole">
        <option value="admin">Admin</option>
        <option value="editor">Editor</option>
        <option value="viewer">Viewer</option>
      </select>
    </div>
  </base-dialog>

  <!-- Update member role modal -->
  <base-dialog
    v-model="updateMemberModal"
    title="Update Member"
    confirmText="Update"
    cancelText="Cancel"
    @confirm="confirmUpdateMember"
  >
    <div class="w-full flex flex-col gap-5">
      <!-- Select input - member role -->
      <select class="select select-bordered w-full" v-model="updatedRole">
        <option value="admin">Admin</option>
        <option value="editor">Editor</option>
        <option value="viewer">Viewer</option>
      </select>
    </div>
  </base-dialog>

  <!-- Delete meber modal -->
  <base-dialog
    v-model="deleteMemberModal"
    title="Delete Member"
    confirmText="Delete"
    cancelText="Cancel"
    @confirm="confirmDeleteMember"
  >
    <div class="w-full flex flex-col gap-5">
      <p>Are you sure you want to delete this member?</p>
    </div>
  </base-dialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'

import { useAdminStore } from '@/stores/admin'

// replace with
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'MembersSpace',
  components: { BaseDialog },

  data() {
    return {
      workspaceProjectMembersStore: useWorkspaceProjectMembersStore(),
      workspaceProjectsStore: useWorkspaceProjectsStore(),
      adminStore: useAdminStore(),

      addMemberModal: false,
      updateMemberModal: false,
      deleteMemberModal: false,

      newMemberEmail: '',
      newMemberRole: 'viewer',
      updatedRole: 'viewer',
      selectedMember: null,
    }
  },

  async mounted() {
    if (!this.workspaceProjectsStore.selectedProject) return

    this.workspaceProjectMembersStore.setProjectId(this.workspaceProjectsStore.selectedProject.id)

    await this.workspaceProjectMembersStore.getAllMembers()
  },

  methods: {
    async searchMembers() {
      this.workspaceProjectMembersStore.meta.page = 1

      if (this.workspaceProjectMembersStore.searchType === 'all')
        return this.workspaceProjectMembersStore.getAllMembers()

      if (this.workspaceProjectMembersStore.searchType === 'email')
        return this.workspaceProjectMembersStore.getMemberByEmail()

      if (this.workspaceProjectMembersStore.searchType === 'role')
        return this.workspaceProjectMembersStore.getMemberByRole()
    },

    async changeLimit(limit) {
      await this.workspaceProjectMembersStore.setLimit(Number(limit))
    },

    async openUpdateMemberModal(member) {
      this.selectedMember = member

      this.updatedRole = member.role

      this.updateMemberModal = true
    },

    async confirmUpdateMember() {
      try {
        const payload = {
          userId: String(this.selectedMember.userId),
          projectId: this.workspaceProjectMembersStore.projectId,
          role: this.updatedRole,
        }

        await this.workspaceProjectMembersStore.updateMember(payload)

        this.updateMemberModal = false
      } catch (err) {
        console.error('Failed to update member:', err)
      }
    },

    async openDeleteMemberModal(member) {
      this.deleteMemberModal = true
      this.selectedMember = member
    },

    async confirmDeleteMember() {
      const payload = {
        userId: String(this.selectedMember.userId),
        projectId: this.workspaceProjectMembersStore.projectId,
      }

      try {
        await this.workspaceProjectMembersStore.deleteMember(payload)
        this.deleteMemberModal = false
      } catch (err) {
        console.error('Failed to delete member:', err)
      }
    },

    async openAddMemberModal() {
      this.addMemberModal = true
    },

    async confirmAddMember() {
      try {
        // send email to auth server - /users/email/{email}
        await this.adminStore.getUserByEmail(this.newMemberEmail)

        const addedUser = this.adminStore.userByEmail

        const payload = {
          email: addedUser.email,
          userId: String(addedUser.id),
          projectId: this.workspaceProjectMembersStore.projectId,
          role: this.newMemberRole,
        }

        await this.workspaceProjectMembersStore.addMember(payload)

        this.addMemberModal = false
        this.newMemberEmail = ''
        this.newMemberRole = 'viewer'
      } catch (err) {
        console.error('Failed to add member:', err)
      }
    },
  },
}
</script>

<style scoped></style>
