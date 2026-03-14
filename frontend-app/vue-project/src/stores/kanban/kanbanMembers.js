// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useKanbanMembersStore = defineStore('kanbanMembers', {
  // ==========
  // STATE
  // ==========
  state: () => ({
    members: [],
    loading: false,
    error: null,
    boardId: null,

    // Pagination metadata
    meta: {
      page: 1,
      limit: 10,
      totalItems: 0,
      totalPages: 0,
    },
  }),

  // ===========
  // GETTERS
  // ===========
  getters: {
    hasMembers() {
      return this.members.length > 0
    },
  },

  // ==========================
  // ACTIONS
  // ==========================
  actions: {
    // ==========================
    // GET
    // ==========================
    async fetchKanbanMembers() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_KANBAN_MEMBERS, {
          params: {
            board_id: this.boardId,
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        // Save tasks and pagination data
        this.members = response.data.items
        this.meta = response.data.meta
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // POST
    // ==========================
    async addMember(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.post(API_ENDPOINTS.ADD_KANBAN_MEMBER, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.fetchKanbanMembers()
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // PUT
    // ==========================
    async updateMember(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_KANBAN_MEMBER, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.fetchKanbanMembers()
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // DELETE
    // ==========================
    async deleteMember(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_KANBAN_MEMBER, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
          data: {
            boardId: data.boardId,
            userId: data.userId,
          },
        })

        await this.fetchKanbanMembers()
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },

    // Pagination helpers
    async setPage(page) {
      this.meta.page = page
      await this.fetchKanbanMembers()
    },

    async setLimit(limit) {
      this.meta.limit = limit
      this.meta.page = 1
      await this.fetchKanbanMembers()
    },

    async nextPage() {
      if (this.meta.page < this.meta.totalPages) {
        this.meta.page++
        await this.fetchKanbanMembers()
      }
    },

    async prevPage() {
      if (this.meta.page > 1) {
        this.meta.page--
        await this.fetchKanbanMembers()
      }
    },
  },
})
