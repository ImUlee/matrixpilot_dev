<template>
  <div class="login-wrapper">
    <!-- 背景 -->
    <div class="bg-layer"></div>
    
    <!-- 主内容 -->
    <div class="main-content">
      <!-- Logo -->
      <div class="logo-container">
        <svg viewBox="0 0 48 48" fill="none" class="logo-svg">
          <circle cx="24" cy="24" r="22" stroke="url(#iosBlue)" stroke-width="1.5"/>
          <path d="M16 24L21 29L32 18" stroke="url(#iosBlue)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <defs>
            <linearGradient id="iosBlue" x1="8" y1="8" x2="40" y2="40">
              <stop stop-color="#0A84FF"/>
              <stop offset="1" stop-color="#5E5CE6"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      
      <!-- 标题 -->
      <h1 class="title">MatrixPilot</h1>
      
      <!-- 输入框组 -->
      <div class="input-group">
        <input
          v-model="pin"
          type="password"
          placeholder="密码"
          maxlength="10"
          autocomplete="off"
          :disabled="loading"
          @keyup.enter="handleLogin"
        >
        <button 
          class="submit-btn" 
          @click="handleLogin"
          :disabled="loading || !pin"
        >
          <ion-icon name="arrow-forward"></ion-icon>
        </button>
      </div>
      
      <!-- 错误 -->
      <transition name="fade">
        <p v-if="error" class="error">{{ error }}</p>
      </transition>
    </div>
    
    <!-- 底部 -->
    <div class="footer">
      智能中控管理平台
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
    const response = await axios.post('/login', { pin: pin.value })
    if (response.data.success) {
      store.$patch({ isLoggedIn: true })
      router.push('/overview')
    } else {
      error.value = response.data.error || '密码错误'
    }
  } catch (e) {
    error.value = '请重试'
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
  background: #000000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 背景层次 */
.bg-layer {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, #1C1C1E 0%, #000000 70%);
}

.bg-layer::before {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(10,132,255,0.1) 0%, transparent 60%);
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
}

/* 主内容 */
.main-content {
  width: 100%;
  max-width: 280px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo */
.logo-container {
  width: 56px;
  height: 56px;
  margin-bottom: 32px;
}

.logo-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 12px rgba(10, 132, 255, 0.3));
}

.logo-svg circle {
  animation: ringPulse 3s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

/* 标题 */
.title {
  color: #F5F5F7;
  font-size: 18px;
  font-weight: 400;
  letter-spacing: 6px;
  margin: 0 0 48px;
  text-transform: uppercase;
}

/* 输入框组 */
.input-group {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 3px;
  width: 100%;
  transition: all 0.25s ease;
}

.input-group:focus-within {
  border-color: rgba(10, 132, 255, 0.5);
  background: rgba(255, 255, 255, 0.1);
}

.input-group input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 14px 18px;
  font-size: 16px;
  color: #FFFFFF;
  outline: none;
  text-align: center;
  letter-spacing: 3px;
}

.input-group input::placeholder {
  font-size: 14px;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.25);
}

/* 按钮 */
.submit-btn {
  width: 42px;
  height: 42px;
  border: none;
  background: rgba(10, 132, 255, 0.2);
  border-radius: 50%;
  color: #0A84FF;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  margin-right: 3px;
}

.submit-btn:hover:not(:disabled) {
  background: #0A84FF;
  color: #FFFFFF;
}

.submit-btn:active:not(:disabled) {
  transform: scale(0.92);
}

.submit-btn:disabled {
  opacity: 0.2;
  cursor: not-allowed;
}

.submit-btn ion-icon {
  font-size: 16px;
}

/* 错误 */
.error {
  color: #FF6961;
  font-size: 13px;
  margin-top: 20px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 底部 */
.footer {
  position: absolute;
  bottom: 32px;
  color: rgba(255, 255, 255, 0.2);
  font-size: 11px;
  letter-spacing: 1px;
}

/* 响应式 */
@media (max-width: 380px) {
  .title {
    font-size: 16px;
    letter-spacing: 4px;
  }
  
  .logo-container {
    width: 48px;
    height: 48px;
  }
}
</style>
