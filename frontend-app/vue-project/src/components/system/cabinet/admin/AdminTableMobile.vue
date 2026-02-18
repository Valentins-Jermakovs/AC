<template>
  <div class="lg:hidden p-4 space-y-4">
    <!-- Users list -->
    <div v-if="!adminStore.loading">
      <div
        v-for="user in adminStore.users"
        :key="user.id"
        v-if="adminStore.users.length > 0"
        class="bg-base-200 border border-base-300 p-4 shadow-sm"
        :class="{ 'bg-base-300': selectedUserIdsLocal.includes(user.id) }"
      >
        <!-- Top row: username + email + checkbox -->
        <div class="flex justify-between items-start mb-3">
          <div>
            <div class="font-semibold text-lg">{{ user.username }}</div>
            <div class="text-sm opacity-70">{{ user.email }}</div>
          </div>
          <input
            type="checkbox"
            class="checkbox checkbox-neutral"
            :checked="selectedUserIdsLocal.includes(user.id)"
            @change="toggleUser(user.id)"
          />
        </div>

        <!-- Info grid -->
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <div class="opacity-60">ID</div>
            <div>{{ user.id }}</div>
          </div>

          <div>
            <div class="opacity-60">{{ $t('cabinet.admin.table_top.status') }}</div>
            <div :class="user.active ? 'text-success' : 'text-error'">
              {{ user.active ? $t('cabinet.admin.table_body.status_active') : $t('cabinet.admin.table_body.status_inactive') }}
            </div>
          </div>

          <div class="col-span-2">
            <div class="opacity-60 mb-1">{{ $t('cabinet.admin.table_top.roles') }}</div>
            <div class="flex flex-wrap gap-2">
              <span v-for="role in user.roles" :key="role" class="badge badge-info">
                {{ role }}
              </span>
            </div>
          </div>

          <div class="col-span-2">
            <div class="opacity-60">{{ $t('cabinet.admin.table_top.created_at') }}</div>
            <div>{{ user.created_at }}</div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else>
        <div class="p-4">
          <div class="alert alert-error flex flex-col items-center justify-center gap-2 p-2 text-center">
            <div class="flex gap-2 items-center justify-center text-2xl">
              <font-awesome-icon icon="fa-solid fa-info-circle" />
              <span>{{ $t('common.no_data') }}</span>
            </div>
            <div>
              <p>{{ $t('common.try_later') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-else class="flex justify-center">
      <LoadingScreen />
    </div>
  </div>
</template>

<script>
import { useAdminStore } from '@/stores/admin'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

export default {
  name: 'AdminTableMobile',
  components: { LoadingScreen },

  props: {
    selectedUserIds: {
      type: Array,
      default: () => [],
    },
  },

  computed: {
    // admin store
    adminStore() {
      return useAdminStore()
    },

    // local copy of selectedUserIds for two-way binding
    selectedUserIdsLocal: {
      get() {
        return this.selectedUserIds
      },
      set(val) {
        this.$emit('update:selectedUserIds', val)
      },
    },
  },

  methods: {
    // Toggle selection of a user
    toggleUser(userId) {
      const newSelected = [...this.selectedUserIdsLocal]
      const index = newSelected.indexOf(userId)
      if (index === -1) {
        newSelected.push(userId)
      } else {
        newSelected.splice(index, 1)
      }
      this.selectedUserIdsLocal = newSelected
    },
  },
}
</script>

<style scoped></style>
