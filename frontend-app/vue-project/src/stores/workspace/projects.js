// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useWorkspaceProjectsStore = defineStore('workspaceProjects', {
  state: () => ({
    projects: [],
    selectedProject: null,
    loading: false,
    error: null,

    // Search configuration
    searchMode: 'all',
    searchQuery: '',

    // Stores last request
    lastRequest: null,

    // Pagination metadata
    meta: {
      page: 1,
      limit: 10,
      totalItems: 0,
      totalPages: 0,
    },
  }),

  //=========
  // GETTERS
  //=========
  getters: {
    hasProjects() {
      return this.projects.length > 0
    },
  },

  //=========
  // ACTIONS
  //=========
  actions: {
    // ==========================
    // GET
    // ==========================
    // Get all projects
    async getAllProjects() {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.get(API_ENDPOINTS.GET_ALL_PROJECTS, {
          params: {
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        // Save tasks and pagination data
        this.projects = response.data.items
        this.meta = response.data.meta

        // Remember request type
        this.lastRequest = { type: 'all' }
        this.searchQuery = ''

        if (this.projects.length === 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }
      } catch (err) {
        this.meta = {
          page: 1,
          limit: 10,
          totalItems: 0,
          totalPages: 1,
        }

        this.projects = []
      } finally {
        this.loading = false
      }
    },

    // Get projects by title
    async getProjectsByTitle() {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.get(API_ENDPOINTS.GET_PROJECT_BY_TITLE, {
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
        this.projects = response.data.items
        this.meta = response.data.meta

        // Remember request type
        this.lastRequest = {
          type: 'title',
          query: this.searchQuery,
        }

        if (this.projects.length === 0) {
          this.meta.totalPages = 1
          this.meta.page = 1
        }
      } catch (err) {
        this.meta = {
          page: 1,
          limit: 10,
          totalItems: 0,
          totalPages: 1,
        }

        this.projects = []
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // POST
    // ==========================
    async createProject(data) {
      /*
            data = {
                title: string,
                description: string,
                email: string,
            }
            */

      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.post(API_ENDPOINTS.CREATE_PROJECT, data, {
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
    // PUT
    // ==========================
    async updateProject(data) {
      /*
            data = {
                title: string,
                description: string,
                projectId: string,
            }
            */

      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_PROJECT, data, {
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
    async deleteProject(data) {
      /*
            data = {
                projectId: string,
            }
            */

      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_PROJECT, {
          data,
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
        await this.getAllProjects()
        return
      }

      const { type, query } = this.lastRequest

      switch (type) {
        case 'all':
          await this.getAllProjects()
          break

        case 'title':
          this.searchQuery = query
          await this.getProjectsByTitle()
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
