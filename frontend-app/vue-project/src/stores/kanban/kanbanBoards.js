// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useKanbanBoardStore = defineStore('kanban', {
  // ==========
  // STATE
  // ==========
  state: () => ({
    selectedBoard: null,
    boards: [],
    loading: false,
    error: null,

    // Search configuration
    searchMode: 'all',
    searchQuery: '',

    // Stores information about last request (used for refresh)
    lastRequest: null,

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
    hasKanbanBoards() {
      return this.boards.length > 0
    },
  },

  // ==========================
  // ACTIONS
  // ==========================
  actions: {
    // ==========================
    // GET
    // ==========================
    // Get all boards
    async fetchKanbanBoards() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_ALL_BOARDS, {
          params: {
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        // Save tasks and pagination data
        this.boards = response.data.items
        this.meta = response.data.meta

        // Remember request type
        this.lastRequest = { type: 'all' }
        this.searchQuery = ''

        if (this.boards.length === 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'

        // reset pagination
        this.meta = {
          page: 1,
          limit: 10,
          totalItems: 0,
          totalPages: 1,
        }
        this.boards = []
      } finally {
        this.loading = false
      }
    },
    // Get boards by title
    async findKanbanBoardsByTitle() {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.get(API_ENDPOINTS.GET_BOARDS_BY_TITLE, {
          params: {
            title: this.searchQuery,
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        // Save tasks and pagination data
        this.boards = response.data.items
        this.meta = response.data.meta

        // Remember request type
        this.lastRequest = {
          type: 'title',
          query: this.searchQuery,
        }

        if (this.boards.length === 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'

        // reset pagination
        this.meta = {
          page: 1,
          limit: 10,
          totalItems: 0,
          totalPages: 1,
        }
        this.boards = []
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // POST
    // ==========================
    async createBoard(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.post(API_ENDPOINTS.CREATE_BOARD, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.repeatLastRequest()
        return response.data
      } catch (err) {
        this.error = err.response?.data?.message || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // PUT
    // ==========================
    async updateBoard(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_BOARD, data, {
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
    // ==========================
    // DELETE
    // ==========================
    async deleteBoard(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_BOARD, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
          data: {
            boardId: data,
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

    // Repeat last request
    async repeatLastRequest() {
      if (!this.lastRequest) {
        await this.fetchKanbanBoards()
        return
      }

      const { type, query } = this.lastRequest

      switch (type) {
        case 'all':
          await this.fetchKanbanBoards()
          break

        case 'title':
          this.searchQuery = query
          await this.findKanbanBoardsByTitle()
          break
      }
    },

    // Clear search input field
    async clearSearch() {
      this.searchQuery = ''
      this.meta.page = 1
    },
    async clearError() {
      this.error = null
    },
  },
})
