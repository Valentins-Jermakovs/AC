// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store
import { useAuthStore } from './auth'

export const useBudgetStore = defineStore('budget', {
    state: () => ({
        budgets: [],
        yearAndMonth: '',
        loading: false,
        error: null,
    }),

    actions: {
        // --------------------------
        // Fetch
        // --------------------------
        async fetchBudgets() {
            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_BUDGETS, {
                    params: {
                        month: this.yearAndMonth
                    },
                    headers: {
                        Authorization: `Bearer ${useAuthStore().token}`
                    }
                })

                this.budgets = response.data

            } catch (error) {
                this.error = error.response?.data?.message || 'Error fetching budgets'
            } finally {
                this.loading = false
            }
        },

        // --------------------------
        // Helper: refresh wrapper
        // --------------------------
        async withRefresh(callback) {
            const result = await callback()
            await this.fetchBudgets()
            return result
        },

        // --------------------------
        // CRUD
        // --------------------------
        async createBudget(data) {
            this.loading = true
            this.error = null

            try {
                return await this.withRefresh(async () => {
                    const response = await api.post(
                        API_ENDPOINTS.CREATE_BUDGET,
                        data,
                        {
                            headers: {
                                Authorization: `Bearer ${useAuthStore().token}`
                            }
                        }
                    )
                    return response.data
                })
            } catch (error) {
                this.error = error.response?.data?.detail || 'Error creating budget'
            } finally {
                this.loading = false
            }
        },

        async updateBudget(data, budget_id) {
            this.loading = true
            this.error = null

            try {
                return await this.withRefresh(async () => {
                    const response = await api.put(
                        API_ENDPOINTS.UPDATE_BUDGET(budget_id),
                        data,
                        {
                            headers: {
                                Authorization: `Bearer ${useAuthStore().token}`
                            }
                        }
                    )
                    return response.data
                })
            } catch (error) {
                this.error = error.response?.data?.detail || 'Error updating budget'
            } finally {
                this.loading = false
            }
        },

        async deleteBudget(budget_id) {
            this.loading = true
            this.error = null

            try {
                return await this.withRefresh(async () => {
                    const response = await api.delete(
                        API_ENDPOINTS.DELETE_BUDGET(budget_id),
                        {
                            headers: {
                                Authorization: `Bearer ${useAuthStore().token}`
                            }
                        }
                    )
                    return response.data
                })
            } catch (error) {
                this.error = error.response?.data?.detail || 'Error deleting budget'
            } finally {
                this.loading = false
            }
        }
    }
})