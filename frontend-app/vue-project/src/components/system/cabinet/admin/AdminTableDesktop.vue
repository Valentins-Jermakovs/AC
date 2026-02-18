<template>
  <div class="hidden lg:block w-full overflow-x-auto p-4 bg-base-200 border-x border-base-300">
    <table class="table w-full min-w-175">
      <thead>
        <tr>
          <th>
            <!-- Select All Checkbox -->
            <input
              type="checkbox"
              class="checkbox checkbox-neutral"
              :checked="selectAllLocal"
              @change="toggleAll"
            />
          </th>
          <th>ID</th>
          <th>{{ $t('cabinet.admin.table_top.username') }}</th>
          <th>{{ $t('cabinet.admin.table_top.email') }}</th>
          <th>{{ $t('cabinet.admin.table_top.roles') }}</th>
          <th>{{ $t('cabinet.admin.table_top.created_at') }}</th>
          <th>{{ $t('cabinet.admin.table_top.status') }}</th>
        </tr>
      </thead>

      <!-- Loading state -->
      <tbody v-if="store.loading">
        <tr>
          <td colspan="7" class="text-center">
            <LoadingScreen />
          </td>
        </tr>
      </tbody>

      <!-- Empty state -->
      <tbody v-else-if="store.users.length === 0">
        <tr>
          <td colspan="7" class="text-center">
            <div class="alert alert-error">{{ $t('common.no_data') }}</div>
          </td>
        </tr>
      </tbody>

      <!-- Users list -->
      <tbody v-else>
        <tr
          v-for="user in store.users"
          :key="user.id"
          :class="{ 'bg-base-300': selectedUserIdsLocal.includes(user.id) }"
        >
          <td>
            <input
              type="checkbox"
              class="checkbox checkbox-neutral"
              :value="user.id"
              :checked="selectedUserIdsLocal.includes(user.id)"
              @change="toggleUser(user.id)"
            />
          </td>
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td class="truncate max-w-50" :title="user.email">{{ user.email }}</td>
          <td>
            <div class="flex gap-2 overflow-x-auto max-w-45">
              <span v-for="role in user.roles" :key="role" class="badge badge-info">{{ role }}</span>
            </div>
          </td>
          <td>{{ user.created_at }}</td>
          <td :class="user.active ? 'text-success' : 'text-error'">
            {{ user.active ? $t('cabinet.admin.table_body.status_active') : $t('cabinet.admin.table_body.status_inactive') }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useAdminStore } from '@/stores/admin'

export default {
  name: 'AdminTableDesktop',
  components: { LoadingScreen },

  props: {
    selectedUserIds: {
      type: Array,
      default: () => [],
    },
    selectAll: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      // Reference to the admin store
      store: useAdminStore(),
    }
  },

  computed: {
    // Local computed property for selected user IDs, synced with parent via v-model
    selectedUserIdsLocal: {
      get() {
        return this.selectedUserIds
      },
      set(val) {
        this.$emit('update:selectedUserIds', val)
      },
    },

    // Local computed property for "select all" checkbox
    selectAllLocal: {
      get() {
        return this.selectAll
      },
      set(val) {
        this.$emit('update:selectAll', val)
      },
    },
  },

  methods: {
    // Toggle selection of a single user
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

    // Toggle "select all" checkbox
    toggleAll() {
      if (this.selectAllLocal) {
        this.selectedUserIdsLocal = []
      } else {
        this.selectedUserIdsLocal = this.store.users.map(u => u.id)
      }
      this.selectAllLocal = !this.selectAllLocal
    },
  },
}
</script>

<style scoped></style>
