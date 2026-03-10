<template>
    <div class=" h-full bg-base-100 p-1 flex">
        <!-- Left screen: task list with search bar, filter button, search button -->
        <!-- and drop down menu and buttons for pagination -->
        <div class="w-1/2 bg-base-200 border border-base-300 flex flex-col gap-1 p-1">
            <SearchBar></SearchBar>
            <TaskList></TaskList>

            <!-- Pagination -->
            <div
                class="w-full p-4 rounded-box border border-base-300 bg-base-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <!-- Left section: Limit, total, page -->
                <div class="flex flex-col sm:flex-row sm:items-center sm:gap-6 w-full sm:w-auto">
                    <div class="flex flex-col sm:flex-row sm:items-center gap-2">
                        <label class="text-sm opacity-70">limit</label>
                        <select class="select select-bordered mt-1 sm:mt-0" v-model="limit">
                            <option :value="5">5</option>
                            <option :value="10">10</option>
                            <option :value="20">20</option>
                            <option :value="50">50</option>
                        </select>
                    </div>
                    <div class="text-sm opacity-80 whitespace-nowrap">Total:
                        <span class="font-semibold">
                            {{ total }}
                        </span>
                    </div>
                    <div class="text-sm opacity-80 whitespace-nowrap">Page Current:
                        <span class="font-semibold">{{ page }}</span> / <span class="font-semibold">{{ totalPages
                            }}</span>
                    </div>
                </div>
                <!-- Pagination buttons -->
                <div class="flex flex-col sm:flex-row sm:gap-3 gap-2 w-full sm:w-auto">
                    <button class="btn btn-neutral hover:btn-primary flex-1 p-2" 
                    @click="prevPage"><font-awesome-icon
                    icon=" fa-solid fa-arrow-left" /></button>
                    <button class="btn btn-neutral hover:btn-primary flex-1 p-2" 
                    @click="nextPage"><font-awesome-icon
                    icon="fa-solid fa-arrow-right" /></button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// Import UI components
import SearchBar from './tasks/SearchBar.vue';
import TaskList from './tasks/TaskList.vue';
import TaskDetails from './tasks/TaskDetails.vue';

// Import store
import { usePrivateTasksStore } from '@/stores/privateTasks';

export default {
    name: 'PrivateTasksPage',
    components: {
        SearchBar,
        TaskList,
        TaskDetails
    },
    data() {
        const privateTasksStore = usePrivateTasksStore();
        return {
            privateTasksStore,
        };
    },
    mounted() {
        this.privateTasksStore.fetchPrivateTasks();
    },
};

</script>

<style scoped></style>