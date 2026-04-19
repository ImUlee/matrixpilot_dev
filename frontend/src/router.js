import { createRouter, createWebHashHistory } from 'vue-router'
import { useMainStore } from './store'

// 路由配置
const routes = [
    { path: '/', redirect: '/overview' },
    { path: '/login', component: () => import('./views/Login.vue'), meta: { public: true } },
    { path: '/search', component: () => import('./views/Search.vue'), meta: { public: true } },
    { path: '/overview', component: () => import('./views/Overview.vue') },
    { path: '/details', component: () => import('./views/LogDetails.vue') },
    { path: '/history', component: () => import('./views/History.vue') },
    { path: '/logs', component: () => import('./views/MpLogs.vue') },
    { path: '/settings', component: () => import('./views/Settings.vue') }
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes
})

// 路由守卫 - 认证检查
router.beforeEach((to, from, next) => {
    const store = useMainStore()
    
    // 公共页面不需要认证
    if (to.meta.public) {
        return next()
    }
    
    // 需要认证的页面
    if (!store.isLoggedIn) {
        return next('/login')
    }
    
    next()
})