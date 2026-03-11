// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from './auth'


// Create task store
export const usePrivateTasksStore = defineStore('privateTasks', {

    // ==========================
    // STATE
    // ==========================
    state: () => ({
        privateTasks: [],

        // Pagination metadata
        meta: {
            page: 1,
            limit: 10,
            totalItems: 0,
            totalPages: 0,
        },

        loading: false, // Indicates request is in progress
        error: null,    // Stores error message

        // Search configuration
        searchMode: 'all',
        searchQuery: '',

        // Stores information about last request (used for refresh)
        lastRequest: null,
    }),


    // ==========================
    // GETTERS
    // ==========================
    getters: {
        hasPrivateTasks() {
            return this.privateTasks.length > 0
        },
    },

    // ==========================
    // ACTIONS
    // ==========================
    actions: {

        // ==========================
        // GET
        // ==========================

        // Get all tasks paginated
        async fetchPrivateTasks() {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_ALL_PRIVATE_TASKS, {
                    params: {
                        page: this.meta.page,
                        limit: this.meta.limit
                    },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                // Save tasks and pagination data
                this.privateTasks = response.data.items
                this.meta = response.data.meta

                // Remember request type
                this.lastRequest = { type: 'all' }
                this.searchQuery = ''
            } catch (err) {
                this.error = err.response?.data?.message || err.message || 'Something went wrong';

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    totalItems: 0,
                    totalPages: 0,
                }
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by title
        async findPrivateTasksByTitle(
        ) {
            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_TITLE,
                    {
                        params: {
                            page: this.meta.page,
                            limit: this.meta.limit,
                            title: this.searchQuery,
                        },
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    }
                )

                // Save tasks and pagination data
                this.privateTasks = response.data.items
                this.meta = response.data.meta

                // Remember request type
                this.lastRequest = { type: 'title' }
            }
            catch (err) {
                this.error = err.response?.data?.message || err.message || 'Something went wrong';

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    totalItems: 0,
                    totalPages: 0,
                }
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by description
        async findPrivateTasksByDescription(
        ) {
            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_DESCRIPTION,
                    {
                        params: {
                            page: this.meta.page,
                            limit: this.meta.limit,
                            description: this.searchQuery,
                        },
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    }
                )

                // Save tasks and pagination data
                this.privateTasks = response.data.items
                this.meta = response.data.meta

                // Remember request type
                this.lastRequest = { type: 'description' }
            }
            catch (err) {
                this.error = err.response?.data?.message || err.message || 'Something went wrong';

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    totalItems: 0,
                    totalPages: 0,
                }
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by duedate
        async findPrivateTasksByDueDate(
        ) {

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_DUE_DATE,
                    {
                        params: {
                            page: this.meta.page,
                            limit: this.meta.limit,
                            due_date: this.searchQuery,
                        },
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    }
                )

                // Save tasks and pagination data
                this.privateTasks = response.data.items
                this.meta = response.data.meta

                // Remember request type
                this.lastRequest = { type: 'duedate' }
            }
            catch (err) {
                this.error = err.response?.data?.message || err.message || 'Something went wrong';

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    totalItems: 0,
                    totalPages: 0,
                }
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by month
        async findPrivateTasksByMonth(
        ) {

            const currentYear = new Date().getFullYear()

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_MONTH,
                    {
                        params: {
                            page: this.meta.page,
                            limit: this.meta.limit,
                            year: currentYear,
                            month: this.searchQuery,
                        },
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    }
                )

                // Save tasks and pagination data
                this.privateTasks = response.data.items
                this.meta = response.data.meta

                // Remember request type
                this.lastRequest = { type: 'month' }
            }
            catch (err) {
                this.error = err.response?.data?.message || err.message || 'Something went wrong';

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    totalItems: 0,
                    totalPages: 0,
                }
            }
            finally {
                this.loading = false
            }
        },

        // ==========================
        // POST
        // ==========================

        // Create private task
        async createPrivateTask(data) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.post(API_ENDPOINTS.CREATE_PRIVATE_TASK, data,
                    {
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    })

                await this.repeatLastRequest()
                return response.data
            }
            catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong';

                throw err
            }
            finally {
                this.loading = false
            }
        },

        // ==========================
        // PUT
        // ==========================

        // Update private task
        async updatePrivateTask(data) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.put(API_ENDPOINTS.UPDATE_PRIVATE_TASK,
                    data,
                    {
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    })

                await this.repeatLastRequest()
                return response.data
            }
            catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong';

                throw err
            }
            finally {
                this.loading = false
            }
        },

        // ==========================
        // DELETE
        // ==========================

        // Remove private task
        async removePrivateTask(taskId) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.delete(API_ENDPOINTS.DELETE_PRIVATE_TASK,
                    {
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                        data: {
                            taskId: taskId
                        }
                    })

                await this.repeatLastRequest()
                return response.data
            }
            catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong';

                throw err
            }
            finally {
                this.loading = false
            }
        },

        // ==========================
        // OTHER
        // ==========================

        // Pagination helpers
        async setPage(page) {
            this.meta.page = page;
            await this.repeatLastRequest();
        },

        async setLimit(limit) {
            this.meta.limit = limit;
            this.meta.page = 1;
            await this.repeatLastRequest();
        },

        async nextPage() {
            if (this.meta.page < this.meta.totalPages) {
                this.meta.page++;
                await this.repeatLastRequest();
            }
        },

        async prevPage() {
            if (this.meta.page > 1) {
                this.meta.page--;
                await this.repeatLastRequest();
            }
        },

        // Repeat last request
        async repeatLastRequest() {
            if (!this.lastRequest) {
                await this.fetchPrivateTasks();
                return;
            };

            const { type } = this.lastRequest;

            switch (type) {
                case 'all':
                    await this.fetchPrivateTasks();
                    break;
                case 'title':
                    await this.findPrivateTasksByTitle();
                    break;
                case 'description':
                    await this.findPrivateTasksByDescription();
                    break;
                case 'duedate':
                    await this.findPrivateTasksByDueDate();
                    break;
                case 'month':
                    await this.findPrivateTasksByMonth();
                    break;
            }
        },

        // Clear search input field
        async clearSearch() {
            this.searchQuery = '';
            this.meta.page = 1;
        },
        async clearError() {
            this.error = null
        }
    }
})