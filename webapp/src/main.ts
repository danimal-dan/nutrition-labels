import 'primevue/resources/themes/lara-dark-pink/theme.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'

import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'

const app = createApp(App)

app.use(PrimeVue)
app.use(ToastService)

app.mount('#app')
