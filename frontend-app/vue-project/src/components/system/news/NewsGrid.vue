<template>
  <div class="flex-1 bg-base-200 border border-base-300 p-5">
    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center gap-4 py-20">
      <span class="loading loading-bars loading-lg text-primary"></span>

      <p class="text-base-content/60">
        {{ $t('common.loading') }}
      </p>
    </div>

    <!-- Empty -->
    <div
      v-else-if="!news.length"
      class="flex flex-col items-center justify-center gap-4 py-20 text-base-content/50"
    >
      <font-awesome-icon icon="fa-solid fa-newspaper" class="text-5xl opacity-40 animate-pulse" />
      {{ $t('errors.news_not_found') }}
      <span class="loading loading-bars loading-lg text-primary"></span>
    </div>

    <!-- List -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 mb-2">
      <NewsCard v-for="item in news" :key="item.id" :news="item" />
    </div>
    <NewsFooter></NewsFooter>
  </div>
  <LoadingScreen v-if="newsStore.loading"></LoadingScreen>
</template>

<script>
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import NewsCard from './NewsCard.vue'

import { useNewsStore } from '@/stores/news'
import NewsFooter from './NewsFooter.vue';

export default {
  name: 'NewsList',

  components: {
    NewsCard,
    LoadingScreen,
    NewsFooter
  },

  data() {
    return {
      newsStore: useNewsStore(),
    }
  },

  props: {
    news: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
}
</script>
