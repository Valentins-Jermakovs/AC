// Import Pinia function to define a store
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// User store (used to clear user data on logout)
import { useUserStore } from '@/stores/user'

// Create authentication store
export const useAuthStore = defineStore('auth', {

  // ==========================
  // STATE
  // ==========================
  state: () => ({
    accessToken: null,      // JWT access token (short-lived)
    refreshToken: null,     // JWT refresh token (long-lived)
    isAuthenticated: false, // Indicates if user is logged in
  }),

  // ==========================
  // ACTIONS
  // ==========================
  actions: {

    // --------------------------
    // Login user
    // --------------------------
    async login(username, password) {
      try {
        // Backend expects form-urlencoded format
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        // Send login request
        const response = await api.post(API_ENDPOINTS.LOGIN, formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })

        // Extract tokens from response
        const { access_token, refresh_token } = response.data

        // Save tokens and update state
        this.setAuthData(access_token, refresh_token)

        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    // --------------------------
    // Register new user
    // --------------------------
    async register(username, email, password) {
      try {
        // Send registration request
        const response = await api.post(
          API_ENDPOINTS.REGISTER,
          {
            username,
            email,
            password,
          })

        // Extract tokens
        const { access_token, refresh_token } = response.data

        // Save authentication data
        this.setAuthData(access_token, refresh_token)

        return true
      } catch (error) {
        console.error('Registration error:', error)
        throw error
      }
    },

    // --------------------------
    // Logout user
    // --------------------------
    async logout() {
      try {
        // If refresh token exists, inform backend
        if (this.refreshToken) {
          await api.post(
            API_ENDPOINTS.LOGOUT, null,
            {
              headers: {
                Authorization: `Bearer ${this.refreshToken}`,
              },
            })
        }
      } catch (e) {
        // Even if logout request fails, continue cleanup
        console.warn('Logout failed:', e)
      } finally {
        // Always clear local authentication state
        this.fullReset()
      }
    },

    // --------------------------
    // Refresh access token
    // --------------------------
    async refreshAccessToken() {

      // Send refresh request with refresh token
      const response = await api.post(
        API_ENDPOINTS.TOKEN_REFRESH, null,
        {
          headers: {
            Authorization: `Bearer ${this.refreshToken}`,
          },
        })

      const { access_token, refresh_token } = response.data

      // Update tokens (keep old refresh token if new one not provided)
      this.setAuthData(access_token, refresh_token ?? this.refreshToken)

      return access_token
    },

    // --------------------------
    // Restore tokens from localStorage
    // --------------------------
    loadFromStorage() {
      const access = localStorage.getItem('accessToken')
      const refresh = localStorage.getItem('refreshToken')

      // If both tokens exist, restore authentication state
      if (access && refresh) {
        this.setAuthData(access, refresh)
      }
    },

    // --------------------------
    // Save authentication data
    // --------------------------
    setAuthData(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      this.isAuthenticated = true

      // Persist tokens in browser storage
      localStorage.setItem('accessToken', access)
      localStorage.setItem('refreshToken', refresh)

      // Set default Authorization header for all future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
    },

    // --------------------------
    // Clear authentication data
    // --------------------------
    clearAuthData() {
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false

      // Remove tokens from localStorage
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')

      // Remove Authorization header from axios
      delete api.defaults.headers.common['Authorization']
    },

    // --------------------------
    // Full reset (Auth + User)
    // --------------------------
    fullReset() {

      // Clear authentication state
      this.clearAuthData()

      // Also clear user data from user store
      const userStore = useUserStore()
      userStore.clearUser()
    },
  },
})
