<template>
  <!-- Members space -->
  <div class="flex-1 flex flex-col w-full h-full overflow-auto p-5 gap-2">
    <div class="w-full h-full flex flex-col items-center gap-4 p-4">
      <div class="w-3/5 flex justify-between items-center gap-2">
        <button class="btn btn-success h-full" @click="openAddMemberModal">
          <font-awesome-icon icon="fa-solid fa-user-plus" />
          Add member
        </button>

        <div class="w-full flex items-center gap-2 border border-base-300 bg-base-200 p-1">
          <input type="text" class="input w-full" placeholder="Search..." v-model="searchQuery"
            @keyup.enter="searchMembers" />
          <!-- Filters -->
          <select class="select select-bordered bg-neutral text-neutral-content">
            <option>All</option>
            <option>By email</option>
            <option>By role</option>
          </select>
          <button class="btn btn-primary btn-square" @click="searchMembers">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>


      <!-- Members list -->
      <div class="w-3/5 bg-base-200 border border-base-300 flex flex-col gap-3 p-1">
        <div v-for="member in kanbanMembersStore.members" :key="member.id"
          class="w-full p-1 bg-base-100 border border-base-300 rounded-box flex items-center justify-between gap-3">
          <div class="flex items-center gap-3 font-medium flex-1 p-2">
            <div class="flex w-full bg-base-200 p-3 items-center gap-2 rounded-box border border-base-300">
              <font-awesome-icon icon="fa-solid fa-user" />
              Email: {{ member.email }}
            </div>
          </div>

          <div class="flex items-center gap-2 badge badge-primary rounded-box">
            {{ member.role }}
          </div>

          <div class="dropdown dropdown-right">
            <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
            <ul tabindex="0"
              class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow">
              <li>
                <button class="flex gap-2" @click="openUpdateMemberModal(member)">
                  <font-awesome-icon icon="fa-solid fa-pencil" />
                  Update
                </button>
              </li>
              <li>
                <button class="flex gap-2 text-error" @click="deleteMember(member)">
                  <font-awesome-icon icon="fa-solid fa-trash" />
                  Delete
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="!kanbanMembersStore.loading && kanbanMembersStore.members.length === 0"
          class="p-4 text-center text-base-content/60">
          No members found.
        </div>
      </div>

      <!-- Footer: limit & pagination -->
      <div class="w-3/5 flex bg-base-200 border border-base-300 px-4 py-2 items-center gap-4">
        <div class="flex-1">
          <select class="select select-bordered" v-model="kanbanMembersStore.meta.limit"
            @change="changeLimit($event.target.value)">
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
          </select>
        </div>

        <div class="flex gap-4 text-sm">
          <p>Total: <span class="font-semibold">{{ kanbanMembersStore.meta.totalItems }}</span></p>
          <p>Page: <span class="font-semibold">{{ kanbanMembersStore.meta.page }}/{{ kanbanMembersStore.meta.totalPages
              }}</span>
          </p>
        </div>

        <div class="flex gap-2 ml-auto">
          <button class="btn btn-sm btn-neutral" @click="kanbanMembersStore.prevPage"
            :disabled="kanbanMembersStore.meta.page === 1">
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
          </button>
          <button class="btn btn-sm btn-neutral" @click="kanbanMembersStore.nextPage"
            :disabled="kanbanMembersStore.meta.page === kanbanMembersStore.meta.totalPages">
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modals -->
  <!-- Add meber modal -->
  <base-dialog v-model="addMemberModal" title="Add Member" confirmText="Add" cancelText="Cancel"
    @confirm="confirmAddMember">
    <div class="w-full flex flex-col gap-5">
      <!-- Text input - member email -->
      <input type="email" class="input w-full" placeholder="Enter member email" v-model="newMemberEmail">
      <!-- Select input - member role -->
      <select class="select select-bordered w-full" v-model="newMemberRole">
        <option value="admin">Admin</option>
        <option value="editor">Editor</option>
        <option value="viewer">Viewer</option>
      </select>
    </div>
  </base-dialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers';
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useAdminStore } from '@/stores/admin';

export default {
  name: 'MembersSpace',
  components: { BaseDialog },

  data() {
    return {
      kanbanMembersStore: useKanbanMembersStore(),
      kanbanBoardStore: useKanbanBoardStore(),
      adminStore: useAdminStore(),
      searchQuery: '',
      addMemberModal: false,
      newMemberEmail: '',
      newMemberRole: 'viewer',
    };
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
    async searchMembers() {
      this.kanbanMembersStore.meta.page = 1
      await this.kanbanMembersStore.fetchKanbanMembers()
    },

    async changeLimit(limit) {
      await this.kanbanMembersStore.setLimit(Number(limit))
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
          boardId: this.kanbanMembersStore.boardId,
          role: this.newMemberRole
        }

        await this.kanbanMembersStore.addMember(payload)

        this.addMemberModal = false
        // take last request and repeat it
        this.kanbanMembersStore.fetchKanbanMembers()
      } catch (err) {
        console.error('Failed to add member:', err)
      }
    }
  },
};
</script>

<style scoped></style>
