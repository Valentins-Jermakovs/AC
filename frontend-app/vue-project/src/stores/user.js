import { defineStore } from "pinia";
import { api } from "@/services/axios";
import { API_ENDPOINTS } from "@/config/api";
import { useAuthStore } from "./auth";

export const useUserStore = defineStore("user", {
    state: () => ({
        user: null,
        loading: false,
        error: null,
    }),

    getters: {
        isLoaded: state => !!state.user,
        username: state => state.user?.username || '',
        email: state => state.user?.email || '',
        roles: state => state.user?.roles || [],
    },

    actions: {
        async fetchMe() {
            const authStore = useAuthStore();

            if (!authStore.isAuthenticated) {
                return;
            }

            this.loading = true
            this.error = null

            try {
                const response = await api.get(API_ENDPOINTS.GET_ME)
                this.user = response.data
            } catch (err) {
                console.error('Failed to fetch user:', err)
                this.error = err
                this.user = null
            } finally {
                this.loading = false
            }
        },
        async changeUsername(newUsername) {
            const authStore = useAuthStore();

            if (!authStore.isAuthenticated) {
                this.error = 'User not authenticated';
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await api.put(
                    API_ENDPOINTS.CHANGE_USERNAME,
                    { new_username: newUsername },
                    { headers: { Authorization: `Bearer ${authStore.accessToken}` } }
                );

                this.user = response.data;

                return response.data;
            } catch (err) {
                console.error('Failed to change username:', err);
                this.error = err.response?.data?.detail || err.message || err;
                throw err;
            } finally {
                this.loading = false;
            }
        },
        async changeEmail(newEmail) {
            const authStore = useAuthStore();

            if (!authStore.isAuthenticated) {
                this.error = 'User not authenticated';
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await api.put(
                    API_ENDPOINTS.CHANGE_EMAIL,
                    { new_email: newEmail },
                    { headers: { Authorization: `Bearer ${authStore.accessToken}` } }
                );

                this.user = response.data;

                return response.data;
            } catch (err) {
                console.error('Failed to change email:', err);
                this.error = err.response?.data?.detail || err.message || err;
                throw err;
            } finally {
                this.loading = false;
            }
        },
        async changePassword(newPassword, oldPassword) {
            const authStore = useAuthStore();

            if (!authStore.isAuthenticated) {
                this.error = 'User not authenticated';
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await api.put(
                    API_ENDPOINTS.CHANGE_PASSWORD,
                    { new_password: newPassword, old_password: oldPassword },
                    { headers: { Authorization: `Bearer ${authStore.accessToken}` } }
                );

                this.user = response.data;

                return response.data;
            }
            catch (err) {
                console.error('Failed to change password:', err);
                this.error = err.response?.data?.detail || err.message || err;
                throw err;
            }
            finally {
                this.loading = false;
            }
        },
        clearUser() {
            this.user = null
            this.error = null
            this.loading = false
        },
        clearError() {
            this.error = null
        }
    },
});