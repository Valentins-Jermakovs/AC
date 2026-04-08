<template>
    <div class="w-full p-5 flex flex-col items-center gap-2" v-if="!newsStore.selectedNews">
        <NewsSearch></NewsSearch>
        <NewsTable></NewsTable>
        <button class="btn btn-primary">
            <font-awesome-icon icon="fa-solid fa-plus" />
            Add news
        </button>
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
import NewsSearch from './NewsSearch.vue';
import NewsTable from './NewsTable.vue';

import { useNewsStore } from '@/stores/news';

export default {
    name: 'NewsManagerPage',
    components: {
        NewsTable,
        NewsSearch
    },

    data() {
        return {
            newsStore: useNewsStore(),
        }
    }

}
</script>

<style scoped></style>