import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

// Create an Axios instance with base URL and credentials
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

// Flag to indicate if token refresh is in progress
let isRefreshing = false
// Queue to hold requests waiting for token refresh
let failedQueue = []

// Process all requests in the queue after refresh
const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error) // Reject request if refresh failed
    } else {
      prom.resolve(token) // Resolve request with new token
    }
  })
  failedQueue = [] // Clear the queue
}

// Axios response interceptor
api.interceptors.response.use(
  (response) => response, // Pass through successful responses
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore() // Get auth store

    if (!error.response) {
      return Promise.reject(error) // Network error
    }

    const status = error.response.status

    // Check if request is for authentication routes
    const isAuthRoute =
      originalRequest.url.includes('/token/refresh') ||
      originalRequest.url.includes('/auth/login') ||
      originalRequest.url.includes('/auth/logout')

    // Handle 401 errors (token expired) and not retrying
    if (status === 401 && !originalRequest._retry && authStore.refreshToken && !isAuthRoute) {
      // If token refresh is already in progress, queue this request
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            // Retry original request with new token
            originalRequest.headers['Authorization'] = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true // Mark request as retried
      isRefreshing = true // Set refresh in progress

      try {
        const newToken = await authStore.refreshAccessToken() // Get new access token

        processQueue(null, newToken) // Resolve all queued requests

        // Retry original request with new token
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`

        return api(originalRequest)
      } catch (err) {
        processQueue(err, null) // Reject all queued requests

        authStore.fullReset() // Clear auth store

        isRefreshing = false

        window.location.replace('/login') // Redirect to login

        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error) // Reject other errors
  },
)
