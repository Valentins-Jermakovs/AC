import { defineStore } from 'pinia'
import { api } from '@/services/axios'
import { API_ENDPOINTS } from '@/config/api'
import { useAuthStore } from './auth'

export const useBudgetStore = defineStore('budget', {
  state: () => ({
    budgets: [],
    yearAndMonth: new Date().toISOString().slice(0, 7), // 🔥 FIX
    loading: false,
    error: null,
  }),

  actions: {
    // --------------------------
    // FETCH
    // --------------------------
    async fetchBudgets() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_BUDGETS, {
          params: {
            month: this.yearAndMonth || new Date().toISOString().slice(0, 7),
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        this.budgets = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error fetching budgets'
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // CREATE
    // --------------------------
    async createBudget(data) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const res = await api.post(API_ENDPOINTS.CREATE_BUDGET, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.fetchBudgets()
        return res.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error creating budget'
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // UPDATE (QUERY PARAM FIX)
    // --------------------------
    async updateBudget(budget_id, data) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const res = await api.put(API_ENDPOINTS.UPDATE_BUDGET, data, {
          params: {
            budget_id,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.fetchBudgets()
        return res.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error updating budget'
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // DELETE (QUERY PARAM FIX)
    // --------------------------
    async deleteBudget(budget_id) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const res = await api.delete(API_ENDPOINTS.DELETE_BUDGET, {
          params: { budget_id },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.fetchBudgets()
        return res.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Error deleting budget'
      } finally {
        this.loading = false
      }
    },
  },
})
