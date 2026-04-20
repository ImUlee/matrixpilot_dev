<template>
  <div class="login-wrapper">
    <!-- 背景 -->
    <div class="bg-gradient"></div>
    <div class="bg-noise"></div>
    
    <!-- 主内容 -->
    <div class="login-container">
      <!-- Logo -->
      <div class="logo-box">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none">
            <rect x="2" y="2" width="28" height="28" rx="7" fill="url(#iosGrad)"/>
            <path d="M10 16L14 20L22 12" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="iosGrad" x1="2" y1="2" x2="30" y2="30">
                <stop stop-color="#0A84FF"/>
                <stop offset="1" stop-color="#5E5CE6"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>

      <!-- 标题 -->
      <h1 class="title">MatrixPilot</h1>
      <p class="subtitle">智能中控管理平台</p>

      <!-- 登录卡片 -->
      <div class="login-card">
        <form @submit.prevent="handleLogin">
          <div class="input-wrapper">
            <input
              v-model="pin"
              type="password"
              class="ios-input"
              placeholder="输入访问密码"
              maxlength="10"
              autocomplete="off"
              :disabled="loading"
            >
          </div>
          <button
            type="submit"
            class="ios-btn-primary"
            :disabled="loading || !pin"
          >
            <span v-if="loading" class="loading-spinner"></span>
            <span v-else>进入</span>
          </button>
        </form>
        <div v-if="error" class="error-message">
          <ion-icon name="alert-circle"></ion-icon>
          {{ error }}
        </div>
      </div>

      <!-- 底部 -->
      <div class="footer-hint">
        <ion-icon name="shield-checkmark-outline"></ion-icon>
        <span>安全验证</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '../store'
import axios from 'axios'

const pin = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()
const store = useMainStore()

const handleLogin = async () => {
  if (!pin.value || loading.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.post('/login', {
      pin: pin.value
    }, {
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (response.data.success) {
      store.$patch({ isLoggedIn: true })
      router.push('/overview')
    } else {
      error.value = response.data.error || '访问密码错误'
    }
  } catch (e) {
    error.value = e.response?.data?.error || '网络错误，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 全屏 */
.login-wrapper {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* iOS 深色背景 */
.bg-gradient {
  position: absolute;
  inset: 0;
  background: #000000;
}

.bg-gradient::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, #1C1C1E 0%, transparent 100%);
}

.bg-gradient::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(10,132,255,0.15) 0%, transparent 60%);
  top: -100px;
  right: -100px;
}

.bg-noise {
  position: absolute;
  inset: 0;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  pointer-events: none;
}

/* 主容器 */
.login-container {
  width: 100%;
  max-width: 340px;
  padding: 60px 24px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Logo - iOS 风格圆角 */
.logo-box {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 28px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.logo-icon {
  width: 44px;
  height: 44px;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

/* 标题 */
.title {
  font-size: 26px;
  font-weight: 600;
  color: #FFFFFF;
  margin: 0 0 6px;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 36px;
  font-weight: 400;
}

/* 登录卡片 - iOS 毛玻璃 */
.login-card {
  width: 100%;
  background: rgba(28, 28, 30, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 24px;
  border: 0.5px solid rgba(255, 255, 255, 0.1);
}

/* 输入框 - iOS 风格 */
.input-wrapper {
  margin-bottom: 12px;
}

.ios-input {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  font-size: 17px;
  color: #FFFFFF;
  text-align: center;
  letter-spacing: 2px;
  outline: none;
  transition: all 0.2s ease;
}

.ios-input::placeholder {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.3);
  letter-spacing: 0;
}

.ios-input:focus {
  border-color: #0A84FF;
  background: rgba(255, 255, 255, 0.12);
}

.ios-input:disabled {
  opacity: 0.5;
}

/* 按钮 - iOS 蓝色 */
.ios-btn-primary {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  border: none;
  background: #0A84FF;
  color: #FFFFFF;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ios-btn-primary:hover:not(:disabled) {
  background: #409CFF;
}

.ios-btn-primary:active:not(:disabled) {
  transform: scale(0.98);
  background: #007AFF;
}

.ios-btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 加载 */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 错误 - iOS 红色 */
.error-message {
  margin-top: 16px;
  padding: 12px;
  background: rgba(255, 59, 48, 0.15);
  border-radius: 10px;
  color: #FF6961;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.error-message ion-icon {
  font-size: 16px;
}

/* 底部 */
.footer-hint {
  margin-top: 40px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
}

.footer-hint ion-icon {
  font-size: 14px;
  color: #30D158;
}

/* 响应式 */
@media (max-width: 380px) {
  .login-container {
    padding: 40px 20px 32px;
  }
  
  .logo-box {
    width: 68px;
    height: 68px;
    border-radius: 18px;
  }
  
  .title {
    font-size: 22px;
  }
  
  .login-card {
    padding: 20px;
  }
}
</style>
