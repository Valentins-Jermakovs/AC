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
        selectedProjectTitle: '',
        selectedProjectStagesCount: 0,

        selectedProjectTasks: {
            total: 0,
            todo: 0,
            inProgress: 0,
            done: 0
        },

        selectedProjectDates: {
            startDate: '',
            endDate: ''
        },
        loading: false,
        error: null
    }),
    actions: {
        async getSelectedProjectData() {
            const authStore = useAuthStore()

            this.loading = true
            this.error = null

            
        }
    }
})