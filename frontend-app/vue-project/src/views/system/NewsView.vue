<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>
  <NewsPage v-if="activePage === 'news'"></NewsPage>
  <NewsManagerPage v-if="activePage === 'newsManager' && userStore.isManager"></NewsManagerPage>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue'
import headerImage from '@/assets/images/anna-keibalo-oc5Brib1dNY-unsplash.jpg'

import { useNewsStore } from '@/stores/news'
import { useUserStore } from '@/stores/user'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'
import NewsPage from '@/components/system/news/NewsPage.vue'
import NewsManagerPage from '@/components/system/news/NewsManagerPage.vue'

export default {
  name: 'NewsView',
  components: {
    PageHeader,
    NavigationPanel,
    NewsPage,
    NewsManagerPage,
  },
  data() {
    return {
      image: headerImage,
      activePage: 'news',
    }
  },
  async mounted() {
    await this.userStore.fetchMe()
    this.newsStore.getAllNews()
  },
  computed: {
    newsStore() {
      return useNewsStore()
    },

    userStore() {
      return useUserStore()
    },

    title() {
      return this.$t('news.title')
    },

    navButtons() {
      let navButtons = [
        {
          key: 'news',
          title: this.$t('news.titles.news'),
        },
      ]

      if (this.userStore.isManager) {
        navButtons.push({
          key: 'newsManager',
          title: this.$t('news.titles.news_manager'),
        })
      }

      return navButtons
    },
  },
}
</script>

<style scoped></style>
