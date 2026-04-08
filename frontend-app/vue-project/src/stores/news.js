// Import Pinia store helper
import { defineStore } from 'pinia'

// Axios instance for API requests
import { api } from '@/services/axios'

// API endpoint constants
import { API_ENDPOINTS } from '@/config/api'

// Auth and User stores (used for token and role checking)
import { useAuthStore } from './auth'

export const useNewsStore = defineStore('news', {
    state: () => ({
        news: [],
        selectedNews: null,
        loading: false,
        error: null,
        searchQuery: '',

        meta: {
            page: 1,
            limit: 10,
            total_news: 0,
            total_pages: 0,
        }
    }),

    actions: {
        async getAllNews() {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_ALL_NEWS, {
                    params: {
                        page: this.meta.page,
                        limit: this.meta.limit,
                        query: this.searchQuery
                    },
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                this.news = response.data.data
                this.meta = response.data.meta || {
                    page: 1,
                    limit: 10,
                    total_news: 0,
                    total_pages: 0,
                }
            } catch (error) {
                this.error = error.response?.data?.detail || error.message || 'Something went wrong'
            } finally {
                this.loading = false
            }
        },
        async createNews(data) {
            /*
            data:
            {
                "authorEmail": "2V2E3@example.com",
                "content": "News content",
                "coverImage": "https://example.com/image.jpg",
                "status": "draft",
                "tags": [
                    "tag1",
                    "tag2"
                ],
                "title": "News title"
            }
            */
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.post(API_ENDPOINTS.CREATE_NEWS, data, {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                await this.getAllNews()
                return response.data
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },
        async updateNews(data) {
            /*
            data:
            {
                "authorEmail": "2V2E3@example.com",
                "content": "News content",
                "coverImage": "https://example.com/image.jpg",
                "status": "draft",
                "tags": [
                    "tag1",
                    "tag2"
                ],
                "title": "News title",
                "newsId": 1
            }
            */
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.put(API_ENDPOINTS.UPDATE_NEWS, data, {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                await this.getAllNews()
                this.selectedNews = {
                    content: data.content,
                    coverImage: data.coverImage,
                    status: data.status,
                    tags: data.tags,
                    title: data.title,
                    id: data.newsId
                }
                
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },
        async deleteNews(newsId) {
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            try {
                const response = await api.delete(API_ENDPOINTS.DELETE_NEWS(newsId), {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` },
                })

                await this.getAllNews()
            } catch (err) {
                this.error = err.response?.data?.detail || err.message || 'Something went wrong'
                throw err
            } finally {
                this.loading = false
            }
        },
        // --------------------------
        // Pagination
        // --------------------------
        async setPage(page) {
            this.meta.page = page
            await this.getAllNews()
        },

        async setLimit(limit) {
            this.meta.limit = limit
            this.meta.page = 1
            await this.getAllNews()
        },

        async nextPage() {
            if (this.meta.page < this.meta.total_pages) {
                this.meta.page++
                await this.getAllNews()
            }
        },

        async prevPage() {
            if (this.meta.page > 1) {
                this.meta.page--
                await this.getAllNews()
            }
        },
    }
})