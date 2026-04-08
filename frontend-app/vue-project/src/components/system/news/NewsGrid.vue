<template>
  <div class="flex-1 bg-base-200 border border-base-300 p-5">
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <NewsCard v-for="item in news" :key="item.id" :news="item" />
    </div>
  </div>
</template>

<script>
import NewsCard from './NewsCard.vue'

export default {
  name: 'NewsList',

  components: {
    NewsCard,
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
