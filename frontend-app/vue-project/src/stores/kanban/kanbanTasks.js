// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useKanbanTasksStore = defineStore('kanbanTasks', {
  // ==========
  // STATE
  // ==========
  state: () => ({
    tasks: [],
    loading: false,
    error: null,
    stageId: null,
    boardId: null,
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
    async getKanbanTasks() {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.get(API_ENDPOINTS.GET_KANBAN_TASKS, {
          params: {
            board_id: this.boardId,
            stage_id: this.stageId,
          },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        // Save tasks and pagination data
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
    async createKanbanTask(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.post(API_ENDPOINTS.CREATE_KANBAN_TASK, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.getKanbanTasks()
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
    async updateKanbanTask(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.UPDATE_KANBAN_TASK, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.getKanbanTasks()
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    async moveKanbanTaskInStage(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.MOVE_KANBAN_TASK_IN_STAGE, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.getKanbanTasks()
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Something went wrong'
        throw err
      } finally {
        this.loading = false
      }
    },
    async moveKanbanTaskBetweenStages(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.put(API_ENDPOINTS.MOVE_KANBAN_TASK_BETWEEN_STAGES, data, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        })

        await this.getKanbanTasks()
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
    async deleteKanbanTask(data) {
      this.loading = true
      this.error = null
      const authStore = useAuthStore()

      try {
        const response = await api.delete(API_ENDPOINTS.DELETE_KANBAN_TASK, {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
          data: {
            boardId: data.boardId,
            taskId: data.taskId,
          },
        })

        await this.getKanbanTasks()
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
