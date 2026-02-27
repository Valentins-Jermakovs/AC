// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth and User stores (used for token and role checking)
import { useAuthStore } from './auth'
import { useUserStore } from './user'

// Create Admin store
export const useAdminStore = defineStore('admin', {

  // ==========================
  // STATE
  // ==========================
  state: () => ({
    users: [], // List of users returned from backend

    // Pagination metadata
    meta: {
      page: 1,
      limit: 10,
      total_users: 0,
      total_pages: 0,
    },

    loading: false, // Indicates request is in progress
    error: null,    // Stores error message

    // Search configuration
    searchMode: 'all',
    searchQuery: '',

    // Stores information about last request (used for refresh)
    lastRequest: null,
  }),

  // ==========================
  // GETTERS
  // ==========================
  getters: {

    // Returns true if users array is not empty
    hasUsers: (state) => state.users.length > 0,
  },

  // ==========================
  // ACTIONS
  // ==========================
  actions: {

    // --------------------------
    // Fetch all users (paginated)
    // --------------------------
    async fetchUsers(page = this.meta.page, limit = this.meta.limit) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      // Only admins can access this
      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_USERS, {
          params: { page, limit },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        // Save users and pagination data
        this.users = response.data.items
        this.meta = response.data.meta

        // Remember request type
        this.lastRequest = { type: 'all' }

      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Get single user by ID
    // --------------------------
    async getUserById(id) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await api.get(API_ENDPOINTS.GET_USER_BY_ID(id), {
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        })

        // Store result as single-item array
        this.users = [response.data]

        // Save pagination data
        this.meta = {
          page: 1,
          total_users: 1,
          total_pages: 1,
        }

        this.lastRequest = {
          type: 'id',
          payload: id,
        }

      } catch (err) {
        this.users = []
        this.error = err.response?.data?.detail || err.message
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Search user by username or email
    // --------------------------
    async getUserByNameEmail(searchString, page = this.meta.page, limit = this.meta.limit) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await api.get(
          API_ENDPOINTS.GET_USER_BY_USERNAME_OR_EMAIL(encodeURIComponent(searchString)),
          {
            params: { page, limit },
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        this.users = response.data.items
        this.meta = response.data.meta

        this.lastRequest = {
          type: 'username',
          payload: searchString,
        }

      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        this.users = []

        // Reset pagination
        this.meta = {
          page: 1,
          limit: 10,
          total_users: 0,
          total_pages: 0,
        }
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Search users by role
    // --------------------------
    async getUserByRole(searchString, page = this.meta.page, limit = this.meta.limit) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      // Save request before execution
      this.lastRequest = {
        type: 'role',
        payload: searchString,
      }

      try {
        const response = await api.get(
          API_ENDPOINTS.GET_USER_BY_ROLE(encodeURIComponent(searchString)),
          {
            params: { page, limit },
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        this.users = response.data.items
        this.meta = response.data.meta

      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        this.users = []

        this.meta = {
          page: 1,
          limit: 10,
          total_users: 0,
          total_pages: 0,
        }
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Add role to selected users
    // --------------------------
    async addRoleToSelectedUsers(roleId, selectedUserIds) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await api.post(
          API_ENDPOINTS.ADD_ROLES_TO_USER,
          {
            role_id: roleId,
            user_ids: selectedUserIds
          },
          {
            headers: {
              Authorization: `Bearer ${authStore.accessToken}`
            }
          }
        )

        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || err
        throw err
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Remove role from selected users
    // --------------------------
    async removeRoleFromSelectedUsers(roleId, selectedUserIds) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await api.post(
          API_ENDPOINTS.REMOVE_ROLES_FROM_USER,
          {
            role_id: roleId,
            user_ids: selectedUserIds
          },
          {
            headers: {
              Authorization: `Bearer ${authStore.accessToken}`
            }
          }
        )

        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || err
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Activate or deactivate users
    // --------------------------
    async updateUserActivity(userIds, status) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      try {
        const isActive = status === 'active'

        const response = await api.put(
          API_ENDPOINTS.CHANGE_USER_ACTIVITY,
          {
            user_ids: userIds,
            is_active: isActive
          },
          {
            headers: {
              Authorization: `Bearer ${authStore.accessToken}`
            }
          }
        )


        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || err
        throw err
      } finally {
        this.loading = false
      }
    },

    // --------------------------
    // Pagination helpers
    // --------------------------
    async setPage(page) {
      this.meta.page = page
      await this.fetchUsers(page, this.meta.limit)
    },

    async setLimit(limit) {
      this.meta.limit = limit
      this.meta.page = 1
    },

    async nextPage() {
      if (this.meta.page < this.meta.total_pages) {
        this.meta.page++
        await this.fetchUsers(this.meta.page, this.meta.limit)
      }
    },

    async prevPage() {
      if (this.meta.page > 1) {
        this.meta.page--
        await this.fetchUsers(this.meta.page, this.meta.limit)
      }
    },

    // --------------------------
    // Repeat last request
    // --------------------------
    async refresh() {
      if (!this.lastRequest) {
        await this.fetchUsers()
        return
      }

      const { type, payload } = this.lastRequest

      switch (type) {
        case 'all':
          await this.fetchUsers()
          break

        case 'id':
          await this.getUserById(payload)
          break

        case 'username':
          await this.getUserByNameEmail(payload)
          break

        case 'role':
          await this.getUserByRole(payload)
          break

        default:
          await this.fetchUsers()
      }
    },

    // Clear search input field
    clearSearch() {
      this.searchQuery = ''
    },
  },
})
