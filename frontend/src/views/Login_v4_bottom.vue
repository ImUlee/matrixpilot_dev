<template>
  <div class="login-wrapper">
    <!-- 版本4: 顶部装饰 + 底部表单 -->
    <div class="top-decoration">
      <div class="glow-orb"></div>
      <div class="glow-orb-2"></div>
    </div>
    
    <div class="bottom-form">
      <div class="form-header">
        <div class="logo-wrapper">
          <div class="logo-bg">
            <ion-icon name="grid"></ion-icon>
          </div>
        </div>
        <h2>MatrixPilot</h2>
        <p>智能中控管理平台</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-field">
          <label>访问密码</label>
          <div class="input-box">
            <ion-icon name="lock-closed-outline"></ion-icon>
            <input
              v-model="pin"
              type="password"
              placeholder="请输入密码"
              maxlength="10"
              autocomplete="off"
              :disabled="loading"
            >
          </div>
        </div>
        
        <button 
          type="submit" 
          class="submit-btn"
          :disabled="loading || !pin"
        >
          <span v-if="loading" class="loading"></span>
          <span v-else>登 录</span>
        </button>
        
        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>
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
    error.value = '网络错误'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  background: linear-gradient(180deg, #0A0A0F 0%, #1A1A2E 100%);
  display: flex;
  flex-direction: column;
}

.top-decoration {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.glow-orb {
  position: absolute;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,0.4) 0%, transparent 70%);
  animation: float 6s ease-in-out infinite;
}

.glow-orb-2 {
  position: absolute;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(168,85,247,0.3) 0%, transparent 70%);
  top: 20%;
  right: 10%;
  animation: float 8s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-30px); }
}

.bottom-form {
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(20px);
  border-radius: 32px 32px 0 0;
  padding: 40px 32px 60px;
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-wrapper {
  margin-bottom: 16px;
}

.logo-bg {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #6366F1, #A855F7);
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.logo-bg ion-icon {
  font-size: 28px;
  color: white;
}

.form-header h2 {
  color: #FFFFFF;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px;
  letter-spacing: 1px;
}

.form-header p {
  color: rgba(255,255,255,0.4);
  font-size: 13px;
  margin: 0;
}

.login-form {
  max-width: 320px;
  margin: 0 auto;
}

.form-field {
  margin-bottom: 20px;
}

.form-field label {
  display: block;
  color: rgba(255,255,255,0.6);
  font-size: 13px;
  margin-bottom: 8px;
}

.input-box {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 0 16px;
  transition: all 0.3s;
}

.input-box:focus-within {
  border-color: #6366F1;
  background: rgba(255,255,255,0.08);
}

.input-box ion-icon {
  color: rgba(255,255,255,0.3);
  font-size: 18px;
}

.input-box input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 14px 12px;
  font-size: 15px;
  color: #FFFFFF;
  outline: none;
}

.input-box input::placeholder {
  color: rgba(255,255,255,0.25);
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #6366F1, #A855F7);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99,102,241,0.4);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-msg {
  color: #F87171;
  font-size: 13px;
  text-align: center;
  margin-top: 16px;
}
</style>
