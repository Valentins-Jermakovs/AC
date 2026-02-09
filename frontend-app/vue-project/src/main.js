import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router'

import '@/assets/global.css'

// translations
import en from '@/i18n/en.json'
import lv from '@/i18n/lv.json'
import ru from '@/i18n/ru.json'

const i18n = createI18n({
  legacy: false,          // IMPORTANT for Vue 3
  locale: 'lv',
  fallbackLocale: 'en',
  messages: {
    en,
    lv,
    ru,
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')
