<template>
    <div class="flex w-full items-center bg-base-100 p-3 border border-base-300 rounded-box gap-2">
        <input type="text" v-model="query" class="flex-1 input bg-base-100 text-lg" placeholder="Meklēt...">
        <select v-model="filter" class="select select-bordered w-auto bg-neutral text-neutral-content">
            <option disabled value="">Filter</option>
            <option value="all">All</option>
            <option value="title">By title</option>
            <option value="description">By description</option>
            <option value="duedate">By duedate</option>
            <option value="monthyear">By month and year</option>
        </select>
        <button class="btn btn-primary" @click="emitSearch">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
        </button>
    </div>
</template>

<script>
export default {
    name: 'SearchBar',
    data() {
        return {
            query: '',
            filter: ''
        };
    },
    methods: {
        emitSearch() {
            this.$emit('search', { query: this.query, filter: this.filter });
        }
    }
};
</script>