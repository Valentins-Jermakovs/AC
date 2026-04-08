<template>
  <div class="w-full lg:p-5 flex flex-col gap-4">
    <!-- Show search + grid when no selected news -->
    <div v-if="!newsStore.selectedNews">
      <NewsSearch />
      <NewsGrid :news="publishedNews" />
    </div>

    <!-- Show selected news -->
    <div v-else class="p-4 border border-base-300 bg-base-200 w-full">
      <!-- Title -->
      <h1 class="text-3xl font-bold mb-2">{{ newsStore.selectedNews.title }}</h1>

      <!-- Tags -->
      <div class="flex flex-wrap gap-2 mb-4">
        <span
          v-for="(tag, idx) in newsStore.selectedNews.tags"
          :key="idx"
          class="badge badge-info font-medium px-2 py-1"
        >
          {{ tag }}
        </span>
      </div>

      <!-- Cover Image -->
      <img
        v-if="newsStore.selectedNews.coverImage"
        :src="newsStore.selectedNews.coverImage"
        class="w-full h-64 object-cover mb-4"
      />

      <!-- Content -->
      <div
        v-html="newsStore.selectedNews.content"
        class="prose prose-base prose-a:text-blue-600 hover:prose-a:underline"
      ></div>

      <!-- Back Button -->
      <button class="btn btn-secondary mt-4" @click="newsStore.selectedNews = null">
        {{ $t('common.back') }}
      </button>
    </div>
  </div>
  <LoadingScreen v-if="newsStore.loading"></LoadingScreen>
</template>

<script>
import NewsSearch from './NewsSearch.vue'
import NewsGrid from './NewsGrid.vue'
import { useNewsStore } from '@/stores/news'
import LoadingScreen from '@/components/common/LoadingScreen.vue';

export default {
  name: 'NewsManagerPage',
  components: { NewsSearch, NewsGrid, LoadingScreen },
  data() {
    return {
      newsStore: useNewsStore(),
    }
  },
  computed: {
    // Filtrē tikai publicētās ziņas
    publishedNews() {
      return this.newsStore.news.filter((news) => news.status === 'published')
    },
  },
}
</script>

<style>
/* Tailwind Prose stili */
.prose h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}
.prose h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}
.prose h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.prose p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.prose ul {
  list-style: disc;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
.prose ol {
  list-style: decimal;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
.prose li {
  margin-bottom: 0.5rem;
}

.prose a {
  color: #2563eb;
  text-decoration: underline;
}
.prose a:hover {
  color: #1e40af;
}
</style>
