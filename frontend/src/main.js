import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import { router } from './router'
import './style.css'
import { setupAxiosInterceptors } from './store.js'

// 初始化 Pinia 并挂载持久化插件
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)

app.use(pinia)
app.use(router)

// 🌟 必须在 app.use(pinia) 之后挂载 Axios 拦截器，因为拦截器内部需要读取 Pinia 状态
setupAxiosInterceptors()

app.mount('#app')