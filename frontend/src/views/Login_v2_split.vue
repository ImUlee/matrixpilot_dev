<template>
  <div class="login-wrapper">
    <!-- 版本2: 左侧装饰 + 右侧表单 -->
    <div class="split-layout">
      <!-- 左侧装饰区 -->
      <div class="left-panel">
        <div class="decorative-circle"></div>
        <div class="decorative-circle-2"></div>
        <div class="brand-content">
          <div class="logo-icon">
            <svg viewBox="0 0 48 48" fill="none">
              <rect x="4" y="4" width="40" height="40" rx="10" fill="url(#grad2)"/>
              <path d="M14 24L20 30L34 16" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <defs>
                <linearGradient id="grad2" x1="4" y1="4" x2="44" y2="44">
                  <stop stop-color="#667EEA"/>
                  <stop offset="1" stop-color="#764BA2"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1>MatrixPilot</h1>
          <p>智能中控管理平台</p>
        </div>
      </div>
      
      <!-- 右侧表单区 -->
      <div class="right-panel">
        <div class="form-container">
          <h2>欢迎回来</h2>
          <p class="hint">输入访问密码继续</p>
          
          <form @submit.prevent="handleLogin">
            <div class="input-group">
              <ion-icon name="key-outline"></ion-icon>
              <input
                v-model="pin"
                type="password"
                placeholder="访问密码"
                maxlength="10"
                autocomplete="off"
                :disabled="loading"
              >
            </div>
            
            <button
              type="submit"
              class="login-btn"
              :disabled="loading || !pin"
            >
              <span v-if="loading" class="spinner"></span>
              <span v-else>进入系统</span>
            </button>
          </form>
          
          <div v-if="error" class="error-toast">
            <ion-icon name="alert-circle-outline"></ion-icon>
            {{ error }}
          </div>
        </div>
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
.login-wrapper {
  min-height: 100vh;
  background: #0F0F23;
}

.split-layout {
  display: flex;
  min-height: 100vh;
}

.left-panel {
  flex: 1;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.decorative-circle {
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3));
  top: -100px;
  left: -100px;
  animation: float 8s ease-in-out infinite;
}

.decorative-circle-2 {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
  bottom: -50px;
  right: -50px;
  animation: float 6s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.logo-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.brand-content h1 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px;
  letter-spacing: 2px;
}

.brand-content p {
  font-size: 14px;
  opacity: 0.7;
  margin: 0;
}

.right-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #fff;
}

.form-container {
  width: 100%;
  max-width: 360px;
}

.form-container h2 {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0 0 8px;
}

.form-container .hint {
  color: #8E8E93;
  font-size: 14px;
  margin: 0 0 40px;
}

.input-group {
  display: flex;
  align-items: center;
  background: #F2F2F7;
  border-radius: 12px;
  padding: 0 16px;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.input-group:focus-within {
  background: #E5E5EA;
  box-shadow: 0 0 0 2px #667EEA;
}

.input-group ion-icon {
  color: #8E8E93;
  font-size: 20px;
}

.input-group input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 16px 12px;
  font-size: 16px;
  outline: none;
}

.login-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667EEA, #764BA2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102,126,234,0.4);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-toast {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px 16px;
  background: #FFF2F2;
  color: #FF3B30;
  border-radius: 8px;
  font-size: 14px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .split-layout {
    flex-direction: column;
  }
  
  .left-panel {
    padding: 40px 20px;
    min-height: 200px;
  }
  
  .brand-content h1 {
    font-size: 24px;
  }
  
  .right-panel {
    padding: 30px 20px;
  }
}
</style>
