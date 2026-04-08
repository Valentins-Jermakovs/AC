<template>
    <!-- Ja selectedNews nav izvēlēts, rādi ziņu grid -->
    <div v-if="!newsStore.selectedNews">
        <NewsSearch></NewsSearch>
        <NewsGrid :news="newsStore.news"></NewsGrid>
    </div>

    <div v-else class="p-4 border border-base-300 bg-base-200">
        <h1 class="text-2xl font-bold mb-3">{{ newsStore.selectedNews.title }}</h1>

        <img v-if="newsStore.selectedNews.coverImage" :src="newsStore.selectedNews.coverImage"
            class="w-full h-64 object-cover mb-3" />

        <!-- Šeit renderējam HTML saturu -->
        <div v-html="newsStore.selectedNews.content" class="text-base text-base-content/80 mb-3"></div>

        <button class="btn btn-secondary" @click="newsStore.selectedNews = null">
            Back to all news
        </button>
    </div>
</template>

<script>
import NewsGrid from './NewsGrid.vue';

import { useNewsStore } from '@/stores/news';
import NewsSearch from './NewsSearch.vue';

export default {
    name: 'NewsPage',
    components: {
        NewsGrid,
        NewsSearch
    },
    data() {
        return {
            newsStore: useNewsStore(),
        }
    },
    mounted() {
        this.newsStore.getAllNews();
    }
}
</script>

<style></style>