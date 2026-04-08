<template>
  <div class="w-full p-5 flex flex-col gap-4">
    <!-- Show search + table when no selected news -->
    <div v-if="!newsStore.selectedNews">
      <NewsSearch />
      <NewsTable :news="newsStore.news" />
      <button class="btn btn-primary mt-2" @click="createNews">
        <font-awesome-icon icon="fa-solid fa-plus" />
        Add news
      </button>
    </div>

    <!-- Show editor when selectedNews is set -->
    <div v-else>
      <NewsEditor />
    </div>
  </div>
</template>

<script>
import NewsEditor from './NewsEditor.vue'
import NewsSearch from './NewsSearch.vue'
import NewsTable from './NewsTable.vue'
import { useNewsStore } from '@/stores/news'

export default {
  name: 'NewsManagerPage',
  components: {
    NewsEditor,
    NewsSearch,
    NewsTable,
  },
  setup() {
    const newsStore = useNewsStore()

    // Function to create a new news item
    const createNews = () => {
      newsStore.selectedNews = {
        id: null,
        title: '',
        coverImage: '',
        tags: [],
        status: 'draft',
        content: '',
      }
    }

    return { newsStore, createNews }
  },
}
</script>

<style scoped></style>
