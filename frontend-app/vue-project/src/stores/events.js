import { defineStore } from 'pinia'
import { api } from '@/services/axios'
import { API_ENDPOINTS } from '@/config/api'
import { useAuthStore } from './auth'

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [],
    selectedEvent: null,

    meta: {
      page: 1,
      limit: 10,
      total_events: 0,
      total_pages: 0,
    },

    loading: false,
    error: null,

    searchMode: 'all',
    searchQuery: '',

    lastRequest: null, // { type: 'all' | 'month' }

    isCreator: false,
  }),
  actions: {
    // ===== EVENTS MANAGEMENT =====
    async checkIsCreator() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_IS_EVENT_CREATOR, {
          params: { event_id: this.selectedEvent.id },
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        })

        this.isCreator = response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },
    async getAllEvents() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_ALL_EVENTS, {
          params: { page: this.meta.page, limit: this.meta.limit },
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        })

        this.events = response.data.events
        this.meta = response.data.metadata || {
          page: 1,
          limit: 10,
          total_events: 0,
          total_pages: 0,
        }
        this.lastRequest = { type: 'all' }
        this.searchQuery = ''
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Something went wrong'
      } finally {
        this.loading = false
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

        this.events = response.data.events
        this.meta = response.data.metadata || {
          page: 1,
          limit: 10,
          total_events: 0,
          total_pages: 1,
        }
        this.lastRequest = { type: 'title', title: this.searchQuery }
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },

    async getEventsByMonth(month, year) {
      if (this.loading) return

      
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_EVENTS_IN_MONTH, {
          params: { month, year, page: this.meta.page, limit: this.meta.limit },
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        })

        this.events = response.data.events
        this.meta = response.data.metadata || {
          page: 1,
          limit: 10,
          total_events: 0,
          total_pages: 0,
        }
        this.lastRequest = { type: 'month', month, year }
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },

    async createEvent(data) {
      /* data = {
        "allDay": true,
        "color": "primary",
        "creatorEmail": "Ig0wz@example.com",
        "description": "Event description",
        "endDate": "2023-01-01",
        "endTime": "00:00",
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
        const response = await api.post(API_ENDPOINTS.CREATE_EVENT, data, {
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

    async updateEvent(data) {
      /*
      data = {
        "allDay": true,
        "color": "primary",
        "description": "Event description",
        "endDate": "2023-01-01",
        "endTime": "00:00",
        "startDate": "2023-01-01",
        "startTime": "00:00",
        "status": "active",
        "title": "Event title",
        "eventId": 1
      }
      */
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_EVENT, data, {
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

    async removeEvent(eventId) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_EVENT(eventId), {
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
      if (!this.lastRequest) return await this.getAllEvents()

      switch (this.lastRequest.type) {
        case 'all':
          await this.getAllEvents()
          break
        case 'month':
          await this.getEventsByMonth(this.lastRequest.month, this.lastRequest.year)
          break
        case 'title':
          this.searchQuery = this.lastRequest.title || ''
          await this.getEventsByTitle()
          break
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
