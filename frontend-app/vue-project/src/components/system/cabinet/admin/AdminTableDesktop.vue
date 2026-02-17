<template>
  <div class="hidden lg:block w-full overflow-x-auto p-4 bg-base-200 border-x border-base-300">
    <table class="table w-full min-w-175">
      <thead>
        <tr>
          <th>
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
import { computed } from 'vue'

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
  setup(props, { emit }) {
    const store = useAdminStore()

    // Lokālie getter/setter props
    const selectedUserIdsLocal = computed({
      get: () => props.selectedUserIds,
      set: (val) => emit('update:selectedUserIds', val),
    })

    const selectAllLocal = computed({
      get: () => props.selectAll,
      set: (val) => emit('update:selectAll', val),
    })

    // Toggle single checkbox
    const toggleUser = (userId) => {
      const newSelected = [...selectedUserIdsLocal.value]
      const index = newSelected.indexOf(userId)
      if (index === -1) {
        newSelected.push(userId)
      } else {
        newSelected.splice(index, 1)
      }
      selectedUserIdsLocal.value = newSelected
    }

    // Toggle "select all"
    const toggleAll = () => {
      if (selectAllLocal.value) {
        selectedUserIdsLocal.value = []
      } else {
        selectedUserIdsLocal.value = store.users.map(u => u.id)
      }
      selectAllLocal.value = !selectAllLocal.value
    }

    return { store, selectedUserIdsLocal, selectAllLocal, toggleUser, toggleAll }
  },
}
</script>

<style scoped></style>
