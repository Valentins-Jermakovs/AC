<template>
    <!-- ACCESS DENIED -->
  <div
    v-if="workspaceProjectMembersStore.accessDenied"
    class="w-full h-full flex items-center justify-center p-4"
  >
    <div
      class="bg-base-200 border border-base-300 
      p-6 sm:p-10 
      rounded-box 
      text-center 
      max-w-md w-full"
    >
      <font-awesome-icon
        icon="fa-solid fa-lock"
        class="text-3xl sm:text-4xl mb-4 text-error"
      />

      <h2 class="text-lg sm:text-xl font-bold">
        Access denied
      </h2>

      <p class="text-sm sm:text-base text-base-content/60">
        You don't have permission to view members
      </p>
    </div>
  </div>

  <!-- MEMBERS -->
  <div
    v-else
    class="flex-1 flex flex-col w-full h-full 
    p-3 sm:p-5 
    gap-3"
  >

    <div
      class="w-full flex flex-col gap-4"
    >

      <!-- HEADER -->
      <div
        class="w-full 
        flex flex-col lg:flex-row 
        gap-3 
        lg:items-center"
      >

        <button
          class="btn btn-success w-full lg:w-auto"
          @click="openAddMemberModal"
        >
          <font-awesome-icon icon="fa-solid fa-user-plus"/>
          Add member
        </button>

        <!-- SEARCH -->
        <div
          class="w-full 
          flex flex-col sm:flex-row 
          gap-2 
          border border-base-300 
          bg-base-200 
          p-2 
          rounded-box"
        >

          <input
            type="text"
            class="input w-full"
            placeholder="Search..."
            v-model="workspaceProjectMembersStore.searchQuery"
            @keyup.enter="searchMembers"
          />

          <select
            class="select select-bordered w-full sm:w-40"
            v-model="workspaceProjectMembersStore.searchType"
          >
            <option value="all">All</option>
            <option value="email">By email</option>
            <option value="role">By role</option>
          </select>

          <button
            class="btn btn-primary w-full sm:w-auto"
            @click="searchMembers"
          >
            <font-awesome-icon icon="fa-solid fa-magnifying-glass"/>
          </button>

        </div>

      </div>

      <!-- MEMBERS LIST -->
      <div class="w-full bg-base-200 border border-base-300 rounded-box p-2 sm:p-3 flex flex-col gap-3">


        <div
    v-for="member in workspaceProjectMembersStore.projectMembers"
    :key="member.id"
    class="
      w-full
      flex flex-col sm:flex-row sm:items-center
      justify-between
      gap-3
      p-3
      bg-base-100
      border border-base-300
      rounded-box
    "
  >

          <!-- EMAIL -->
          <div
            class="flex items-center gap-2 
            flex-1 
            bg-base-200 
            p-3 
            border border-base-300 
            rounded-box
            break-all"
          >
            <font-awesome-icon icon="fa-solid fa-user"/>

            {{ member.email }}

          </div>

          <!-- ROLE -->
          <div
            class="badge badge-primary 
            self-start sm:self-auto
            w-full sm:w-auto"
          >
            {{ member.role }}
          </div>

          <!-- ACTIONS -->
          <div class="dropdown dropdown-center md:dropdown-end">

            <div
              tabindex="0"
              role="button"
              class="btn w-full btn-neutral"
            >
              ⋮
            </div>

            <ul
              tabindex="0"
              class="dropdown-content 
              menu 
              bg-base-200 
              border border-base-300 
              rounded-box
              w-44 
              p-2 
              shadow"
            >

              <li>
                <button
                  class="flex gap-2"
                  @click="openUpdateMemberModal(member)"
                >
                  <font-awesome-icon icon="fa-solid fa-pencil"/>
                  Update
                </button>
              </li>

              <li>
                <button
                  class="flex gap-2 text-error"
                  @click="openDeleteMemberModal(member)"
                >
                  <font-awesome-icon icon="fa-solid fa-trash"/>
                  Delete
                </button>
              </li>

            </ul>

          </div>

        </div>

        <!-- EMPTY -->
        <div
          v-if="
            !workspaceProjectMembersStore.loading &&
            workspaceProjectMembersStore.projectMembers.length === 0
          "
          class="p-6 text-center text-base-content/60"
        >
          No members found
        </div>

      </div>

      <!-- FOOTER -->
      <div
        class="
        w-full 
        flex flex-col sm:flex-row 
        gap-3 
        sm:items-center

        bg-base-200 
        border border-base-300 
        rounded-box

        p-3 sm:px-4 sm:py-2"
      >

        <!-- LIMIT -->
        <div>
          <select
            class="select select-bordered w-full sm:w-24"
            v-model="workspaceProjectMembersStore.meta.limit"
            @change="changeLimit($event.target.value)"
          >
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
          </select>
        </div>

        <!-- META -->
        <div
          class="flex flex-col sm:flex-row 
          gap-1 sm:gap-4 items-center md:items-start
          text-sm"
        >

          <p>
            Total:
            <span class="font-semibold">
              {{ workspaceProjectMembersStore.meta.totalItems }}
            </span>
          </p>

          <p>
            Page:
            <span class="font-semibold">
              {{ workspaceProjectMembersStore.meta.page }}/
              {{ workspaceProjectMembersStore.meta.totalPages }}
            </span>
          </p>

        </div>

        <!-- PAGINATION -->
        <div
          class="flex flex-col md:flex-row gap-2 sm:ml-auto"
        >

          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="workspaceProjectMembersStore.prevPage"
            :disabled="workspaceProjectMembersStore.meta.page === 1"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-left"/>
          </button>

          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="workspaceProjectMembersStore.nextPage"
            :disabled="
              workspaceProjectMembersStore.meta.page ===
              workspaceProjectMembersStore.meta.totalPages
            "
          >
            <font-awesome-icon icon="fa-solid fa-arrow-right"/>
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
    @cancel="closeAddMemberModal"
  >
    <div class="w-full flex flex-col gap-5">
      <Transition name="error-slide">
        <div v-if="error || adminError">
          <h1 class="text-error mb-2">{{ error }}</h1>
          <h1 class="text-error mb-2">{{ adminError }}</h1>
        </div>
      </Transition>
      <label for="memberEmail" class="label">Member Email</label>
      <!-- Text input - member email -->
      <input
        type="email"
        class="input w-full"
        placeholder="Enter member email"
        v-model="newMemberEmail"
      />
      <label for="memberRole" class="label">Member Role</label>
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

  computed: {
    error() {
      return this.workspaceProjectMembersStore.error
    },
    adminError() {
      return this.adminStore.error
    }
  },

  async mounted() {
    if (!this.workspaceProjectsStore.selectedProject) return

    this.workspaceProjectMembersStore.setProjectId(this.workspaceProjectsStore.selectedProject.id)

    await this.workspaceProjectMembersStore.getAllMembers()
  },

  methods: {
    closeAddMemberModal() {
      this.adminStore.clearError()
      this.workspaceProjectMembersStore.clearError()
      this.addMemberModal = false
      this.newMemberEmail = ''
      this.newMemberRole = 'viewer'
    },
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
