import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8080' // Nginx URL
axios.defaults.withCredentials = true // ja backend izmanto cookies


import App from './App.vue'
import router from './router'

import '@/assets/styles/global.css'

/* add fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import all the icons in Free Solid, Free Regular, and Brands styles */
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

library.add(fas, far, fab)

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
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
