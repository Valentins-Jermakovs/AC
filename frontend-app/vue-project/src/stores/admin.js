import { defineStore } from 'pinia'
import { api } from '@/services/axios'
import { API_ENDPOINTS } from '@/config/api'
import { useAuthStore } from './auth'
import { useUserStore } from './user'

export const useAdminStore = defineStore('admin', {
    state: () => ({
        users: [],
        meta: {
            page: 1,
            limit: 10,
            total_users: 0,
            total_pages: 0,
        },
        loading: false,
        error: null,
        searchMode: 'all',
        searchQuery: '',
    }),

    getters: {
        hasUsers: (state) => state.users.length > 0,
    },

    actions: {
        async fetchUsers(page = this.meta.page, limit = this.meta.limit) {

            const authStore = useAuthStore()
            const userStore = useUserStore()

            if (!userStore.isAdmin) {
                this.error = 'You are not an admin'
                return
            }

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_USERS, {
                    params: { page, limit },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                this.users = response.data.items
                this.meta = response.data.meta

            } catch (err) {
                this.error = err.response?.data?.detail || err.message
            } finally {
                this.loading = false
            }
        },

        async getUserById(id) {
            const authStore = useAuthStore()
            const userStore = useUserStore()

            if (!userStore.isAdmin) {
                this.error = 'You are not an admin'
                return
            }

            this.loading = true
            this.error = null

            try {
                const response = await api.get(
                    API_ENDPOINTS.GET_USER_BY_ID(id),
                    {
                        headers: { Authorization: `Bearer ${authStore.accessToken}` },
                    }
                )


                this.users = [response.data]

                if (!response.data) {
                    this.error = 'User not found'
                    return null
                }

                return response.data

            } catch (err) {
                this.error = err.response?.data?.detail || err.message
                return null
            } finally {
                this.loading = false
            }
        },

        async getUserByNameEmail(searchString, page = this.meta.page, limit = this.meta.limit) {
            const authStore = useAuthStore()
            const userStore = useUserStore()

            if (!userStore.isAdmin) {
                this.error = 'You are not an admin'
                return
            }

            this.loading = true
            this.error = null

            try {
                // endpoint ar path param + query param
                const response = await api.get(
                    API_ENDPOINTS.GET_USER_BY_USERNAME_OR_EMAIL(encodeURIComponent(searchString)),
                    {
                        params: { page, limit },
                        headers: { Authorization: `Bearer ${authStore.accessToken}` },
                    }
                )

                this.users = response.data.items
                this.meta = response.data.meta
            } catch (err) {
                this.error = err.response?.data?.detail || err.message
                this.users = []
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_users: 0,
                    total_pages: 0,
                }
            } finally {
                this.loading = false
            }
        },

        async getUserByRole(searchString, page = this.meta.page, limit = this.meta.limit) {
            const authStore = useAuthStore()
            const userStore = useUserStore()

            if (!userStore.isAdmin) {
                this.error = 'You are not an admin'
                return
            }

            this.loading = true
            this.error = null

            try {
                // endpoint ar path param + query param
                const response = await api.get(
                    API_ENDPOINTS.GET_USER_BY_ROLE(encodeURIComponent(searchString)),
                    {
                        params: { page, limit },
                        headers: { Authorization: `Bearer ${authStore.accessToken}` },
                    }
                )

                this.users = response.data.items
                this.meta = response.data.meta
            } catch (err) {
                this.error = err.response?.data?.detail || err.message
                this.users = []
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_users: 0,
                    total_pages: 0,
                }
            } finally {
                this.loading = false
            }
        },


        async setPage(page) {
            this.meta.page = page
            await this.fetchUsers(page, this.meta.limit)
        },

        async setLimit(limit) {
            this.meta.limit = limit;
            this.meta.page = 1; // lai sāktu no pirmās lapas pēc limit maiņas

            // Pārbauda, kurš meklēšanas režīms ir aktīvs
            if (this.searchMode === 'username') {
                await this.getUserByNameEmail(this.searchQuery, 1, limit);
            } else if (this.searchMode === 'role') {
                await this.getUserByRole(this.searchQuery, 1, limit);
            } else {
                await this.fetchUsers(1, limit);
            }
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

        clearSearch() {
            this.searchQuery = ''
        }
    }
})