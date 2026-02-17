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
import { ref, watch, onMounted } from 'vue'
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
  setup() {
    const adminStore = useAdminStore()

    // Modāli logi
    const addRoleModal = ref(false)
    const removeRoleModal = ref(false)
    const changeActivityModal = ref(false)

    // Izvēlētie dati
    const selectedAddRole = ref(5)
    const selectedRemoveRole = ref(5)
    const selectedActivityStatus = ref('active')
    const selectedUserIds = ref([])
    const selectAll = ref(false)

    // Error messages
    const emptyError = ref('')

    // Methods
    const clearEmptyError = () => (emptyError.value = '')

    const setNewLimit = async () => {
      await adminStore.setLimit(adminStore.meta.limit)
      await adminStore.refresh()
    }

    const onChangeLimit = (limit) => {
      adminStore.meta.limit = limit
    }

    const searchButton = async () => {
      const query = adminStore.searchQuery.toLowerCase()
      if (adminStore.searchMode === 'all') {
        adminStore.fetchUsers()
        adminStore.clearSearch()
      } else if (adminStore.searchMode === 'id') {
        if (!query) return (emptyError.value = 'Tukšs ievades lauks!')
        const numericId = Number(query)
        if (!Number.isInteger(numericId)) return (emptyError.value = 'Invalid ID format')
        await adminStore.getUserById(numericId)
        emptyError.value = ''
      } else if (adminStore.searchMode === 'username') {
        if (!query) return (emptyError.value = 'Tukšs ievades lauks!')
        await adminStore.getUserByNameEmail(query)
        emptyError.value = ''
      } else if (adminStore.searchMode === 'role') {
        if (!query) return (emptyError.value = 'Tukšs ievades lauks!')
        await adminStore.getUserByRole(query)
        emptyError.value = ''
      }
    }

    const addRole = async () => {
      await adminStore.addRoleToSelectedUsers(selectedAddRole.value, selectedUserIds.value)
      addRoleModal.value = false
      adminStore.error = ''
      selectedAddRole.value = 5
      await adminStore.refresh()
    }

    const removeRole = async () => {
      await adminStore.removeRoleFromSelectedUsers(selectedRemoveRole.value, selectedUserIds.value)
      removeRoleModal.value = false
      adminStore.error = ''
      selectedRemoveRole.value = 5
      await adminStore.refresh()
    }

    const changeActivity = async () => {
      await adminStore.updateUserActivity(selectedUserIds.value, selectedActivityStatus.value)
      changeActivityModal.value = false
      adminStore.error = ''
      selectedActivityStatus.value = 'active'
      await adminStore.refresh()
    }

    watch(selectedUserIds, (val) => {
      selectAll.value = val.length === adminStore.users.length
    })

    watch(() => adminStore.users, () => {
      selectedUserIds.value = []
      selectAll.value = false
    })

    onMounted(() => {
      adminStore.fetchUsers()
    })

    return {
      adminStore,
      addRoleModal,
      removeRoleModal,
      changeActivityModal,
      selectedAddRole,
      selectedRemoveRole,
      selectedActivityStatus,
      selectedUserIds,
      selectAll,
      emptyError,
      clearEmptyError,
      setNewLimit,
      searchButton,
      addRole,
      removeRole,
      changeActivity,
      onChangeLimit,
    }
  },
}
</script>

<style scoped>
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
