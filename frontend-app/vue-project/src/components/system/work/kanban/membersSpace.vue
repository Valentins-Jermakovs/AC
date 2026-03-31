<template>
  <!-- ACCESS DENIED -->
  <div
    v-if="kanbanMembersStore.accessDenied"
    class="w-full h-full flex items-center justify-center p-4 flex-1"
  >
    <div class="bg-base-200 border border-base-300 p-6 md:p-10 text-center max-w-md w-full">
      <font-awesome-icon icon="fa-solid fa-lock" class="text-3xl md:text-4xl mb-4 text-error" />

      <h2 class="text-lg md:text-xl font-bold">
        {{ $t('work.kanban.errors.access_denied.title') }}
      </h2>

      <p class="text-base-content/60">{{ $t('work.kanban.errors.access_denied.description') }}</p>
    </div>
  </div>

  <!-- MEMBERS -->
  <div v-else class="flex-1 flex flex-col w-full h-full overflow-auto p-2 md:p-5 gap-3">
    <div class="w-full h-full flex flex-col items-center gap-4">
      <!-- HEADER -->
      <div
        class="w-full md:w-3/5 flex flex-col md:flex-row justify-between items-stretch md:items-center gap-2"
      >
        <button class="btn btn-success w-full md:w-auto md:h-full" @click="openAddMemberModal">
          <font-awesome-icon icon="fa-solid fa-user-plus" />
          {{ $t('common.add_member') }}
        </button>

        <!-- SEARCH -->
        <div
          class="w-full flex flex-col md:flex-row items-stretch md:items-center gap-2 border border-base-300 bg-base-200 p-2"
        >
          <input
            type="text"
            class="input w-full"
            :placeholder="$t('common.search')"
            v-model="kanbanMembersStore.searchQuery"
            @keyup.enter="searchMembers"
            :disabled="
              kanbanMembersStore.searchType === 'all' && kanbanMembersStore.searchQuery.length < 3
            "
          />

          <select
            class="select select-bordered w-full md:w-40 bg-neutral text-neutral-content"
            v-model="kanbanMembersStore.searchType"
          >
            <option value="all">{{ $t('filters.all') }}</option>
            <option value="email">{{ $t('filters.by_email') }}</option>
            <option value="role">{{ $t('filters.by_role') }}</option>
          </select>

          <button
            class="btn btn-primary w-full md:w-auto"
            @click="searchMembers"
            :disabled="
              kanbanMembersStore.searchType !== 'all' && !kanbanMembersStore.searchQuery.trim()
            "
          >
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>

      <!-- MEMBERS LIST -->
      <div class="w-full md:w-3/5 bg-base-200 border border-base-300 flex flex-col gap-2 p-2">
        <div
          v-for="member in kanbanMembersStore.members"
          :key="member.id"
          class="w-full p-2 bg-base-100 border border-base-300 flex flex-col md:flex-row md:items-center md:justify-between gap-2"
        >
          <!-- LEFT -->
          <div class="flex flex-col md:flex-row md:items-center gap-2 w-full">
            <div class="flex w-full bg-base-200 p-2 items-center gap-2 border border-base-300">
              <font-awesome-icon icon="fa-solid fa-user" />

              <span class="break-all">
                {{ member.email }}
              </span>
            </div>

            <div class="badge badge-primary w-full md:w-fit">
              <p v-if="member.role == 'owner'">{{ $t('work.kanban.common.roles.owner') }}</p>
              <p v-if="member.role == 'admin'">{{ $t('work.kanban.common.roles.admin') }}</p>
              <p v-if="member.role == 'editor'">{{ $t('work.kanban.common.roles.editor') }}</p>
              <p v-if="member.role == 'viewer'">{{ $t('work.kanban.common.roles.viewer') }}</p>
            </div>
          </div>

          <!-- ACTIONS -->
          <div class="dropdown dropdown-end self-end md:self-auto">
            <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>

            <ul
              tabindex="0"
              class="dropdown-content menu bg-base-200 border border-base-300 w-40 p-2 shadow"
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
          v-if="!kanbanMembersStore.loading && kanbanMembersStore.members.length === 0"
          class="p-8 flex flex-col items-center justify-center gap-4 text-base-content/60"
        >
          <!-- Icon composition -->
          <div class="relative flex items-center justify-center">
            <font-awesome-icon icon="fa-solid fa-users" class="text-6xl text-base-content/20" />

            <font-awesome-icon
              icon="fa-solid fa-circle-exclamation"
              class="text-error text-xl absolute -top-1 -right-2"
              fade
            />
          </div>

          <!-- Text block -->
          <div class="text-center flex flex-col gap-1">
            <h3
              class="text-lg font-semibold text-base-content/80 flex items-center gap-2 justify-center"
            >
              <font-awesome-icon icon="fa-solid fa-user-slash" class="text-error" />
              {{ $t('work.kanban.errors.members_not_found') }}
            </h3>
          </div>

          <!-- Visual element -->
          <progress class="progress progress-primary w-32"></progress>
        </div>
      </div>

      <!-- FOOTER -->
      <div
        class="w-full md:w-3/5 flex flex-col md:flex-row bg-base-200 border border-base-300 px-3 py-3 items-center gap-3"
      >
        <!-- LIMIT -->
        <select
          class="select select-bordered w-full md:w-auto"
          v-model="kanbanMembersStore.meta.limit"
          @change="changeLimit($event.target.value)"
        >
          <option value="5">5</option>
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="30">30</option>
        </select>

        <!-- STATS -->
        <div class="flex flex-col md:flex-row gap-1 md:gap-4 text-sm text-center">
          <p>
            {{ $t('cabinet.admin.table_footer.total') }}
            <span class="font-semibold">
              {{ kanbanMembersStore.meta.totalItems }}
            </span>
          </p>

          <p>
            {{ $t('cabinet.admin.table_footer.page') }}

            <span class="font-semibold">
              {{ kanbanMembersStore.meta.page }}/{{ kanbanMembersStore.meta.totalPages }}
            </span>
          </p>
        </div>

        <!-- PAGINATION -->
        <div class="flex flex-col md:flex-row gap-2 md:ml-auto w-full md:w-auto justify-center">
          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="kanbanMembersStore.prevPage"
            :disabled="kanbanMembersStore.meta.page === 1"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
          </button>

          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="kanbanMembersStore.nextPage"
            :disabled="kanbanMembersStore.meta.page === kanbanMembersStore.meta.totalPages"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ADD MODAL -->
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

      <label class="label">
        {{ $t('work.kanban.modals.add_member.email') }}
      </label>
      <input
        type="email"
        class="input w-full"
        :placeholder="$t('work.kanban.modals.add_member.email_placeholder')"
        v-model="newMemberEmail"
      />
      <label class="label">{{ $t('work.kanban.modals.add_member.role') }}</label>
      <select class="select select-bordered w-full" v-model="newMemberRole">
        <option value="admin">{{ $t('work.kanban.common.roles.admin') }}</option>
        <option value="editor">{{ $t('work.kanban.common.roles.editor') }}</option>
        <option value="viewer">{{ $t('work.kanban.common.roles.viewer') }}</option>
      </select>
    </div>
  </base-dialog>

  <!-- UPDATE MODAL -->
  <base-dialog
    v-model="updateMemberModal"
    :title="$t('work.kanban.modals.update_member.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmUpdateMember"
    @cancel="closeUpdateMember"
  >
    <div class="w-full flex flex-col gap-2">
      <Transition name="error-slide">
        <div v-if="memberError">
          <h1 class="text-error mb-2">{{ memberError }}</h1>
        </div>
      </Transition>
      <label class="label">{{ $t('work.kanban.modals.update_member.role') }}</label>

      <select class="select select-bordered w-full" v-model="updatedRole">
        <option value="admin">{{ $t('work.kanban.common.roles.admin') }}</option>
        <option value="editor">{{ $t('work.kanban.common.roles.editor') }}</option>
        <option value="viewer">{{ $t('work.kanban.common.roles.viewer') }}</option>
      </select>
    </div>
  </base-dialog>

  <!-- DELETE MODAL -->
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

  <LoadingScreen v-if="kanbanMembersStore.loading" />
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useAdminStore } from '@/stores/admin'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'MembersSpace',
  components: { BaseDialog, LoadingScreen },

  data() {
    return {
      kanbanMembersStore: useKanbanMembersStore(),
      kanbanBoardStore: useKanbanBoardStore(),
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

  watch: {
    'kanbanBoardStore.selectedBoard': {
      handler: async function (newBoard) {
        if (newBoard) {
          this.kanbanMembersStore.boardId = newBoard.id
          this.kanbanMembersStore.meta.page = 1
          await this.kanbanMembersStore.fetchKanbanMembers()
        } else {
          this.kanbanMembersStore.members = []
        }
      },
      immediate: true,
    },
  },
  methods: {
    closeUpdateMember() {
      this.updateMemberModal = false
      this.kanbanMembersStore.clearError()
    },
    closeDeleteMemberModal() {
      this.deleteMemberModal = false
      this.kanbanMembersStore.clearError()
    },
    async searchMembers() {
      const store = this.kanbanMembersStore

      store.meta.page = 1

      if (store.searchType === 'all') return store.fetchKanbanMembers()

      if (store.searchType === 'email') return store.getMemberByEmail()

      if (store.searchType === 'role') return store.getMemberByRole()
    },

    async changeLimit(limit) {
      await this.kanbanMembersStore.setLimit(Number(limit))
    },

    async openUpdateMemberModal(member) {
      this.updateMemberModal = true
      this.selectedMember = member
    },

    async confirmUpdateMember() {
      try {
        const payload = {
          userId: String(this.selectedMember.userId),
          boardId: this.kanbanMembersStore.boardId,
          role: this.updatedRole,
        }

        await this.kanbanMembersStore.updateMember(payload)

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
        boardId: this.kanbanMembersStore.boardId,
      }

      try {
        await this.kanbanMembersStore.deleteMember(payload)
        this.deleteMemberModal = false
      } catch (err) {
        console.error('Failed to delete member:', err)
      }
    },

    async openAddMemberModal() {
      this.addMemberModal = true
    },

    closeAddMemberModal() {
      this.adminStore.clearError()
      this.addMemberModal = false
      this.newMemberEmail = ''
      this.newMemberRole = 'viewer'
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
          boardId: this.kanbanMembersStore.boardId,
          role: this.newMemberRole,
        }

        await this.kanbanMembersStore.addMember(payload)

        this.addMemberModal = false
      } catch (err) {
        console.error('Failed to add member:', err)
      }
    },
  },
  computed: {
    error() {
      return this.adminStore.error
    },
    memberError() {
      return this.kanbanMembersStore.error
    },
  },
}
</script>

<style scoped></style>
