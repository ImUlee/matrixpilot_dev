<template>
  <div class="login-wrapper">
    <div class="login-container">
      <!-- Logo -->
      <div class="logo-box">
        <img :src="logoSrc" alt="Logo">
      </div>

      <!-- 标题 -->
      <h1 class="title">MatrixPilot</h1>
      <p class="subtitle">智能中控管理平台</p>

      <!-- 登录卡片 -->
      <div class="login-card">
        <form @submit.prevent="handleLogin">
          <input
            v-model="pin"
            type="password"
            class="ios-input"
            placeholder="输入访问密码"
            maxlength="10"
            autocomplete="off"
            :disabled="loading"
          >
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

      <!-- 底部提示 -->
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

// Logo 路径 - 修复路径
const logoSrc = '/icon-192.png'

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
    if (e.response?.data?.error) {
      error.value = e.response.data.error
    } else {
      error.value = '网络错误，请重试'
    }
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
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #0A0A0F 0%, #1A1A2E 50%, #16213E 100%);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

/* 背景装饰 */
.login-wrapper::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
  top: -200px;
  right: -200px;
  animation: float 8s ease-in-out infinite;
}

.login-wrapper::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(168,85,247,0.12) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation: float 10s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -30px) scale(1.05); }
}

.login-container {
  width: 100%;
  max-width: 380px;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
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
.logo-box {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(99,102,241,0.3);
  transition: all 0.3s ease;
}

.logo-box:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 40px rgba(99,102,241,0.4);
}

.logo-box img {
  width: 42px;
  height: 42px;
  object-fit: contain;
}

/* 标题 */
.title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0 0 8px;
  text-align: center;
  color: #FFFFFF;
  background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 14px;
  color: rgba(255,255,255,0.5);
  text-align: center;
  margin: 0 0 36px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

/* 登录卡片 */
.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: 24px;
  padding: 28px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.login-card:focus-within {
  transform: translateY(-2px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
  border-color: rgba(99,102,241,0.3);
}

/* 输入框 */
.ios-input {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 54px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.06);
  border: 1.5px solid rgba(255, 255, 255, 0.1);
  font-size: 18px;
  font-weight: 500;
  color: #FFFFFF;
  text-align: center;
  letter-spacing: 6px;
  outline: none;
  transition: all 0.25s ease;
  margin-bottom: 16px;
}

.ios-input::placeholder {
  font-size: 14px;
  font-weight: 400;
  letter-spacing: normal;
  color: rgba(255,255,255,0.3);
}

.ios-input:focus {
  border-color: #6366F1;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 4px rgba(99,102,241,0.15);
}

.ios-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 按钮 */
.ios-btn-primary {
  width: 100%;
  height: 54px;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
  color: #FFFFFF;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 2px;
  box-shadow: 0 4px 16px rgba(99,102,241,0.3);
}

.ios-btn-primary:hover:not(:disabled) {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99,102,241,0.4);
}

.ios-btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}

.ios-btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 加载动画 */
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

/* 错误提示 */
.error-message {
  margin-top: 16px;
  padding: 14px 16px;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 12px;
  color: #FCA5A5;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  animation: shake 0.4s ease;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.error-message ion-icon {
  font-size: 16px;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}

/* 底部提示 */
.footer-hint {
  margin-top: 40px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(255,255,255,0.35);
}

.footer-hint ion-icon {
  font-size: 14px;
  color: #10B981;
}

/* 响应式 */
@media (max-width: 480px) {
  .login-container {
    padding: 24px 20px;
  }
  
  .logo-box {
    width: 64px;
    height: 64px;
    border-radius: 18px;
  }
  
  .logo-box img {
    width: 36px;
    height: 36px;
  }
  
  .title {
    font-size: 24px;
  }
  
  .login-card {
    padding: 24px;
  }
  
  .ios-input {
    height: 50px;
    font-size: 16px;
  }
  
  .ios-btn-primary {
    height: 50px;
  }
}
</style>
