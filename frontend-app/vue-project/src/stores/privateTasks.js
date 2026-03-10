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
            total_items: 0,
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

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 0,
                }
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

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 0,
                }
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

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 0,
                }
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
                this.error = error.message

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 0,
                }
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
                this.error = error.message

                // reset pagination
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 0,
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

        // ==========================
        // OTHER
        // ==========================

        // Pagination helpers
        async setPage(page) {
            this.meta.page = page
            await this.fetchUsers(page, this.meta.limit)
        },

        async setLimit(limit) {
            this.meta.limit = limit
            this.meta.page = 1
        },

        async nextPage() {
            if (this.meta.page < this.meta.total_pages) {
                this.meta.page++
                await this.fetchUsers(this.meta.page, this.meta.limit)
            }
        },

        async prevPage() {
            if (this.meta.page > 1) {
                this.meta.page--
                await this.fetchUsers(this.meta.page, this.meta.limit)
            }
        },

        // Repeat last request
        async repeatLastRequest() {
            if (this.lastRequest.type === 'all') {
                await this.fetchPrivateTasks(this.meta.page, this.meta.limit)
            }
            else if (this.lastRequest.type === 'title') {
                await this.findPrivateTasksByTitle(this.lastRequest.payload, this.meta.page, this.meta.limit)
            }
            else if (this.lastRequest.type === 'description') {
                await this.findPrivateTasksByDescription(this.lastRequest.payload, this.meta.page, this.meta.limit)
            }
            else if (this.lastRequest.type === 'duedate') {
                await this.findPrivateTasksByDueDate(this.lastRequest.payload, this.meta.page, this.meta.limit)
            }
            else if (this.lastRequest.type === 'month') {
                await this.findPrivateTasksByMonth(this.lastRequest.payload, this.meta.page, this.meta.limit)
            }
        },

        // Clear search input field
        clearSearch() {
            this.searchQuery = ''
        },
    }
})