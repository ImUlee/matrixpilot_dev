<template>
  <div class="app-wrapper">
    <div id="dynamic-top-mask" class="top-blur-mask"></div>

    <nav class="bottom-nav" v-show="showNav">
        <div class="nav-tabs-c">
            <router-link to="/overview" class="nav-item-c" active-class="active">
                <ion-icon :name="$route.path.includes('/overview') ? 'pulse' : 'pulse-outline'" class="nav-icon"></ion-icon>
                <div class="nav-indicator"></div>
            </router-link>
            <router-link to="/details" class="nav-item-c" active-class="active">
                <ion-icon :name="$route.path.includes('/details') ? 'list' : 'list-outline'" class="nav-icon"></ion-icon>
                <div class="nav-indicator"></div>
            </router-link>
            <router-link to="/history" class="nav-item-c" active-class="active">
                <ion-icon :name="$route.path.includes('/history') ? 'calendar' : 'calendar-outline'" class="nav-icon"></ion-icon>
                <div class="nav-indicator"></div>
            </router-link>
            <router-link to="/logs" class="nav-item-c" active-class="active">
                <ion-icon :name="$route.path.includes('/logs') ? 'wallet' : 'wallet-outline'" class="nav-icon"></ion-icon>
                <div class="nav-indicator"></div>
            </router-link>
            <router-link to="/settings" class="nav-item-c" active-class="active">
                <ion-icon :name="$route.path.includes('/settings') ? 'options' : 'options-outline'" class="nav-icon"></ion-icon>
                <div class="nav-indicator"></div>
            </router-link>
        </div>
    </nav>

    <div class="scale-container">
        <router-view v-slot="{ Component }">
            <keep-alive>
                <component :is="Component" :key="$route.path" />
            </keep-alive>
        </router-view>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMainStore } from './store.js'

const route = useRoute()
const globalState = useMainStore()

// 是否显示导航栏（登录页和搜索页不显示）
const showNav = computed(() => {
    const publicPages = ['/login', '/search']
    return !publicPages.includes(route.path)
})

const handleScroll = () => {
    const topMask = document.getElementById('dynamic-top-mask');
    if (!topMask) return;
    const st = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    if (st > 15) { topMask.classList.add('show'); } else { topMask.classList.remove('show'); }
}

let pollingInterval = null;

onMounted(async () => {
    // 检查登录状态
    await globalState.checkAuth()
    
    // 如果已登录，加载数据
    if (globalState.isLoggedIn) {
        globalState.fetchMpData();
        globalState.loadLpData();
        globalState.loadNodes();
    }

    window.addEventListener('scroll', handleScroll, { passive: true });

    // 每 5 秒静默轮询一次
    pollingInterval = setInterval(() => {
        if (document.hidden) return;
        if (!globalState.isLoggedIn) return;
        globalState.nowTime = new Date();
        globalState.fetchMpData();
        globalState.loadLpData();
        globalState.loadNodes();
    }, 5000);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
    if (pollingInterval) clearInterval(pollingInterval);
});
</script>