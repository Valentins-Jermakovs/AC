<template>
    <div class="w-full p-5 flex flex-col items-center">
        <NewsSearch></NewsSearch>
        <NewsTable></NewsTable>
    </div>
</template>

<script>
import NewsSearch from './NewsSearch.vue';
import NewsTable from './NewsTable.vue';

export default {
    name: 'NewsManagerPage',
    components: {
        NewsTable,
        NewsSearch
    }
}
</script>

<style scoped></style>