import { createApp } from 'vue'
import App from './App.vue'
import 'materialize-css/dist/js/materialize.min'

import router from './router'

createApp(App).use(router).mount('#app')
