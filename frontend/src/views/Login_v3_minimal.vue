<template>
  <div class="login-wrapper">
    <!-- 版本3: 全屏极简 -->
    <div class="minimal-container">
      <div class="center-content">
        <!-- Logo -->
        <div class="logo">
          <svg viewBox="0 0 56 56" fill="none">
            <circle cx="28" cy="28" r="26" stroke="url(#grad3)" stroke-width="2"/>
            <path d="M18 28L25 35L38 22" stroke="url(#grad3)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#E0E0E0"/>
                <stop offset="100%" stop-color="#9E9E9E"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        
        <!-- 标题 -->
        <h1>MatrixPilot</h1>
        
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
.login-wrapper {
  min-height: 100vh;
  background: #1C1C1E;
  display: flex;
  flex-direction: column;
}

.minimal-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.center-content {
  width: 100%;
  max-width: 280px;
  text-align: center;
}

.logo {
  width: 56px;
  height: 56px;
  margin: 0 auto 32px;
  animation: pulse 2s ease-in-out infinite;
}

.logo svg {
  width: 100%;
  height: 100%;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(0.98); }
}

h1 {
  color: #FFFFFF;
  font-size: 22px;
  font-weight: 500;
  letter-spacing: 6px;
  margin: 0 0 48px;
  text-transform: uppercase;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.08);
  border-radius: 24px;
  padding: 4px;
  transition: all 0.3s;
}

.input-wrapper:focus-within {
  background: rgba(255,255,255,0.12);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.2);
}

.input-wrapper input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 14px 20px;
  font-size: 16px;
  color: #FFFFFF;
  outline: none;
  text-align: center;
  letter-spacing: 2px;
}

.input-wrapper input::placeholder {
  color: rgba(255,255,255,0.3);
}

.arrow-btn {
  width: 44px;
  height: 44px;
  border: none;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  color: #FFFFFF;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.arrow-btn:hover:not(:disabled) {
  background: rgba(255,255,255,0.2);
}

.arrow-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.arrow-btn ion-icon {
  font-size: 20px;
}

.error {
  color: #FF6B6B;
  font-size: 13px;
  margin-top: 16px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.footer {
  padding: 24px;
  text-align: center;
}

.footer span {
  color: rgba(255,255,255,0.25);
  font-size: 11px;
  letter-spacing: 1px;
}
</style>
