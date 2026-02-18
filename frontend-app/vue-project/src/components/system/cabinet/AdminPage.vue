<template>
  <AdminCards />

  <div class="px-4 sm:px-5 pb-5 flex flex-col w-full">
    <!-- Top Controls -->
    <AdminTopControls
      :selected-user-ids="selectedUserIds"
      @update:selected-user-ids="selectedUserIds = $event"
      @add-role="addRoleModal = true"
      @remove-role="removeRoleModal = true"
      @change-activity="changeActivityModal = true"
      @search="searchButton"
      @clear-error="clearEmptyError"
    />

    <!-- Error message -->
    <Transition name="error-slide">
      <div v-if="emptyError" class="w-full bg-base-100 p-5 border-x border-base-300 text-center text-error">
        {{ emptyError }}
      </div>
    </Transition>

    <!-- Tables -->
    <AdminTableDesktop
      :selected-user-ids="selectedUserIds"
      @update:selected-user-ids="selectedUserIds = $event"
      :select-all="selectAll"
      @update:select-all="selectAll = $event"
    />

    <AdminTableMobile
      :selected-user-ids="selectedUserIds"
      @update:selected-user-ids="selectedUserIds = $event"
    />

    <!-- Footer / Pagination -->
    <AdminFooterPagination
      :meta="adminStore.meta"
      :selected-page-size="adminStore.meta.limit"
      :disable-limit="adminStore.searchMode === 'id'"
      @update:selected-page-size="onChangeLimit"
      @change-limit="setNewLimit"
      @prev-page="adminStore.prevPage"
      @next-page="adminStore.nextPage"
    />

    <!-- Modals -->
    <AdminModals
      :add-role-modal="addRoleModal"
      :remove-role-modal="removeRoleModal"
      :change-activity-modal="changeActivityModal"
      :selected-add-role="selectedAddRole"
      :selected-remove-role="selectedRemoveRole"
      :selected-activity-status="selectedActivityStatus"
      @update:add-role-modal="addRoleModal = $event"
      @update:remove-role-modal="removeRoleModal = $event"
      @update:change-activity-modal="changeActivityModal = $event"
      @update:selected-add-role="selectedAddRole = $event"
      @update:selected-remove-role="selectedRemoveRole = $event"
      @update:selected-activity-status="selectedActivityStatus = $event"
      @add-role="addRole"
      @remove-role="removeRole"
      @change-activity="changeActivity"
    />
  </div>
</template>

<script>
import { useAdminStore } from '@/stores/admin'

import AdminCards from './admin/AdminCards.vue'
import AdminTopControls from './admin/AdminTopControls.vue'
import AdminTableDesktop from './admin/AdminTableDesktop.vue'
import AdminTableMobile from './admin/AdminTableMobile.vue'
import AdminFooterPagination from './admin/AdminFooterPagination.vue'
import AdminModals from './admin/AdminModals.vue'

export default {
  name: 'AdminPage',
  components: {
    AdminCards,
    AdminTopControls,
    AdminTableDesktop,
    AdminTableMobile,
    AdminFooterPagination,
    AdminModals,
  },

  data() {
    const adminStore = useAdminStore()

    return {
      adminStore,               // Pinia store

      // Modal states
      addRoleModal: false,
      removeRoleModal: false,
      changeActivityModal: false,

      // Selected options
      selectedAddRole: 5,
      selectedRemoveRole: 5,
      selectedActivityStatus: 'active',
      selectedUserIds: [],
      selectAll: false,

      // Error message
      emptyError: '',
    }
  },

  methods: {
    // Clear error
    clearEmptyError() {
      this.emptyError = ''
    },

    // Set new limit and refresh table
    async setNewLimit() {
      await this.adminStore.setLimit(this.adminStore.meta.limit)
      await this.adminStore.refresh()
    },

    // Update page size without refresh
    onChangeLimit(limit) {
      this.adminStore.meta.limit = limit
    },

    // Search users based on search mode
    async searchButton() {
      const query = this.adminStore.searchQuery.toLowerCase()

      if (this.adminStore.searchMode === 'all') {
        this.adminStore.fetchUsers()
        this.adminStore.clearSearch()
      } else if (this.adminStore.searchMode === 'id') {
        if (!query) return (this.emptyError = 'Tukšs ievades lauks!')
        const numericId = Number(query)
        if (!Number.isInteger(numericId)) return (this.emptyError = 'Invalid ID format')
        await this.adminStore.getUserById(numericId)
        this.emptyError = ''
      } else if (this.adminStore.searchMode === 'username') {
        if (!query) return (this.emptyError = 'Tukšs ievades lauks!')
        await this.adminStore.getUserByNameEmail(query)
        this.emptyError = ''
      } else if (this.adminStore.searchMode === 'role') {
        if (!query) return (this.emptyError = 'Tukšs ievades lauks!')
        await this.adminStore.getUserByRole(query)
        this.emptyError = ''
      }
    },

    // Add role to selected users
    async addRole() {
      await this.adminStore.addRoleToSelectedUsers(this.selectedAddRole, this.selectedUserIds)
      this.addRoleModal = false
      this.adminStore.error = ''
      this.selectedAddRole = 5
      await this.adminStore.refresh()
    },

    // Remove role from selected users
    async removeRole() {
      await this.adminStore.removeRoleFromSelectedUsers(this.selectedRemoveRole, this.selectedUserIds)
      this.removeRoleModal = false
      this.adminStore.error = ''
      this.selectedRemoveRole = 5
      await this.adminStore.refresh()
    },

    // Change activity status for selected users
    async changeActivity() {
      await this.adminStore.updateUserActivity(this.selectedUserIds, this.selectedActivityStatus)
      this.changeActivityModal = false
      this.adminStore.error = ''
      this.selectedActivityStatus = 'active'
      await this.adminStore.refresh()
    },
  },

  watch: {
    // Update "select all" checkbox based on selected users
    selectedUserIds(val) {
      this.selectAll = val.length === this.adminStore.users.length
    },

    // Reset selections when users list changes
    'adminStore.users'() {
      this.selectedUserIds = []
      this.selectAll = false
    },
  },

  mounted() {
    this.adminStore.fetchUsers()
  },
}
</script>

<style scoped>
/* Error message slide animation */
.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 100px;
}
</style>
