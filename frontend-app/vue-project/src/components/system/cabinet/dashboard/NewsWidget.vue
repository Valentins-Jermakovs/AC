<template>
  <div v-if="news" class="group bg-base-200 border border-base-300">
    <!-- Image -->
    <div class="relative h-48 overflow-hidden">
      <img
        v-if="news.coverImage && !imageError"
        :src="news.coverImage"
        @error="imageError = true"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      />

      <!-- fallback -->
      <div
        v-else
        class="w-full h-full flex items-center justify-center bg-base-200 text-base-content/30"
      >
        <font-awesome-icon icon="fa-solid fa-newspaper" class="text-5xl" />
      </div>

      <!-- date -->
      <div class="absolute bottom-3 left-3 text-white text-xs">
        {{ formatDate(news.publishedAt) }}
      </div>
    </div>

    <!-- Content -->
    <div class="p-5 flex flex-col gap-3">
      <!-- tags -->
      <div class="flex gap-2 flex-wrap">
        <span
          v-for="tag in news.tags"
          :key="tag"
          class="text-xs px-2 py-1 bg-primary/10 text-primary"
        >
          {{ tag }}
        </span>
      </div>

      <!-- title -->
      <h2 class="text-xl font-semibold">
        {{ news.title }}
      </h2>

      <!-- preview -->
      <p class="text-sm text-base-content/70 line-clamp-3 leading-relaxed">
        {{ previewText }}
      </p>

      <!-- footer -->
      <div class="flex items-center pt-2">
        <div class="flex-1"></div>

        <router-link :to="{ name: 'news' }" class="font-medium btn btn-info">
          <font-awesome-icon icon="fa-solid fa-newspaper" class="mr-2" />
          {{ $t('common.read_more') }}
        </router-link>
      </div>
    </div>
  </div>

  <LoadingScreen v-if="newsStore.loading" />
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useNewsStore } from '@/stores/news'

export default {
  name: 'NewsWidget',
  components: { LoadingScreen },
  data() {
    return {
      newsStore: useNewsStore(),
      news: null,
      imageError: false,
    }
  },

  async mounted() {
    await this.newsStore.getAllNews()
    if (this.newsStore.news.length > 0) {
      this.news = this.newsStore.news[0]
    }
  },
  methods: {
    truncateContent(html, limit) {
      if (!html) return ''

      // izņem HTML tagus
      const text = html.replace(/<[^>]*>/g, '')

      if (text.length <= limit) return text

      return text.slice(0, limit) + '...'
    },
    formatDate(date) {
      if (!date) return ''

      return new Date(date).toLocaleDateString({
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    },
  },
  computed: {
    previewText() {
      if (!this.news?.content) return ''

      const div = document.createElement('div')
      div.innerHTML = this.news.content

      const text = div.textContent || ''

      return text.length > 160 ? text.slice(0, 160) + '...' : text
    },
  },
}
</script>

<style></style>
