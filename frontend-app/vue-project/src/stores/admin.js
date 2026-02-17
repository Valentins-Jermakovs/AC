import { defineStore } from 'pinia'
import { api } from '@/services/axios'
import { API_ENDPOINTS } from '@/config/api'
import { useAuthStore } from './auth'
import { useUserStore } from './user'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [],
    meta: {
      page: 1,
      limit: 10,
      total_users: 0,
      total_pages: 0,
    },
    loading: false,
    error: null,
    searchMode: 'all',
    searchQuery: '',

    lastRequest: null,
  }),

  getters: {
    hasUsers: (state) => state.users.length > 0,
  },

  actions: {
    async fetchUsers(page = this.meta.page, limit = this.meta.limit) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

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

        this.users = response.data.items
        this.meta = response.data.meta

        this.lastRequest = {
          type: 'all',
        }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

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

        this.users = [response.data]

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
        // endpoint ar path param + query param
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

    async getUserByRole(searchString, page = this.meta.page, limit = this.meta.limit) {
      const authStore = useAuthStore()
      const userStore = useUserStore()

      if (!userStore.isAdmin) {
        this.error = 'You are not an admin'
        return
      }

      this.loading = true
      this.error = null

      this.lastRequest = {
        type: 'role',
        payload: searchString,
      }

      try {
        // endpoint ar path param + query param
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
        const response = await api.post(API_ENDPOINTS.ADD_ROLES_TO_USER, selectedUserIds, {
          params: { role_id: roleId },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        console.log('Role added:', response.data)
        return response.data
      } catch (err) {
        console.error('Failed to add role:', err)
        this.error = err.response?.data?.detail || err.message || err
        throw err
      } finally {
        this.loading = false
      }
    },

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
          `${API_ENDPOINTS.REMOVE_ROLES_FROM_USER}?role_id=${roleId}`,
          selectedUserIds,
          {
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        console.log('Role removed:', response.data)
        return response.data
      } catch (err) {
        console.error('Failed to remove role:', err)
        this.error = err.response?.data?.detail || err.message || err
        throw err
      } finally {
        this.loading = false
      }
    },

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
          `${API_ENDPOINTS.CHANGE_USER_ACTIVITY}?is_active=${isActive}`,
          userIds,
          {
            headers: { Authorization: `Bearer ${authStore.accessToken}` },
          },
        )

        console.log('User activity updated:', response.data)
        return response.data
      } catch (err) {
        console.error('Failed to update user activity:', err)
        this.error = err.response?.data?.detail || err.message || err
        throw err
      } finally {
        this.loading = false
      }
    },

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

    clearSearch() {
      this.searchQuery = ''
    },
  },
})
