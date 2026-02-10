import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {

  state: () => ({
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false
  }),

  actions: {
    async login(username, password) {
      try {
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          withCredentials: true
        })

        const { access_token, refresh_token } = response.data

        this.accessToken = access_token
        this.refreshToken = refresh_token
        this.isAuthenticated = true

        // Save tokens to local storage
        localStorage.setItem('accessToken', access_token)
        localStorage.setItem('refreshToken', refresh_token)

        // Axios default header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

        return true

      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    async register(username, email, password) {
        try {
            const payload = {
                username,
                email,
                password
            }

            const response = await axios.post('/auth/register', payload, {
                headers: {
                    'Content-Type': 'application/json'
                },
                withCredentials: true
            });

            const { access_token, refresh_token } = response.data;

            this.accessToken = access_token;
            this.refreshToken = refresh_token;
            this.isAuthenticated = true;

            // Save tokens to local storage
            localStorage.setItem('accessToken', access_token);
            localStorage.setItem('refreshToken', refresh_token);

            // Axios default header
            axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

            return true;
        }    
        catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await axios.post('/auth/logout', null, {
            headers: {
              Authorization: `Bearer ${this.refreshToken}`
            }
          })
        }

      } catch (e) {
        console.warn('Logout failed:', e)
      } finally {
        this.accessToken = null
        this.refreshToken = null
        this.isAuthenticated = false
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    loadFromStorage() {
      const access = localStorage.getItem('accessToken')
      const refresh = localStorage.getItem('refreshToken')
      if (access && refresh) {
        this.accessToken = access
        this.refreshToken = refresh
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
      }
    }
  }
})
