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
            total_users: 0,
            total_pages: 0,
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
        async fetchPrivateTasks(page = this.meta.page, limit = this.meta.limit) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_ALL_PRIVATE_TASKS, {
                    params: { page, limit },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                // Save tasks and pagination data
                this.privateTasks = response.data.items
                this.meta = response.data.meta

                // Remember request type
                this.lastRequest = { type: 'all' }
            } catch (err) {
                this.error = err.response?.data?.message
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by title
        async findPrivateTasksByTitle(
            searchQuery = this.searchQuery,
            page = this.meta.page,
            limit = this.meta.limit
        ) {

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_TITLE,
                    {
                        params: { 
                            page,
                            limit,
                            title: searchQuery,
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
                this.lastRequest = { type: 'title', payload: searchQuery }
            }
            catch (err) {
                this.error = err.response?.data?.message
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by description
        async findPrivateTasksByDescription(
            searchQuery = this.searchQuery,
            page = this.meta.page,
            limit = this.meta.limit
        ) {
            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_DESCRIPTION,
                    {
                        params: { 
                            page, 
                            limit,
                            description: searchQuery,
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
                this.lastRequest = { type: 'description', payload: searchQuery }
            }
            catch (err) {
                this.error = err.response?.data?.message
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by duedate
        async findPrivateTasksByDueDate(
            searchQuery = this.searchQuery,
            page = this.meta.page,
            limit = this.meta.limit
        ) {
            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_DUEDATE,
                    {
                        params: { 
                            page, 
                            limit,
                            duedate: searchQuery,
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
                this.lastRequest = { type: 'duedate', payload: searchQuery }
            }
            catch (error) {
                console.error('Error fetching tasks:', error)
                this.error = error.message
            }
            finally {
                this.loading = false
            }
        },

        // Get tasks by month
        async findPrivateTasksByMonth(
            searchQuery = this.searchQuery,
            page = this.meta.page,
            limit = this.meta.limit
        ) {

            const currentYear = new Date().getFullYear()

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_TASKS_BY_MONTH,
                    {
                        params: { 
                            page, 
                            limit,
                            year: currentYear,
                            month: searchQuery,
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
                this.lastRequest = { type: 'month', payload: searchQuery }
            }
            catch (error) {
                console.error('Error fetching tasks:', error)
                this.error = error.message
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
                const response = await api.post(API_ENDPOINTS.CREATE_PRIVATE_TASK, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                return response.data
            }
            catch (err) {
                this.error = err.response?.data?.message
            }
            finally {
                this.loading = false
            }
        },

        // ==========================
        // PUT
        // ==========================

        // Update private task
        async updatePrivateTask(taskId, data) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.put(API_ENDPOINTS.UPDATE_PRIVATE_TASK(taskId), data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                return response.data
            }
            catch (err) {
                this.error = err.response?.data?.message
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
                const response = await api.delete(API_ENDPOINTS.REMOVE_PRIVATE_TASK(taskId), {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                return response.data
            }
            catch (err) {
                this.error = err.response?.data?.message
            }
            finally {
                this.loading = false
            }
        },
    }
})