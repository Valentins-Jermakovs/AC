import { defineStore } from 'pinia'
import { api } from '@/services/axios'
import { API_ENDPOINTS } from '@/config/api'
import { useAuthStore } from './auth'

export const useEventParticipantsStore = defineStore('eventParticipants', {
    state: () => ({
        selectedEvent: null,
        participants: [],

        loading: false,
        error: null,

        meta: {
            page: 1,
            limit: 10,
            total_items: 0,
            total_pages: 0,
        },

        searchMode: 'all',
        searchQuery: '',

        lastRequest: {
            type: 'all'
        }, // { type: 'all' | 'email' }
    }),
    actions: {
        async fetchParticipants() {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            this.participants = []

            try {
                const response = await api.get(API_ENDPOINTS.GET_ALL_PARTICIPANTS, {
                    params: {
                        event_id: this.selectedEvent.id,
                        page: this.meta.page,
                        limit: this.meta.limit
                    },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                this.participants = response.data.participants
                this.meta = response.data.metadata || {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 1,
                }
                this.lastRequest = { type: 'all' }
                this.searchQuery = ''
            } catch (error) {
                this.error = error.response?.data?.detail || error.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        },
        async fetchParticipantsByEmail(email = this.searchQuery) {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_PARTICIPANTS_BY_EMAIL, {
                    params: {
                        event_id: this.selectedEvent.id,
                        email: email,
                        page: this.meta.page,
                        limit: this.meta.limit
                    },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                this.participants = response.data.participants
                this.meta = response.data.metadata || {
                    page: 1,
                    limit: 10,
                    total_items: 0,
                    total_pages: 1,
                }
                this.lastRequest = { type: 'email', email }
            } catch (error) {
                this.error = error.response?.data?.detail || error.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        },
        async createParticipant(data) {

            /*
            data = {
                "eventId": 1,
                "email": "Ig0wz@example.com"
            }
            */

            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.post(API_ENDPOINTS.CREATE_PARTICIPANT, data, {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })
                await this.refresh()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },

        async removeParticipant(eventId, userId) {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.delete(API_ENDPOINTS.DELETE_PARTICIPANT(eventId, userId), {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                await this.refresh()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },
        async leaveEvent() {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.delete(API_ENDPOINTS.LEAVE_EVENT(eventId = this.selectedEvent.Id), {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })
            }
            catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            }
            finally {
                this.loading = false
            }
        },
        // --------------------------
        // Pagination
        // --------------------------
        async setPage(page) {
            this.meta.page = page
            await this.refresh()
        },

        async setLimit(limit) {
            this.meta.limit = limit
            this.meta.page = 1
            await this.refresh()
        },

        async nextPage() {
            if (this.meta.page < this.meta.total_pages) {
                this.meta.page++
                await this.refresh()
            }
        },

        async prevPage() {
            if (this.meta.page > 1) {
                this.meta.page--
                await this.refresh()
            }
        },

        async refresh() {
            if (!this.lastRequest) {
                await this.fetchParticipants()
                return
            }

            if (this.lastRequest.type === 'all') {
                await this.fetchParticipants()
            } else if (this.lastRequest.type === 'email') {
                await this.fetchParticipantsByEmail(this.lastRequest.email)
            }
        },
        // --------------------------
        // Clear
        // --------------------------
        clearSearch() {
            this.searchMode = 'all'
            this.searchQuery = ''
        },
        clearError() {
            this.error = null
        },
    },
})