// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useWorkspaceProjectMembersStore = defineStore('workspaceProjectMembers', {
  state: () => ({
    projectMembers: [],
    loading: false,
    error: null,
    projectId: null,

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
      return this.projectMembers.length > 0
    },
  },
  // ===========
  // SETTERS
  // ===========
  setters: {
    setProjectId(projectId) {
      this.projectId = projectId
    },
  },

  // ==========================
  // ACTIONS
  // ==========================
  actions: {
    // ==========================
    // GET
    // ==========================
    // Get all project members
    async getAllMembers() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null
      try {
        const response = await api.get(API_ENDPOINTS.GET_PROJECT_ALL_MEMBERS, {
          params: {
            project_id: this.projectId,
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })
        this.projectMembers = response.data.items

        this.meta = response.data.meta

        if (this.projectMembers.length == 0) {
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
          this.projectMembers = []
          this.accessDenied = true
          return
        }
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },
    // Get all members by email
    async getMemberByEmail() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_PROJECT_MEMBER_BY_EMAIL, {
          params: {
            project_id: this.projectId,
            email: this.searchQuery,
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })
        this.projectMembers = response.data.items

        this.meta = response.data.meta

        if (this.projectMembers.length == 0) {
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
          this.projectMembers = []
          this.accessDenied = true
          return
        }
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
      } finally {
        this.loading = false
      }
    },
    // get members by role
    async getMemberByRole() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_PROJECT_MEMBERS_BY_ROLE, {
          params: {
            project_id: this.projectId,
            role: this.searchQuery,
            page: this.meta.page,
            limit: this.meta.limit,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })
        this.projectMembers = response.data.items

        this.meta = response.data.meta

        if (this.projectMembers.length == 0) {
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
          this.projectMembers = []
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
    // Add member
    async addMember(data) {
      /*
            data = {
                email: string,
                projectId: string,
                userId: string,
                role: viewer | editor | admin
            }
            */
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.post(API_ENDPOINTS.ADD_PROJECT_MEMBER, data, {
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
    // Update member
    async updateMember(data) {
      /*
            data = {
                projectId: string,
                userId: string,
                role: viewer | editor | admin
            }
            */
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_PROJECT_MEMBER, data, {
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
    // Delete member
    async deleteMember(data) {
      /*
            data = {
                projectId: string,
                userId: string,
            }
            */
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_PROJECT_MEMBER, {
          data,
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
        return await this.getAllMembers()
      }

      if (this.lastRequest.type === 'all') {
        await this.getAllMembers()
      } else if (this.lastRequest.type === 'email') {
        this.searchQuery = this.lastRequest.query
        await this.getMemberByEmail()
      } else if (this.lastRequest.type === 'role') {
        this.searchQuery = this.lastRequest.query
        await this.getMemberByRole()
      }
    },
  },
})
