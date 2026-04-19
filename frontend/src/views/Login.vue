<template>
  <div class="login-wrapper">
    <!-- Logo -->
    <div class="logo-box">
      <img :src="logoSrc" alt="Logo">
    </div>

    <!-- 标题 -->
    <div class="title">MatrixPilot</div>
    <div class="subtitle">智能中控管理平台</div>

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
      <ion-icon name="lock-closed-outline"></ion-icon>
      <span>安全验证</span>
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

// Logo 路径
const logoSrc = window.location.origin + '/static/icon.png'

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
      // 更新store状态
      store.$patch({ isLoggedIn: true })
      // 跳转到首页
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
.login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  animation: fadeInOut 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInOut {
  from {
    opacity: 0;
    transform: scale(1.05);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.logo-box {
  width: 68px;
  height: 68px;
  background: linear-gradient(135deg, #FFF 0%, #E5E5EA 100%);
  border-radius: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 18px;
  border: 1px solid var(--border-color, rgba(229, 229, 234, 0.7));
  transition: all 0.3s ease;
  overflow: hidden;
}

.logo-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

@media (prefers-color-scheme: dark) {
  .logo-box {
    background: linear-gradient(135deg, #2C2C2E 0%, #1C1C1E 100%);
    border-color: rgba(255, 255, 255, 0.04);
  }
}

.title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
  text-align: center;
  color: var(--text-main, #1C1C1E);
}

.subtitle {
  font-size: 13px;
  color: var(--text-sub, #8E8E93);
  text-align: center;
  margin-bottom: 28px;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.login-card {
  background: var(--card-bg, rgba(255, 255, 255, 0.7));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  width: 100%;
  max-width: 320px;
  border-radius: 22px;
  padding: 22px;
  border: 1px solid var(--border-color, rgba(229, 229, 234, 0.7));
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.ios-input {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 50px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.03);
  border: 1.5px solid transparent;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-main, #1C1C1E);
  text-align: center;
  letter-spacing: 8px;
  outline: none;
  transition: all 0.25s ease;
  margin-bottom: 18px;
  font-family: ui-rounded, "SF Pro Rounded", -apple-system, sans-serif;
}

@media (prefers-color-scheme: dark) {
  .ios-input {
    background: rgba(255, 255, 255, 0.03);
  }
}

.ios-input::placeholder {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: normal;
  color: var(--text-sub, #8E8E93);
}

.ios-input:focus {
  border-color: var(--primary, #007AFF);
  background: rgba(0, 0, 0, 0.01);
  transform: scale(1.01);
}

.ios-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.ios-btn-primary {
  width: 100%;
  height: 50px;
  border-radius: 14px;
  border: none;
  background: var(--primary, #007AFF);
  color: #FFF;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ios-btn-primary:hover:not(:disabled) {
  filter: brightness(1.1);
  transform: scale(1.02);
}

.ios-btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}

.ios-btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

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

.error-message {
  margin-top: 16px;
  padding: 12px 14px;
  background: rgba(255, 59, 48, 0.1);
  border-radius: 10px;
  color: var(--danger, #FF3B30);
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: shake 0.4s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

.footer-hint {
  margin-top: 32px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-sub, #8E8E93);
  opacity: 0.6;
}

.footer-hint ion-icon {
  font-size: 14px;
}
</style>
