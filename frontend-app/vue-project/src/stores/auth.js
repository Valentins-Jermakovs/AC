import { defineStore } from 'pinia'
import { api } from '@/services/axios'
import { API_ENDPOINTS } from '@/config/api'
import { useUserStore } from '@/stores/user'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
  }),

  actions: {
    async login(username, password) {
      try {
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        const response = await api.post(API_ENDPOINTS.LOGIN, formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })

        const { access_token, refresh_token } = response.data

        this.setAuthData(access_token, refresh_token)

        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    async register(username, email, password) {
      try {
        const response = await api.post(API_ENDPOINTS.REGISTER, {
          username,
          email,
          password,
        })

        const { access_token, refresh_token } = response.data

        this.setAuthData(access_token, refresh_token)

        return true
      } catch (error) {
        console.error('Registration error:', error)
        throw error
      }
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await api.post(API_ENDPOINTS.LOGOUT, null, {
            headers: {
              Authorization: `Bearer ${this.refreshToken}`,
            },
          })
        }
      } catch (e) {
        console.warn('Logout failed:', e)
      } finally {
        this.fullReset()
      }
    },

    async refreshAccessToken() {
      const response = await api.post(API_ENDPOINTS.TOKEN_REFRESH, null, {
        headers: {
          Authorization: `Bearer ${this.refreshToken}`,
        },
      })

      const { access_token, refresh_token } = response.data

      this.setAuthData(access_token, refresh_token ?? this.refreshToken)

      return access_token
    },

    loadFromStorage() {
      const access = localStorage.getItem('accessToken')
      const refresh = localStorage.getItem('refreshToken')

      if (access && refresh) {
        this.setAuthData(access, refresh)
      }
    },

    setAuthData(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      this.isAuthenticated = true

      localStorage.setItem('accessToken', access)
      localStorage.setItem('refreshToken', refresh)

      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
    },

    clearAuthData() {
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false

      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')

      delete api.defaults.headers.common['Authorization']
    },

    fullReset() {
      this.clearAuthData()

      const userStore = useUserStore()
      userStore.clearUser()
    },
  },
})
