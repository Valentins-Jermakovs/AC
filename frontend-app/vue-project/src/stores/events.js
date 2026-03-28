// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth and User stores (used for token and role checking)
import { useAuthStore } from './auth'

// Create Admin store
export const useEventsStore = defineStore('events', {
    state: () => ({
        events: [],
        participants: [],
        selectedEvent: null,

        meta: {
            page: 1,
            limit: 10,
            total_users: 0,
            total_pages: 0,
        },

        loading: false, // Indicates request is in progress
        error: null, // Stores error message

        // Search configuration
        searchMode: 'all',
        searchQuery: '',

        // Stores information about last request (used for refresh)
        lastRequest: null,
    }),
    actions: {
        async getAllEvents() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_ALL_EVENTS, {
                    params: { page: this.meta.page, limit: this.meta.limit },
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                // Store result as single-item array
                this.events = response.data.events

                // Save pagination data
                this.meta = response.data.metadata

                // Remember request type
                this.lastRequest = { type: 'all' }
                this.searchQuery = ''
            } catch (error) {
                this.error = error.response?.data?.detail || error.message || 'Something went wrong'
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_events: 0,
                    total_pages: 0,
                }
            }
        },
        async getEventsByTitle() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_EVENTS_BY_TITLE, {
                    params: { page: this.meta.page, limit: this.meta.limit, title: this.searchQuery },
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                // Store result as single-item array
                this.events = response.data.events

                // Save pagination data
                this.meta = response.data.metadata

                // Remember request type
                this.lastRequest = { type: 'title' }
            } catch (error) {
                this.error = error.response?.data?.detail || error.message || 'Something went wrong'
                this.meta = {
                    page: 1,
                    limit: 10,
                    total_events: 0,
                    total_pages: 1,
                }
            }
        },
        async getEventsByMonth(month, year) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_EVENTS_IN_MONTH, {
                    params: {
                        month: month,
                        year: year
                    },
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                // Store result as single-item array
                this.events = response.data.events

                // Save pagination data
                this.meta = response.data.metadata

                // Remember request type
                this.lastRequest = { type: 'month' }
            } catch (error) {
                this.error = error.response?.data?.detail || error.message || 'Something went wrong'
            }
        },
        async createEvent(data) {
            /*
            {
                "allDay": true,
                "color": "primary",
                "creatorEmail": "test@outlook.com",
                "description": "Event description",
                "endDate": "2026-04-05",
                "endTime": "00:00",
                "startDate": "2026-03-30",
                "startTime": "00:00",
                "status": "active",
                "title": "Event title"
            }
            */

            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.post(API_ENDPOINTS.CREATE_EVENT, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                await this.repeatLastRequest()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'

                throw err
            } finally {
                this.loading = false
            }
        },
        async updateEvent(data) {
            /*
            {
                "allDay": true,
                "color": "primary",
                "description": "Event description",
                "endDate": "2023-01-01",
                "endTime": "00:00",
                "eventId": "event_id",
                "startDate": "2023-01-01",
                "startTime": "00:00",
                "status": "active",
                "title": "Event title"
            }
            */

            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.put(API_ENDPOINTS.UPDATE_EVENT, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                await this.repeatLastRequest()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'

                throw err
            } finally {
                this.loading = false
            }
        },
        async removeEvent(eventId) {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.delete(API_ENDPOINTS.DELETE_EVENT(eventId), {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                await this.repeatLastRequest()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'

                throw err
            } finally {
                this.loading = false
            }
        }
    }
})