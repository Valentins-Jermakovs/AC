// Import Vue Router functions
import { createRouter, createWebHistory } from 'vue-router'

// ==========================
// Public Views
// ==========================
import LandingView from '@/views/landing/LandingView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'

import EmailRedirectView from '@/views/common/EmailRedirectView.vue'
import NotFoundView from '@/views/errors/NotFoundView.vue'

// ==========================
// System (Authenticated) Views
// ==========================
import SystemView from '@/views/system/SystemView.vue'
import CabinetView from '@/views/system/CabinetView.vue'
import CalendarView from '@/views/system/CalendarView.vue'
import NewsView from '@/views/system/NewsView.vue'
import NotificationsView from '@/views/system/NotificationsView.vue'
import PomodoroView from '@/views/system/PomodoroView.vue'
import DataAnalyzerView from '@/views/system/DataAnalyzerView.vue'
import WorkView from '@/views/system/WorkView.vue'

// ==========================
// Router Configuration
// ==========================

const router = createRouter({
  // Use HTML5 history mode
  history: createWebHistory(import.meta.env.BASE_URL),

  // Application routes
  routes: [

    // --------------------------
    // Public Routes
    // --------------------------

    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView,
    },

    // --------------------------
    // Catch-all Route (404)
    // Must be placed before dynamic routes if needed
    // --------------------------
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView,
    },

    // --------------------------
    // Protected System Routes
    // --------------------------
    {
      path: '/system',
      name: 'system',
      component: SystemView,

      // This route requires authentication
      meta: {
        requiresAuth: true,
      },

      // Nested routes (rendered inside <router-view> of SystemView)
      children: [

        {
          path: '',
          name: 'cabinet',
          component: CabinetView,
          meta: {
            title: 'Cabinet',
          },
        },
        {
          path: 'calendar',
          name: 'calendar',
          component: CalendarView,
          meta: {
            title: 'Calendar',
          },
        },
        {
          path: 'news',
          name: 'news',
          component: NewsView,
          meta: {
            title: 'News',
          },
        },
        {
          path: 'notifications',
          name: 'notifications',
          component: NotificationsView,
          meta: {
            title: 'Notifications',
          },
        },
        {
          path: 'pomodoro',
          name: 'pomodoro',
          component: PomodoroView,
          meta: {
            title: 'Pomodoro',
          },
        },
        {
          path: 'data-analyzer',
          name: 'data-analyzer',
          component: DataAnalyzerView,
          meta: {
            title: 'Data Analyzer',
          },
        },
        {
          path: 'work',
          name: 'work',
          component: WorkView,
          meta: {
            title: 'Work',
          },
        },
      ],
    },

    // --------------------------
    // Email Redirect Route
    // --------------------------
    {
      path: '/email-redirect',
      name: 'email-redirect',
      component: EmailRedirectView,

      // This route is hidden from navigation menus
      meta: { hidden: true },
    },
  ],
})

// ==========================
// Navigation Guard
// ==========================

import { useAuthStore } from '@/stores/auth'

// Global route guard
// This runs before every route change
router.beforeEach((to, from, next) => {

  // Get authentication store
  const authStore = useAuthStore()

  // If auth state is not loaded, restore it from localStorage
  if (!authStore.isAuthenticated) {
    authStore.loadFromStorage()
  }

  // Define public pages (accessible without login)
  const publicPages = ['landing', 'login', 'register']

  // Check if route requires authentication
  const authRequired = to.meta.requiresAuth

  // If authentication is required and user is NOT logged in
  if (authRequired && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }

  // If user is already logged in and tries to access public pages
  // Redirect to main cabinet page
  if (authStore.isAuthenticated && publicPages.includes(to.name)) {
    return next({ name: 'cabinet' })
  }

  // Otherwise allow navigation
  next()
})

// Export router
export default router
