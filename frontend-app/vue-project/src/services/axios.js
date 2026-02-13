import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    if (!error.response) {
      return Promise.reject(error)
    }

    const status = error.response.status

    const isAuthRoute =
      originalRequest.url.includes('/token/refresh') ||
      originalRequest.url.includes('/auth/login') ||
      originalRequest.url.includes('/auth/logout')

    if (status === 401 && !originalRequest._retry && authStore.refreshToken && !isAuthRoute) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const newToken = await authStore.refreshAccessToken()

        processQueue(null, newToken)

        originalRequest.headers['Authorization'] = `Bearer ${newToken}`

        return api(originalRequest)
      } catch (err) {
        processQueue(err, null)

        authStore.fullReset()

        isRefreshing = false

        window.location.replace('/login')

        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  },
)
