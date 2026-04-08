<template>
  <div class="bg-base-200 border-base-300 border p-3 flex flex-1 w-full">
    <div class="flex flex-1 gap-3">
      <input
        class="input input-bordered bg-base-200 w-full"
        :placeholder="$t('common.search')"
        v-model="store.searchQuery"
        @keyup.enter="store.getAllNews()"
      />
    </div>
  </div>
</template>

<script>
import { useNewsStore } from '@/stores/news'

export default {
  name: 'NewsSearch',
  data() {
    return {
      store: useNewsStore(),
    }
  },
  mounted() {
    this.store.searchQuery = ''
  },
}
</script>

<style scoped></style>
