import 'primevue/resources/themes/lara-dark-pink/theme.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'

import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'

const app = createApp(App)

app.use(PrimeVue)

app.mount('#app')
