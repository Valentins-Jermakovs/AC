<template>
  <div class="flex w-full items-center bg-base-100 p-3 border border-base-300  gap-2">
    <!-- Search input -->
    <input
      type="text"
      v-model="query"
      class="flex-1 input bg-base-100 text-lg"
      :placeholder="$t('common.search')"
      :disabled="filter === 'all'"
    />

    <!-- Filter select -->
    <select v-model="filter" class="select select-bordered w-auto bg-neutral text-neutral-content">
      <option value="all">{{ $t('filters.all') }}</option>
      <option value="title">{{ $t('filters.by_title') }}</option>
      <option value="description">{{ $t('filters.by_description') }}</option>
      <option value="duedate">{{ $t('filters.by_due_date') }}</option>
      <option value="monthyear">{{ $t('filters.by_month') }}</option>
    </select>

    <!-- Search button -->
    <button
      class="btn btn-primary"
      @click="emitSearch"
      :disabled="filter !== 'all' && query.trim() === ''"
    >
      <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
    </button>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      query: '',
      filter: 'all', // noklusējuma vērtība
    }
  },
  watch: {
    // Katru reizi, kad mainās filter, attīra query
    filter(newFilter, oldFilter) {
      this.query = ''
    },
  },
  methods: {
    emitSearch() {
      this.$emit('search', { query: this.query, filter: this.filter })
    },
  },
}
</script>
