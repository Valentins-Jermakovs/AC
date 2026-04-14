// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store
import { useAuthStore } from './auth'

export const usePaymentStore = defineStore('payment', {
  state: () => ({
    payments: [],
    meta: {
      total_items: 0,
      total_pages: 0,
      page: 1,
      limit: 10,
    },
    loading: false,
    error: null,
  }),

  actions: {
    // --------------------------
    // Fetch (uses last page/limit)
    // --------------------------
    async fetchPayments() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_PAYMENTS, {
          params: {
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        this.payments = response.data.items || []
        this.meta.total_items = response.data.total_items
        this.meta.total_pages = response.data.total_pages

        // fix if page becomes invalid (after delete)
        if (this.meta.page > this.meta.total_pages) {
          this.meta.page = this.meta.total_pages || 1
        }
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Helper: repeat last request
    // --------------------------
    async withRefresh(callback) {
      const result = await callback()
      await this.fetchPayments()
      return result
    },

    // --------------------------
    // CRUD
    // --------------------------
    async createPayment(data) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        return await this.withRefresh(async () => {
          const response = await api.post(API_ENDPOINTS.CREATE_PAYMENT, data, {
            headers: {
              Authorization: `Bearer ${authStore.accessToken}`,
            },
          })
          return response.data
        })
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error creating payment'
      } finally {
        this.loading = false
      }
    },

    async updatePayment(data, payment_id) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        return await this.withRefresh(async () => {
          const response = await api.put(API_ENDPOINTS.UPDATE_PAYMENT(payment_id), data, {
            headers: {
              Authorization: `Bearer ${authStore.accessToken}`,
            },
          })
          return response.data
        })
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error updating payment'
      } finally {
        this.loading = false
      }
    },

    async deletePayment(payment_id) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        return await this.withRefresh(async () => {
          const response = await api.delete(API_ENDPOINTS.DELETE_PAYMENT(payment_id), {
            headers: {
              Authorization: `Bearer ${authStore.accessToken}`,
            },
          })
          return response.data
        })
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error deleting payment'
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Pagination
    // --------------------------
    async setPage(page) {
      this.meta.page = page
      await this.fetchPayments()
    },

    async setLimit(limit) {
      this.meta.limit = limit
      this.meta.page = 1
      await this.fetchPayments()
    },

    async nextPage() {
      if (this.meta.page < this.meta.total_pages) {
        this.meta.page++
        await this.fetchPayments()
      }
    },

    async prevPage() {
      if (this.meta.page > 1) {
        this.meta.page--
        await this.fetchPayments()
      }
    },

    // --------------------------
    // Manual refresh
    // --------------------------
    async repeatLastRequest() {
      await this.fetchPayments()
    },
  },
})
