<template>
    <div class=" h-full bg-base-100 p-1 flex">
        <!-- Left screen: task list with search bar, filter button, search button -->
        <!-- and drop down menu and buttons for pagination -->
        <div class="w-1/2 bg-base-200 border border-base-300 flex flex-col gap-1 p-1">
            <SearchBar @search="handleSearch"></SearchBar>
            <TaskList :tasks="privateTasksStore.privateTasks" @select-task="selectTask"></TaskList>

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
                        <span class="font-semibold">{{ page }}</span> / <span class="font-semibold">{{
                            totalPages }}</span>
                    </div>
                </div>
                <!-- Pagination buttons -->
                <div class="flex flex-col sm:flex-row sm:gap-3 gap-2 w-full sm:w-auto">
                    <button class="btn btn-neutral hover:btn-primary flex-1 p-2" @click="prevPage"
                        :disabled="page <= 1">
                        <font-awesome-icon icon="fa-solid fa-arrow-left" />
                    </button>
                    <button class="btn btn-neutral hover:btn-primary flex-1 p-2" @click="nextPage"
                        :disabled="page >= totalPages || totalPages === 0">
                        <font-awesome-icon icon="fa-solid fa-arrow-right" />
                    </button>
                </div>
            </div>
        </div>

        <!-- Right screen: task details -->
        <div class="w-1/2 bg-base-200 border border-base-300 flex flex-col gap-1 p-1">
            <TaskDetails v-if="selectedTask" :task="selectedTask" />

            <div v-else class="flex items-center justify-center h-full text-base-content/50">
                Select a task
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
            selectedTask: null
        };
    },
    mounted() {
        this.privateTasksStore.fetchPrivateTasks();
    },

    computed: {
        page() {
            return this.privateTasksStore.meta.page;
        },

        limit: {
            get() {
                return this.privateTasksStore.meta.limit;
            },
            set(value) {
                this.privateTasksStore.setLimit(value);
            }
        },

        total() {
            return this.privateTasksStore.meta.totalItems;
        },

        totalPages() {
            return this.privateTasksStore.meta.totalPages;
        },
    },

    methods: {
        nextPage() {
            this.privateTasksStore.nextPage();
        },

        prevPage() {
            this.privateTasksStore.prevPage();
        },
        async handleSearch({ query, filter }) {

            this.privateTasksStore.searchQuery = query
            this.privateTasksStore.meta.page = 1

            switch (filter) {

                case 'all':
                    await this.privateTasksStore.fetchPrivateTasks()
                    break

                case 'title':
                    await this.privateTasksStore.findPrivateTasksByTitle()
                    break

                case 'description':
                    await this.privateTasksStore.findPrivateTasksByDescription()
                    break

                case 'duedate':
                    await this.privateTasksStore.findPrivateTasksByDueDate()
                    break

                case 'monthyear':
                    await this.privateTasksStore.findPrivateTasksByMonth()
                    break

                default:
                    await this.privateTasksStore.fetchPrivateTasks()
            }
        },
        selectTask(task) {
            this.selectedTask = task
        },

    },
};

</script>

<style scoped></style>