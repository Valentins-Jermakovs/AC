// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store
import { useAuthStore } from './auth'

export const useExpenseStore = defineStore('expense', {
    state: () => ({
        expenses: [],
        stats: [],
        fromDate: null,
        toDate: null,
        category: null,
        loading: false,
        error: null,

        meta: {
            page: 1,
            limit: 10,
            total_expenses: 0,
            total_pages: 0,
        },

        selectedExpense: null
    }),

    actions: {
        // --------------------------
        // Core fetch
        // --------------------------
        async getExpenses() {
            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_EXPENSES, {
                    params: {
                        from_date: this.fromDate,
                        to_date: this.toDate,
                        category: this.category,
                        page: this.meta.page,
                        limit: this.meta.limit
                    },
                    headers: {
                        Authorization: `Bearer ${useAuthStore().token}`
                    }
                })

                this.expenses = response.data.expenses
                this.stats = response.data.stats

                // meta info (if backend provides it)
                this.meta.total_pages = response.data.meta?.total_pages || 0
                this.meta.total_expenses = response.data.meta?.total_expenses || 0

                // fix page overflow (after delete for example)
                if (this.meta.page > this.meta.total_pages) {
                    this.meta.page = this.meta.total_pages || 1
                }

            } catch (error) {
                this.error = error.response?.data?.detail || 'Error fetching expenses'
            } finally {
                this.loading = false
            }
        },

        async getStats() {
            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_EXPENSES_STATS, {
                    headers: {
                        Authorization: `Bearer ${useAuthStore().token}`
                    }
                })

                this.stats = response.data

            } catch (error) {
                this.error = error.response?.data?.detail || 'Error fetching stats'
            } finally {
                this.loading = false
            }
        },

        // --------------------------
        // Helper: refresh wrapper
        // --------------------------
        async withRefresh(callback) {
            const result = await callback()
            await this.getExpenses()
            return result
        },

        // --------------------------
        // CRUD
        // --------------------------
        async createExpense(data) {
            this.loading = true
            this.error = null

            try {
                return await this.withRefresh(async () => {
                    const response = await api.post(
                        API_ENDPOINTS.CREATE_EXPENSE,
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
                this.error = error.response?.data?.detail || 'Error creating expense'
            } finally {
                this.loading = false
            }
        },

        async updateExpanse(data) {
            this.loading = true
            this.error = null

            try {
                return await this.withRefresh(async () => {
                    const response = await api.put(
                        API_ENDPOINTS.UPDATE_EXPENSE(this.selectedExpense.expense_id),
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
                this.error = error.response?.data?.detail || 'Error updating expense'
            } finally {
                this.loading = false
            }
        },

        async deleteExpense(expenseId) {
            this.loading = true
            this.error = null

            try {
                return await this.withRefresh(async () => {
                    const response = await api.delete(
                        API_ENDPOINTS.DELETE_EXPENSE(expenseId),
                        {
                            headers: {
                                Authorization: `Bearer ${useAuthStore().token}`
                            }
                        }
                    )
                    return response.data
                })
            } catch (error) {
                this.error = error.response?.data?.detail || 'Error deleting expense'
            } finally {
                this.loading = false
            }
        },

        // --------------------------
        // Pagination
        // --------------------------
        async setPage(page) {
            this.meta.page = page
            await this.getExpenses()
        },

        async setLimit(limit) {
            this.meta.limit = limit
            this.meta.page = 1
            await this.getExpenses()
        },

        async nextPage() {
            if (this.meta.page < this.meta.total_pages) {
                this.meta.page++
                await this.getExpenses()
            }
        },

        async prevPage() {
            if (this.meta.page > 1) {
                this.meta.page--
                await this.getExpenses()
            }
        },

        // --------------------------
        // Filters
        // --------------------------
        async setFilters({ fromDate, toDate, category }) {
            this.fromDate = fromDate
            this.toDate = toDate
            this.category = category
            this.meta.page = 1
            await this.getExpenses()
        },

        // --------------------------
        // Manual refresh
        // --------------------------
        async repeatLastRequest() {
            await this.getExpenses()
        }
    }
})