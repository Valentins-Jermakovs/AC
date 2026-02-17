// Import Vue core
import { createApp } from 'vue'

// Import Pinia (state management)
import { createPinia } from 'pinia'

// Import Vue I18n for translations
import { createI18n } from 'vue-i18n'

// Import FontAwesome Vue component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Import main App component
import App from './App.vue'

// Import router instance
import router from './router'

// Import global CSS
import '@/assets/styles/global.css'

// --------------------------
// FontAwesome setup
// --------------------------

// Import the library core
import { library } from '@fortawesome/fontawesome-svg-core'

// Import icon packs
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

// Add all imported icons to the library
library.add(fas, far, fab)

// --------------------------
// Translations / i18n
// --------------------------
import en from '@/i18n/en.json'
import lv from '@/i18n/lv.json'
import ru from '@/i18n/ru.json'

// Create i18n instance
const i18n = createI18n({
  legacy: false,          // Use Composition API style (Vue 3)
  locale: 'lv',            // Default locale
  fallbackLocale: 'en',    // Fallback if translation missing
  messages: {
    en,
    lv,
    ru,
  },
})

// --------------------------
// Create Vue app
// --------------------------
const app = createApp(App)

// Install Pinia
app.use(createPinia())

// Install router
app.use(router)

// Install i18n
app.use(i18n)

// Register global FontAwesome component
app.component('font-awesome-icon', FontAwesomeIcon)

// Mount app to DOM
app.mount('#app')
