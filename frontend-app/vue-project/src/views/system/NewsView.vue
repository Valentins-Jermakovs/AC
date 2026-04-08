<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>
  <NewsPage v-if="activePage === 'news'"></NewsPage>
  <NewsManagerPage v-if="activePage === 'newsManager'"></NewsManagerPage>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue';
import headerImage from '@/assets/images/anna-keibalo-oc5Brib1dNY-unsplash.jpg'

import { useNewsStore } from '@/stores/news';
import NavigationPanel from '@/components/ui/NavigationPanel.vue';
import NewsPage from '@/components/system/news/NewsPage.vue';
import NewsManagerPage from '@/components/system/news/NewsManagerPage.vue';

export default {
  name: 'NewsView',
  components: {
    PageHeader,
    NavigationPanel,
    NewsPage,
    NewsManagerPage
  },
  data() {
    return {
      image: headerImage,

      newsStore: useNewsStore(),

      activePage: 'news',
    };
  },
  mounted() {
    this.newsStore.getAllNews();
  },
  computed: {
    title() {
      return this.$t('news.title');
    },
    navButtons() {
      // Basic navigation buttons
      let navButtons = [
        {
          key: 'news',
          title: this.$t('news.titles.news'),
        },
        {
          key: 'newsManager',
          title: this.$t('news.titles.news_manager'),
        },
      ]

      return navButtons
    },
  },
};
</script>

<style scoped></style>
