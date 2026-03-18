// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth store (used for token)
import { useAuthStore } from '../auth'

// Create store
export const useWorkspaceProjectStagesStore = defineStore('workspaceProjectStages', {
    state: () => ({
        projectStages: [],
        loading: false,
        error: null,
        projectId: null,
    }),
    // ===========
    // GETTERS
    // ===========
    getters: {
        hasStages() {
            return this.projectStages.length > 0
        },
        getStageById(id) {
            return this.projectStages.find((stage) => stage.id === id)
        }
    },
    // ==========================
    // ACTIONS
    // ==========================
    actions: {
        // ==========================
        // GET
        // ==========================
        async getStages() {
            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.get(API_ENDPOINTS.GET_ALL_PROJECT_STAGES, {
                    params: {
                        project_id: this.projectId,
                    },
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                this.projectStages = response.data.items
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
        // Create stage
        async createStage(data) {
            /*
            data = {
                description: string,
                dueDate: string,
                projectId: string,
                title: string
            }
            */

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.post(API_ENDPOINTS.CREATE_PROJECT_STAGE, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                await this.getStages()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },
        // Create stage relative
        async createStageRelative(data) {
            /*
            data = {
                description: string,
                dueDate: string,
                position: before | after,
                projectId: string,
                referenceStageId: string,
                title: string
            }
            */

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.post(API_ENDPOINTS.CREATE_PROJECT_STAGE_RELATIVE, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                await this.getStages()
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
        // Update stage
        async updateStage(data) {
            /*
            data = {
                description: string,
                dueDate: string,
                projectId: string,
                stageId: string,
                title: string
            }
            */

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.put(API_ENDPOINTS.UPDATE_PROJECT_STAGE, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                await this.getStages()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },
        // move stage
        async moveStage(data) {
            /*
            data = {
                projectId: string,
                stageId: string,
                direction: up | down
            }
            */

            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.put(API_ENDPOINTS.MOVE_PROJECT_STAGE, data, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                await this.getStages()
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
        // Delete stage
        async deleteStage(data) {
            /*
            data = {
                projectId: string,
                stageId: string,
            }
            */
            this.loading = true
            this.error = null
            const authStore = useAuthStore()

            try {
                const response = await api.delete(API_ENDPOINTS.DELETE_PROJECT_STAGE, {
                    data,
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                    },
                })
                await this.getStages()
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