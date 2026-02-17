// Import Pinia function to define a store
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used to check authentication and get token)
import { useAuthStore } from './auth'

// Create Pinia store for user data
export const useUserStore = defineStore('user', {

  // ==========================
  // STATE
  // ==========================
  state: () => ({
    user: null,      // Stores current user object
    loading: false,  // Indicates if request is in progress
    error: null,     // Stores error message (if any)
  }),

  // ==========================
  // GETTERS (Computed values)
  // ==========================
  getters: {

    // Returns true if user data is loaded
    isLoaded: (state) => !!state.user,

    // Safely return username (empty string if user is null)
    username: (state) => state.user?.username || '',

    // Safely return email
    email: (state) => state.user?.email || '',

    // Return roles array (empty array if not defined)
    roles: (state) => state.user?.roles || [],

    // Check if user has admin role
    isAdmin: (state) => state.user?.roles.includes('admin') || false,
  },

  // ==========================
  // ACTIONS (Async logic)
  // ==========================
  actions: {

    // Fetch current authenticated user from backend
    async fetchMe() {
      const authStore = useAuthStore()

      // Stop if user is not authenticated
      if (!authStore.isAuthenticated) {
        return
      }

      this.loading = true
      this.error = null

      try {
        // Send GET request to backend
        const response = await api.get(API_ENDPOINTS.GET_ME)

        // Save user data in store
        this.user = response.data

      } catch (err) {
        console.error('Failed to fetch user:', err)

        this.error = err
        this.user = null

      } finally {
        this.loading = false
      }
    },

    // Change username
    async changeUsername(newUsername) {
      const authStore = useAuthStore()

      if (!authStore.isAuthenticated) {
        this.error = 'User not authenticated'
        return
      }

      this.loading = true
      this.error = null

      try {
        // Send PUT request with new username
        const response = await api.put(
          API_ENDPOINTS.CHANGE_USERNAME,
          { new_username: newUsername },
          { headers: { Authorization: `Bearer ${authStore.accessToken}` } },
        )

        // Update local user data
        this.user = response.data

        return response.data

      } catch (err) {
        console.error('Failed to change username:', err)

        // Extract readable error message if possible
        this.error = err.response?.data?.detail || err.message || err

        throw err

      } finally {
        this.loading = false
      }
    },

    // Change email
    async changeEmail(newEmail) {
      const authStore = useAuthStore()

      if (!authStore.isAuthenticated) {
        this.error = 'User not authenticated'
        return
      }

      this.loading = true
      this.error = null

      try {
        // Send PUT request with new email
        const response = await api.put(
          API_ENDPOINTS.CHANGE_EMAIL,
          { new_email: newEmail },
          { headers: { Authorization: `Bearer ${authStore.accessToken}` } },
        )

        this.user = response.data

        return response.data

      } catch (err) {
        console.error('Failed to change email:', err)

        this.error = err.response?.data?.detail || err.message || err

        throw err

      } finally {
        this.loading = false
      }
    },

    // Change password
    async changePassword(newPassword, oldPassword) {
      const authStore = useAuthStore()

      if (!authStore.isAuthenticated) {
        this.error = 'User not authenticated'
        return
      }

      this.loading = true
      this.error = null

      try {
        // Send PUT request with old and new password
        const response = await api.put(
          API_ENDPOINTS.CHANGE_PASSWORD,
          { new_password: newPassword, old_password: oldPassword },
          { headers: { Authorization: `Bearer ${authStore.accessToken}` } },
        )

        this.user = response.data

        return response.data

      } catch (err) {
        console.error('Failed to change password:', err)

        this.error = err.response?.data?.detail || err.message || err

        throw err

      } finally {
        this.loading = false
      }
    },

    // Clear all user data (used on logout)
    clearUser() {
      this.user = null
      this.error = null
      this.loading = false
    },

    // Clear only error message
    clearError() {
      this.error = null
    },
  },
})
