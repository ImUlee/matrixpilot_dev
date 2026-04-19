import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// 🌟 定义 Pinia Store (采用最现代的 Setup 函数风格)
export const useMainStore = defineStore('main', () => {
    // ================= 1. State (状态) =================
    const isLoggedIn = ref(false)
    const lpStats = ref({ unparsed_count: 0, latest_unparsed_sample: "", total_users: 0, total_wins: 0, total_physical_wins: 0, rank_list: [], details: [], history_data: [], date_range: "", all_ranges: [] })
    const mpRecords = ref([])
    const mpItems = ref([])
    const mpSettings = ref({ 
        interval_hours: 72, 
        bark_enabled: false, bark_url: '', bark_title: '', bark_body: '', bark_icon: '', 
        bark_notify_physical: false, bark_physical_title: '', bark_physical_body: '',
        faqList: [], customParsers: [] 
    })
    const nodeList = ref([])
    const clientFiles = ref([])
    const globalNodeFilter = ref('ALL')
    const nowTime = ref(new Date())

    // ================= 2. Getters (计算属性) =================
    const localToday = computed(() => {
        const d = new Date(nowTime.value)
        d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
        return d.toISOString().split('T')[0]
    })

    // ================= 3. Actions (动作与请求) =================
    
    // 登录
    const login = async (pin) => {
        try {
            const res = await axios.post('/login', { pin }, {
                headers: { 'Content-Type': 'application/json' }
            })
            if (res.data.success) {
                isLoggedIn.value = true
                return true
            }
            return false
        } catch (e) {
            console.error('登录失败', e)
            return false
        }
    }
    
    // 登出
    const logout = async () => {
        try {
            await axios.get('/logout')
        } catch (e) {
            // 忽略错误
        }
        isLoggedIn.value = false
    }
    
    // 检查登录状态
    const checkAuth = async () => {
        try {
            const res = await axios.get('/check_auth')
            isLoggedIn.value = res.data.logged_in
        } catch (e) {
            isLoggedIn.value = false
        }
    }

    const fetchMpData = async () => {
        try {
            const res = await axios.get('/api/data')
            mpRecords.value = res.data.records
            mpItems.value = res.data.items
            const s = res.data.settings
            mpSettings.value.interval_hours = s.interval_hours
            mpSettings.value.bark_enabled = s.bark_enabled || false
            mpSettings.value.bark_url = s.bark_url
            mpSettings.value.bark_title = s.bark_title
            mpSettings.value.bark_body = s.bark_body
            mpSettings.value.bark_notify_physical = s.bark_notify_physical
            mpSettings.value.bark_physical_title = s.bark_physical_title || ''
            mpSettings.value.bark_physical_body = s.bark_physical_body || ''
            mpSettings.value.bark_icon = s.bark_icon || (window.location.origin + '/static/icon.png')
            try { mpSettings.value.faqList = s.faq_json ? JSON.parse(s.faq_json) : [] } catch (e) { mpSettings.value.faqList = [] }
            try { mpSettings.value.customParsers = s.parsers_json ? JSON.parse(s.parsers_json) : [] } catch (e) { mpSettings.value.customParsers = [] }
        } catch (e) { console.error("加载全局数据出错", e) }
    }

    const loadLpData = async () => {
        try {
            const res = await axios.get(`/api/stats?device_id=${globalNodeFilter.value}`)
            lpStats.value = res.data
        } catch (e) { console.error("加载大屏数据失败", e) }
    }

    const loadNodes = async () => {
        try {
            const res = await axios.get('/api/nodes')
            nodeList.value = res.data.nodes
        } catch (e) { }
    }

    const fetchClientFiles = async () => {
        try {
            const res = await axios.get('/api/client_files')
            clientFiles.value = res.data.files || []
        } catch (e) { console.error("无法加载客户端列表") }
    }

    // 将所有需要被外部访问的属性和方法 Return 出去
    return {
        isLoggedIn, lpStats, mpRecords, mpItems, mpSettings, nodeList, clientFiles, globalNodeFilter, nowTime,
        localToday, login, logout, checkAuth, fetchMpData, loadLpData, loadNodes, fetchClientFiles
    }
}, {
    // 🌟 魔法配置：开启持久化！刷新浏览器后，选中的节点筛选器将自动恢复！
    persist: {
        paths: ['globalNodeFilter', 'isLoggedIn']
    }
})

// ================= 4. 全局网络与鉴权拦截器 =================
export const setupAxiosInterceptors = () => {
    // 彻底移除了 Request 时的 loading 拦截，让所有请求 100% 静默
    axios.interceptors.response.use(
        response => response,
        error => {
            // 只保留关键的鉴权防御：如果后端返回 401 Session 过期，则踢回登录页
            if (error.response && error.response.status === 401) {
                alert("登录已失效或在别处被挤下线，请重新验证");
                window.location.href = '/login';
            }
            return Promise.reject(error);
        }
    );
}

// ================= 5. 纯净工具函数 =================
export const getLocalISOTime = () => {
    const d = new Date()
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
    return d.toISOString().slice(0, 16)
}

export const formatShortDate = (dateStr) => {
    if (!dateStr) return ''
    const cleanStr = dateStr.trim()
    const parts = cleanStr.split(' ')
    if (parts.length >= 2) return `${parts[0].replace(/-/g, '/').substring(5)} ${parts[1].substring(0, 5)}`
    return cleanStr
}