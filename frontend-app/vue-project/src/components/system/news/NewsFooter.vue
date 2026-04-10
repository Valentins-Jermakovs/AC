<template>
  <!-- FOOTER -->
  <div
    class="w-full flex flex-col sm:flex-row gap-3 sm:items-center bg-base-100 border border-base-300 wrap-break-word p-3 sm:px-4 sm:py-2"
  >
    <!-- LIMIT -->
    <div>
      <select
        class="select select-bordered w-full sm:w-24"
        v-model="newsStore.meta.limit"
        @change="newsStore.setLimit(Number($event.target.value))"
      >
        <option :value="5">5</option>
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="30">30</option>
      </select>
    </div>

    <!-- META -->
    <div class="flex flex-col sm:flex-row gap-1 sm:gap-4 items-center md:items-start text-sm">
      <p>
        {{ $t('cabinet.admin.table_footer.total') }}
        <span class="font-semibold">
          {{ newsStore.meta.total_events }}
        </span>
      </p>

      <p>
        {{ $t('cabinet.admin.table_footer.page') }}
        <span class="font-semibold">
          {{ newsStore.meta.page }}/{{ newsStore.meta.total_pages }}
        </span>
      </p>
    </div>

    <!-- PAGINATION -->
    <div class="flex flex-col md:flex-row gap-2 sm:ml-auto">
      <button
        class="btn w-full md:w-auto btn-neutral"
        @click="newsStore.prevPage"
        :disabled="newsStore.meta.page === 0 || newsStore.meta.page === 1"
      >
        <font-awesome-icon icon="fa-solid fa-arrow-left" />
      </button>

      <button
        class="btn w-full md:w-auto btn-neutral"
        @click="newsStore.nextPage"
        :disabled="newsStore.meta.page === newsStore.meta.total_pages"
      >
        <font-awesome-icon icon="fa-solid fa-arrow-right" />
      </button>
    </div>
  </div>
</template>

<script>
import { useNewsStore } from '@/stores/news'

export default {
  data() {
    return {
      newsStore: useNewsStore(),
    }
  },
}
</script>

<style scoped></style>
