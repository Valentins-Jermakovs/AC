<template>
  <!-- MEMBERS -->
  <div class="flex-1 flex flex-col w-full h-full p-3 sm:p-5 gap-3">
    <div class="w-full flex flex-col gap-4">
      <!-- HEADER -->
      <div class="w-full flex flex-col lg:flex-row gap-3 lg:items-center">
        <button class="btn btn-success w-full lg:h-full lg:w-auto" @click="openAddMemberModal">
          <font-awesome-icon icon="fa-solid fa-user-plus" />
          {{ $t('common.add_member') }}
        </button>

        <!-- SEARCH -->
        <div
          class="w-full flex flex-col sm:flex-row gap-2 border border-base-300 bg-base-100 p-2 wrap-break-word"
        >
          <input
            type="text"
            class="input w-full"
            :placeholder="$t('common.search')"
            v-model="workspaceProjectMembersStore.searchQuery"
            @keyup.enter="searchMembers"
            :disabled="workspaceProjectMembersStore.searchType === 'all'"
          />

          <select
            class="bg-neutral text-neutral-content select select-bordered w-full sm:w-40"
            v-model="workspaceProjectMembersStore.searchType"
          >
            <option value="all">{{ $t('filters.all') }}</option>
            <option value="email">{{ $t('filters.by_email') }}</option>
            <option value="role">{{ $t('filters.by_role') }}</option>
          </select>

          <button
            class="btn btn-primary w-full sm:w-auto"
            @click="searchMembers"
            :disabled="
              workspaceProjectMembersStore.searchType !== 'all' &&
              !workspaceProjectMembersStore.searchQuery.trim()
            "
          >
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>

      <!-- MEMBERS LIST -->
      <div
        class="w-full bg-base-200 border border-base-300 wrap-break-word p-2 sm:p-3 flex flex-col gap-3"
      >
        <div
          v-for="member in workspaceProjectMembersStore.projectMembers"
          :key="member.id"
          class="w-full flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 bg-base-100 border border-base-300 wrap-break-word"
        >
          <!-- EMAIL -->
          <div
            class="flex items-center gap-2 flex-1 bg-base-200 p-3 border border-base-300 wrap-break-word break-all"
          >
            <font-awesome-icon icon="fa-solid fa-user" />

            {{ member.email }}
          </div>

          <!-- ROLE -->
          <div class="badge badge-primary w-full md:w-fit">
            <p v-if="member.role == 'owner'">{{ $t('work.kanban.common.roles.owner') }}</p>
            <p v-if="member.role == 'admin'">{{ $t('work.kanban.common.roles.admin') }}</p>
            <p v-if="member.role == 'editor'">{{ $t('work.kanban.common.roles.editor') }}</p>
            <p v-if="member.role == 'viewer'">{{ $t('work.kanban.common.roles.viewer') }}</p>
          </div>

          <!-- ACTIONS -->
          <div class="dropdown dropdown-center md:dropdown-end">
            <div tabindex="0" role="button" class="btn w-full btn-neutral">⋮</div>

            <ul
              tabindex="0"
              class="dropdown-content menu bg-base-200 border border-base-300 wrap-break-word w-44 p-2 shadow"
            >
              <li>
                <button class="flex gap-2" @click="openUpdateMemberModal(member)">
                  <font-awesome-icon icon="fa-solid fa-pencil" />
                  {{ $t('work.kanban.common.update_role') }}
                </button>
              </li>

              <li>
                <button class="flex gap-2 text-error" @click="openDeleteMemberModal(member)">
                  <font-awesome-icon icon="fa-solid fa-trash" />
                  {{ $t('work.kanban.common.delete_member') }}
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
          class="p-4 text-center text-base-content/60 flex items-center justify-center gap-2"
        >
          <font-awesome-icon icon="fa-solid fa-users" class="text-3xl" />
          {{ $t('work.kanban.errors.members_not_found') }}
        </div>
      </div>

      <!-- FOOTER -->
      <div
        class="w-full flex flex-col sm:flex-row gap-3 sm:items-center bg-base-200 border border-base-300 wrap-break-word p-3 sm:px-4 sm:py-2"
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
        <div class="flex flex-col sm:flex-row gap-1 sm:gap-4 items-center md:items-start text-sm">
          <p>
            {{ $t('cabinet.admin.table_footer.total') }}
            <span class="font-semibold">
              {{ workspaceProjectMembersStore.meta.totalItems }}
            </span>
          </p>

          <p>
            {{ $t('cabinet.admin.table_footer.page') }}
            <span class="font-semibold">
              {{ workspaceProjectMembersStore.meta.page }}/
              {{ workspaceProjectMembersStore.meta.totalPages }}
            </span>
          </p>
        </div>

        <!-- PAGINATION -->
        <div class="flex flex-col md:flex-row gap-2 sm:ml-auto">
          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="workspaceProjectMembersStore.prevPage"
            :disabled="workspaceProjectMembersStore.meta.page === 1"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
          </button>

          <button
            class="btn w-full md:w-auto btn-neutral"
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
    :title="$t('work.kanban.modals.add_member.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmAddMember"
    @cancel="closeAddMemberModal"
  >
    <div class="w-full flex flex-col gap-2">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>
      <label for="memberEmail" class="label">
        {{ $t('work.kanban.modals.add_member.email') }}
      </label>
      <!-- Text input - member email -->
      <input
        type="email"
        class="input w-full"
        v-model="newMemberEmail"
        :placeholder="$t('work.kanban.modals.add_member.email_placeholder')"
      />
      <label for="memberRole" class="label">
        {{ $t('work.kanban.modals.add_member.role') }}
      </label>
      <!-- Select input - member role -->
      <select class="select select-bordered w-full" v-model="newMemberRole">
        <option value="admin">{{ $t('work.kanban.common.roles.admin') }}</option>
        <option value="editor">{{ $t('work.kanban.common.roles.editor') }}</option>
        <option value="viewer">{{ $t('work.kanban.common.roles.viewer') }}</option>
      </select>
    </div>
  </base-dialog>

  <!-- Update member role modal -->
  <base-dialog
    v-model="updateMemberModal"
    :title="$t('work.kanban.modals.update_member.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmUpdateMember"
    @cancel="closeUpdateMember"
  >
    <div class="w-full flex flex-col gap-5">
      <Transition name="error-slide">
        <div v-if="memberError">
          <h1 class="text-error mb-2">{{ memberError }}</h1>
        </div>
      </Transition>
      <!-- Select input - member role -->
      <select class="select select-bordered w-full" v-model="updatedRole">
        <option value="admin">{{ $t('work.kanban.common.roles.admin') }}</option>
        <option value="editor">{{ $t('work.kanban.common.roles.editor') }}</option>
        <option value="viewer">{{ $t('work.kanban.common.roles.viewer') }}</option>
      </select>
    </div>
  </base-dialog>

  <!-- Delete meber modal -->
  <base-dialog
    v-model="deleteMemberModal"
    :title="$t('work.kanban.modals.delete_member.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmDeleteMember"
    @cancel="closeDeleteMemberModal"
  >
    <div class="w-full flex flex-col gap-5">
      <Transition name="error-slide">
        <div v-if="memberError">
          <h1 class="text-error mb-2">{{ memberError }}</h1>
        </div>
      </Transition>
      <p>{{ $t('work.kanban.modals.delete_member.content') }}</p>
    </div>
  </base-dialog>

  <LoadingScreen v-if="workspaceProjectMembersStore.loading"></LoadingScreen>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'

import { useAdminStore } from '@/stores/admin'

// replace with
import { useWorkspaceProjectMembersStore } from '@/stores/workspace/projectsMembers'
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'MembersSpace',
  components: { BaseDialog, LoadingScreen },

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
    memberError() {
      return this.workspaceProjectMembersStore.error
    },
    error() {
      return this.adminStore.error
    },
  },

  async mounted() {
    if (!this.workspaceProjectsStore.selectedProject) return

    this.workspaceProjectMembersStore.setProjectId(this.workspaceProjectsStore.selectedProject.id)

    await this.workspaceProjectMembersStore.getAllMembers()
  },

  methods: {
    closeDeleteMemberModal() {
      this.deleteMemberModal = false
      this.workspaceProjectMembersStore.clearError()
    },
    closeUpdateMember() {
      this.updateMemberModal = false
      this.workspaceProjectMembersStore.clearError()
    },
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
      if (!this.newMemberEmail) {
        this.adminStore.error = 'Email is required'
        return
      }

      // validate email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.newMemberEmail)) {
        this.adminStore.error = 'Invalid email format'
        return
      }

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
