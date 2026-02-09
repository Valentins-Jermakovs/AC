import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// import './assets/global.css'
import '@/assets/global.css'

app.use(createPinia())
app.use(router)

app.mount('#app')
