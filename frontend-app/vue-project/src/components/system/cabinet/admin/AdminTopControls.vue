<template>
  <div class="flex flex-col xl:flex-row w-full bg-base-100 border border-base-300">
    <!-- Search input + button -->
    <div class="flex flex-col lg:flex-row flex-1">
      <div class="flex flex-col sm:flex-row flex-1 p-4 gap-3 items-stretch sm:items-center">
        <input
          type="text"
          v-model="store.searchQuery"
          :placeholder="$t('common.search')"
          class="input input-bordered w-full"
          :disabled="store.searchMode === '' || store.searchMode === 'all'"
        />
        <button class="btn btn-primary" @click="$emit('search')">
          {{ $t('common.make_query') }}
        </button>
      </div>

      <!-- Filter dropdown -->
      <div class="flex p-4 items-center">
        <select
          v-model="store.searchMode"
          class="select select-bordered w-full lg:w-64"
          @change="$emit('clear-error')"
        >
          <option value="all">{{ $t('cabinet.admin.admin_top.filters[0]') }}</option>
          <option value="id">{{ $t('cabinet.admin.admin_top.filters[1]') }}</option>
          <option value="username">{{ $t('cabinet.admin.admin_top.filters[2]') }}</option>
          <option value="role">{{ $t('cabinet.admin.admin_top.filters[3]') }}</option>
        </select>
      </div>
    </div>

    <!-- Control buttons -->
    <div class="flex flex-col sm:flex-row flex-wrap gap-3 p-4 justify-center">
      <button
        class="btn btn-neutral hover:btn-primary w-full sm:w-auto"
        :class="{ 'btn-disabled': !selectedUserIds.length }"
        @click="$emit('add-role')"
      >
        {{ $t('common.add_role') }}
      </button>

      <button
        class="btn btn-neutral hover:btn-primary w-full sm:w-auto"
        :class="{ 'btn-disabled': !selectedUserIds.length }"
        @click="$emit('remove-role')"
      >
        {{ $t('common.remove_role') }}
      </button>

      <button
        class="btn btn-neutral hover:btn-primary w-full sm:w-auto"
        :class="{ 'btn-disabled': !selectedUserIds.length }"
        @click="$emit('change-activity')"
      >
        {{ $t('common.change_activity') }}
      </button>
    </div>
  </div>
</template>

<script>
import { useAdminStore } from '@/stores/admin'

export default {
  name: 'AdminTopControls',
  props: {
    selectedUserIds: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['add-role', 'remove-role', 'change-activity', 'search', 'clear-error', 'update:selectedUserIds'],
  setup() {
    const store = useAdminStore()
    return { store }
  },
}
</script>

<style scoped></style>
