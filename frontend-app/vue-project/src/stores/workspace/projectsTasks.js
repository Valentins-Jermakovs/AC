// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useWorkspaceProjectsTasksStore = defineStore('workspaceProjectsTasks', {
  state: () => ({
    tasks: [],
    loading: false,
    error: null,
    stageId: null,
    projectId: null,
  }),
  // ===========
  // GETTERS
  // ===========
  getters: {
    hasTasks() {
      return this.tasks.length > 0
    },
    getTaskById(id) {
      return this.tasks.find((task) => task.id === id)
    },
  },
  // ==========================
  // ACTIONS
  // ==========================
  actions: {
    // ==========================
    // GET
    // ==========================
    async getTasks() {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.get(API_ENDPOINTS.GET_PROJECT_TASKS, {
          params: {
            project_id: this.projectId,
            stage_id: this.stageId,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })
        this.tasks = response.data.items
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    // ==========================
    // POST
    // ==========================
    async createTask(data) {
      /*
            data = {
                "description": "New task description - optional",
                "dueDate": "2026-01-01",
                "priority": 1,
                "projectId": "projectId",
                "stageId": "stageId",
                "status": "todo",
                "storyPoints": 1,
                "title": "New task"
            }
            */

      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.post(API_ENDPOINTS.CREATE_PROJECT_TASK, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.getTasks()
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
    async updateTask(data) {
      /*
            data = {
                "description": "New task description - optional",
                "dueDate": "2026-01-01",
                "priority": 1,
                "projectId": "project_id",
                "status": "todo",
                "storyPoints": 1,
                "taskId": "task_id",
                "title": "New task"
                }
            */

      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_PROJECT_TASK, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })
        await this.getTasks()
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
    async deleteTask(data) {
      /*
            data = {
                "projectId": "project_id",
                "taskId": "task_id",
            }
            */
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_PROJECT_TASK, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
          data,
        })
        await this.getTasks()
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
