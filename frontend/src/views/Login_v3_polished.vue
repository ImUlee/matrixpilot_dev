<template>
  <div class="login-wrapper">
    <!-- 背景装饰 -->
    <div class="bg-orb bg-orb-1"></div>
    <div class="bg-orb bg-orb-2"></div>
    <div class="bg-orb bg-orb-3"></div>
    
    <!-- 主内容 -->
    <div class="main-content">
      <!-- Logo -->
      <div class="logo-wrapper">
        <svg viewBox="0 0 56 56" fill="none" class="logo-svg">
          <circle cx="28" cy="28" r="26" stroke="url(#grad Minimal)" stroke-width="1.5"/>
          <path d="M18 28L25 35L38 22" stroke="url(#gradMinimal)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <defs>
            <linearGradient id="gradMinimal" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#A5B4FC"/>
              <stop offset="100%" stop-color="#6366F1"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      
      <!-- 标题 -->
      <h1 class="title">MatrixPilot</h1>
      
      <!-- 输入框 -->
      <div class="input-wrapper">
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
          class="arrow-btn" 
          @click="handleLogin"
          :disabled="loading || !pin"
        >
          <ion-icon name="arrow-forward"></ion-icon>
        </button>
      </div>
      
      <!-- 错误提示 -->
      <transition name="fade">
        <p v-if="error" class="error">{{ error }}</p>
      </transition>
    </div>
    
    <!-- 底部版权 -->
    <div class="footer">
      <span>智能中控管理平台</span>
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
/* 全屏修复 */
.login-wrapper {
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  background: #0C0C0E;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

/* 动态背景光晕 */
.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
  pointer-events: none;
}

.bg-orb-1 {
  width: 500px;
  height: 500px;
  background: #4F46E5;
  top: -150px;
  left: -150px;
  animation: drift1 12s ease-in-out infinite;
}

.bg-orb-2 {
  width: 400px;
  height: 400px;
  background: #7C3AED;
  bottom: -100px;
  right: -100px;
  animation: drift2 15s ease-in-out infinite;
}

.bg-orb-3 {
  width: 300px;
  height: 300px;
  background: #06B6D4;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse3 10s ease-in-out infinite;
}

@keyframes drift1 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(50px, 50px); }
}

@keyframes drift2 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-40px, -40px); }
}

@keyframes pulse3 {
  0%, 100% { opacity: 0.2; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.4; transform: translate(-50%, -50%) scale(1.1); }
}

/* 主内容区 */
.main-content {
  width: 100%;
  max-width: 320px;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo */
.logo-wrapper {
  width: 64px;
  height: 64px;
  margin-bottom: 40px;
  animation: logoFloat 4s ease-in-out infinite;
}

.logo-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 20px rgba(99,102,241,0.4));
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* 标题 */
.title {
  color: #F4F4F5;
  font-size: 20px;
  font-weight: 300;
  letter-spacing: 8px;
  margin: 0 0 48px;
  text-transform: uppercase;
  opacity: 0.9;
}

/* 输入框 */
.input-wrapper {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  padding: 4px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  width: 100%;
}

.input-wrapper:focus-within {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 0 30px rgba(99, 102, 241, 0.15);
  transform: scale(1.02);
}

.input-wrapper input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 16px 20px;
  font-size: 16px;
  color: #FAFAFA;
  outline: none;
  text-align: center;
  letter-spacing: 4px;
}

.input-wrapper input::placeholder {
  font-size: 13px;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.25);
}

.input-wrapper input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 30px #0C0C0E inset !important;
  -webkit-text-fill-color: #FAFAFA !important;
}

/* 箭头按钮 */
.arrow-btn {
  width: 48px;
  height: 48px;
  border: none;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  color: #A5B4FC;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.arrow-btn:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.3);
  transform: translateX(4px);
}

.arrow-btn:active:not(:disabled) {
  transform: scale(0.92);
}

.arrow-btn:disabled {
  opacity: 0.2;
  cursor: not-allowed;
}

.arrow-btn ion-icon {
  font-size: 18px;
}

/* 错误 */
.error {
  color: #F87171;
  font-size: 13px;
  margin-top: 20px;
  font-weight: 400;
  letter-spacing: 0.5px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 底部 */
.footer {
  position: absolute;
  bottom: 32px;
  left: 0;
  right: 0;
  text-align: center;
}

.footer span {
  color: rgba(255, 255, 255, 0.2);
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* 响应式 */
@media (max-width: 480px) {
  .main-content {
    padding: 32px 20px;
  }
  
  .logo-wrapper {
    width: 56px;
    height: 56px;
    margin-bottom: 32px;
  }
  
  .title {
    font-size: 18px;
    letter-spacing: 6px;
    margin-bottom: 40px;
  }
  
  .input-wrapper input {
    padding: 14px 16px;
    font-size: 15px;
  }
  
  .arrow-btn {
    width: 44px;
    height: 44px;
  }
}
</style>
