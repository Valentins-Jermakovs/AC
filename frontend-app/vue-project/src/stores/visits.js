// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth and User stores (used for token and role checking)
import { useAuthStore } from './auth'

export const useVisitsStore = defineStore('visits', {
  state: () => ({
    visits: [],
    loading: false,
    error: null,
  }),
  actions: {
    async registerVisit() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.post(
          API_ENDPOINTS.REGISTER_VISIT,
          {},
          {
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    async startSession() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.post(
          API_ENDPOINTS.START_SESSION,
          {},
          {
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    async endSession() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.post(
          API_ENDPOINTS.END_SESSION,
          {},
          {
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    async getWeekStats() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.WEEK_STATS, {
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        })

        this.visits = response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
