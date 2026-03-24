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

    currentUser: null,

    // Pagination metadata
    meta: {
      page: 1,
      limit: 10,
      totalItems: 0,
      totalPages: 0,
    },

    // Stores information about last request (used for refresh)
    lastRequest: null,
    searchQuery: '',
    searchType: 'all',
    accessDenied: false,
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
    async fetchMe() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null
      try {
        // Send GET request to backend
        const response = await api.get(API_ENDPOINTS.GET_ME_KANBAN_MEMBER, {
          params: {
            board_id: this.boardId,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        this.currentUser = response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },

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

        if (this.members.length == 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }

        // Remember request type
        this.lastRequest = { type: 'all' }
        this.searchQuery = ''
        this.accessDenied = false
      } catch (err) {
        if (err.response?.status === 403) {
          this.error = 'forbidden'
          this.members = []
          this.accessDenied = true
          return
        }

        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },

    // Get members by email
    async getMemberByEmail() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_KANBAN_MEMBER_BY_EMAIL, {
          params: {
            board_id: this.boardId,
            email: this.searchQuery,
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

        if (this.members.length == 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }

        // Remember request type
        this.lastRequest = {
          type: 'email',
          query: this.searchQuery,
        }
        this.accessDenied = false
      } catch (err) {
        if (err.response?.status === 403) {
          this.error = 'forbidden'
          this.members = []
          this.accessDenied = true
          return
        }

        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },

    // Get members by role
    async getMemberByRole() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_KANBAN_MEMBERS_BY_ROLE, {
          params: {
            board_id: this.boardId,
            role: this.searchQuery,
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

        if (this.members.length == 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }

        // Remember request type
        this.lastRequest = {
          type: 'role',
          query: this.searchQuery,
        }
        this.accessDenied = false
      } catch (err) {
        if (err.response?.status === 403) {
          this.error = 'forbidden'
          this.members = []
          this.accessDenied = true
          return
        }

        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
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

        await this.repeatLastRequest()
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

        await this.repeatLastRequest()
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
          data: data,
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.repeatLastRequest()
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
      await this.repeatLastRequest()
    },

    async setLimit(limit) {
      this.meta.limit = limit
      this.meta.page = 1
      await this.repeatLastRequest()
    },

    async nextPage() {
      if (this.meta.page < this.meta.totalPages) {
        this.meta.page++
        await this.repeatLastRequest()
      }
    },

    async prevPage() {
      if (this.meta.page > 1) {
        this.meta.page--
        await this.repeatLastRequest()
      }
    },

    async repeatLastRequest() {
      if (!this.lastRequest) {
        return await this.fetchKanbanMembers()
      }

      if (this.lastRequest.type === 'all') {
        await this.fetchKanbanMembers()
      } else if (this.lastRequest.type === 'email') {
        this.searchQuery = this.lastRequest.query
        await this.getMemberByEmail()
      } else if (this.lastRequest.type === 'role') {
        this.searchQuery = this.lastRequest.query
        await this.getMemberByRole()
      }
    },
    clearError() {
      this.error = null
    },
  },
})
