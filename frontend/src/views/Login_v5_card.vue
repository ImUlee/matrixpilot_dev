<template>
  <div class="login-wrapper">
    <!-- 版本5: 悬浮卡片 + 动态背景 -->
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    
    <div class="login-card">
      <div class="card-header">
        <div class="logo-icon">
          <ion-icon name="apps"></ion-icon>
        </div>
        <h1>MatrixPilot</h1>
        <p>智能中控管理平台</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="card-body">
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
          <template v-else>
            <span>进入</span>
            <ion-icon name="chevron-forward-outline"></ion-icon>
          </template>
        </button>
        
        <transition name="shake">
          <div v-if="error" class="error-box">
            <ion-icon name="warning-outline"></ion-icon>
            {{ error }}
          </div>
        </transition>
      </form>
      
      <div class="card-footer">
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
  background: #0F172A;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.bg-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: #3B82F6;
  top: -100px;
  left: -100px;
  animation: drift 15s ease-in-out infinite;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #8B5CF6;
  bottom: -50px;
  right: -50px;
  animation: drift 12s ease-in-out infinite reverse;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: #06B6D4;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse-bg 8s ease-in-out infinite;
}

@keyframes drift {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, 30px); }
}

@keyframes pulse-bg {
  0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.5; transform: translate(-50%, -50%) scale(1.1); }
}

.login-card {
  width: 100%;
  max-width: 380px;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4);
  position: relative;
  z-index: 1;
  animation: card-appear 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes card-appear {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3B82F6, #8B5CF6);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.logo-icon ion-icon {
  font-size: 32px;
  color: white;
}

.card-header h1 {
  font-size: 22px;
  font-weight: 700;
  color: #1E293B;
  margin: 0 0 4px;
  letter-spacing: 1px;
}

.card-header p {
  font-size: 13px;
  color: #64748B;
  margin: 0;
}

.input-group {
  display: flex;
  align-items: center;
  background: #F1F5F9;
  border-radius: 12px;
  padding: 0 16px;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.input-group:focus-within {
  background: #E2E8F0;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.2);
}

.input-group ion-icon {
  color: #94A3B8;
  font-size: 20px;
}

.input-group input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 14px 12px;
  font-size: 15px;
  color: #1E293B;
  outline: none;
}

.input-group input::placeholder {
  color: #94A3B8;
}

.login-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: linear-gradient(135deg, #3B82F6, #8B5CF6);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59,130,246,0.3);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-btn ion-icon {
  font-size: 18px;
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

.error-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 16px;
  padding: 10px;
  background: #FEF2F2;
  color: #EF4444;
  border-radius: 8px;
  font-size: 13px;
}

.error-box ion-icon {
  font-size: 16px;
}

.shake-enter-active {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #E2E8F0;
}

.card-footer ion-icon {
  font-size: 14px;
  color: #10B981;
}

.card-footer span {
  font-size: 12px;
  color: #64748B;
}
</style>
