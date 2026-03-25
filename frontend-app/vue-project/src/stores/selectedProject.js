// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from './auth'

// Create store
export const useSelectedProjectStore = defineStore('selectedProject', {
    state: () => ({
        totalProjects: 0,
        
        selectedProject: null,

        selectedProjectStagesCount: 0,

        selectedProjectTasks: {
            total: 0,
            todo: 0,
            inProgress: 0,
            done: 0
        },

        selectedProjectDates: null,
        loading: false,
        error: null
    }),
    actions: {
        async getSelectedProjectData() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_SELECTED_PROJECT, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                this.selectedProject = response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        },
        async getSelectedProjectStagesCount() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_SELECTED_PROJECT_STAGES_COUNT, {
                    params: { projectId: this.selectedProject.workspaceId },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                this.selectedProjectStagesCount = response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        },
        async getSelectedProjectDateRange() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_PROJECT_DATE_RANGE, {
                    params: { projectId: this.selectedProject.workspaceId },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                this.selectedProjectDates = response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        },
        async getSelectedProjectTasksCount() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_PROJECT_TASKS_STATS, {
                    params: { projectId: this.selectedProject.workspaceId },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })

                this.selectedProjectTasks = response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        }
    }
})