<template>
  <div class="w-full bg-base-100 border border-base-300 p-2 flex flex-col sm:flex-row items-center justify-between gap-3 sm:gap-5">
    <!-- LIMIT -->
    <select class="select select-bordered w-full sm:w-auto" v-model="store.meta.limit" @change="changeLimit">
      <option :value="5">5</option>
      <option :value="10">10</option>
      <option :value="20">20</option>
      <option :value="30">30</option>
    </select>

    <!-- META -->
    <div class="flex flex-col sm:flex-row gap-2 sm:gap-5 text-sm text-base-content/60">
      <p>Total projects: {{ store.meta.totalItems }}</p>
      <p>Page {{ store.meta.page }} / {{ store.meta.totalPages || 1 }}</p>
    </div>

    <!-- NAV -->
    <div class="flex flex-col md:flex-row gap-2 w-full md:w-auto">
      <button
        class="btn btn-neutral w-full md:w-auto"
        @click="prevPage"
        :disabled="store.meta.page <= 1 || store.loading"
      >
        <font-awesome-icon icon="fa-solid fa-arrow-left" />
      </button>

      <button
        class="btn btn-neutral w-full md:w-auto"
        @click="nextPage"
        :disabled="store.meta.page >= store.meta.totalPages || store.loading"
      >
        <font-awesome-icon icon="fa-solid fa-arrow-right" />
      </button>
    </div>
  </div>
</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects'

export default {
  name: 'ProjectsPagination',

  data() {
    return {
      store: useWorkspaceProjectsStore(),
    }
  },

  methods: {
    async changeLimit() {
      await this.store.setLimit(Number(this.store.meta.limit))
    },

    async nextPage() {
      await this.store.nextPage()
    },

    async prevPage() {
      await this.store.prevPage()
    },
  },
}
</script>
