import { createRouter, createWebHistory } from 'vue-router'

import LandingView from '@/views/LandingView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import LogoutView from '@/views/LogoutView.vue'

import EmailRedirectView from '@/views/EmailRedirectView.vue'

import SystemView from '@/views/SystemView.vue'
import CabinetView from '@/views/system/CabinetView.vue'
import CalendarView from '@/views/system/CalendarView.vue'
import NewsView from '@/views/system/NewsView.vue'
import NotificationsView from '@/views/system/NotificationsView.vue'
import PomodoroView from '@/views/system/PomodoroView.vue'
import DataAnalyzerView from '@/views/system/DataAnalyzerView.vue'
import WorkView from '@/views/system/WorkView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
    {
      path: '/system',
      name: 'system',
      component: SystemView,
      meta: {
        requiresAuth: true,
      },
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
    {
      path: '/email-redirect',
      name: 'email-redirect',
      component: EmailRedirectView,
      meta: { hidden: true },
    },
  ],
})

import { useAuthStore } from '@/stores/auth'

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.isAuthenticated) {
    authStore.loadFromStorage()
  }

  const publicPages = ['landing', 'login', 'register']
  const authRequired = to.meta.requiresAuth

  if (authRequired && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }

  if (authStore.isAuthenticated && publicPages.includes(to.name)) {
    return next({ name: 'cabinet' })
  }

  if (
    to.name === 'email-redirect' &&
    !from.path.startsWith('/system')
  ) {
    return next({ name: 'landing' })
  }

  next()
})


export default router
