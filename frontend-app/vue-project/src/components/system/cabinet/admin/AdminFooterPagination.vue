<template>
  <div
    class="w-full p-4 rounded-box border border-base-300 bg-base-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
  >
    <!-- Left section: Limit selector, total users, current page info -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:gap-6 w-full sm:w-auto">
      
      <!-- Page size selector -->
      <div class="flex flex-col sm:flex-row sm:items-center gap-2">
        <label class="text-sm opacity-70">
          {{ $t('cabinet.admin.table_footer.limit') }}
        </label>
        <select
          :value="selectedPageSize"
          @change="onLimitChange"
          class="select select-bordered mt-1 sm:mt-0"
          :disabled="disableLimit"
        >
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </div>

      <!-- Total users count -->
      <div class="text-sm opacity-80 whitespace-nowrap">
        {{ $t('cabinet.admin.table_footer.total') }}
        <span class="font-semibold">{{ meta.total_users }}</span>
      </div>

      <!-- Current page info -->
      <div class="text-sm opacity-80 whitespace-nowrap">
        {{ $t('cabinet.admin.table_footer.page') }}
        <span class="font-semibold">{{ meta.page }}</span> /
        <span class="font-semibold">{{ meta.total_pages }}</span>
      </div>
    </div>

    <!-- Right section: Pagination buttons -->
    <div class="flex flex-col sm:flex-row sm:gap-3 gap-2 w-full sm:w-auto">
      <button
        class="btn btn-neutral hover:btn-primary flex-1 p-2"
        :disabled="meta.page === 1"
        @click="$emit('prevPage')"
      >
        <font-awesome-icon icon="fa-solid fa-arrow-left" />
      </button>
      <button
        class="btn btn-neutral hover:btn-primary flex-1 p-2"
        :disabled="meta.page === meta.total_pages"
        @click="$emit('nextPage')"
      >
        <font-awesome-icon icon="fa-solid fa-arrow-right" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminFooterPagination',

  props: {
    // Currently selected page size
    selectedPageSize: {
      type: Number,
      default: 10,
    },

    // Pagination metadata: total_users, page, total_pages
    meta: {
      type: Object,
      required: true,
    },

    // Disable page size selector if true
    disableLimit: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    // Emit new limit when user changes page size
    onLimitChange(e) {
      const newValue = Number(e.target.value)
      this.$emit('update:selectedPageSize', newValue)
      this.$emit('changeLimit') // notify parent to update data
    },
  },
}
</script>

<style scoped></style>
