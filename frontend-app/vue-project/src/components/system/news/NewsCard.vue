<template>
  <div class="card bg-base-100 rounded-none border border-base-300">
    <figure class="h-40 overflow-hidden">
      <img
        v-if="news.coverImage && !imageError"
        :src="news.coverImage"
        @error="imageError = true"
        class="w-full h-full object-cover"
      />

      <div v-else class="flex flex-col items-center justify-center text-base-content/40">
        <font-awesome-icon icon="fa-solid fa-newspaper" class="text-4xl mb-2" bounce />
      </div>
    </figure>

    <div class="card-body rounded-none gap-3">
      <h2 class="card-title text-lg">
        {{ news.title }}
      </h2>

      <p class="text-sm text-base-content/70 line-clamp-3">
        {{ truncateContent(news.content, 150) }}
      </p>

      <button class="btn btn-primary" @click="selectNews">
        {{ $t('common.read_more') }}
      </button>
    </div>
  </div>
</template>

<script>
import { useNewsStore } from '@/stores/news'

export default {
  name: 'NewsCard',

  props: {
    news: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },

  data() {
    return {
      newsStore: useNewsStore(),
    }
  },

  methods: {
    selectNews() {
      this.newsStore.selectedNews = this.news
    },

    // Truncate content and strip HTML tags
    truncateContent(content, length = 150) {
      // No HTML tags
      const textOnly = content.replace(/<\/?[^>]+(>|$)/g, '')
      if (textOnly.length <= length) return textOnly
      return textOnly.substring(0, length) + '...'
    },
  },
}
</script>

<style scoped></style>
