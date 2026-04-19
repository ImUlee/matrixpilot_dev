<template>
  <div class="search-page">
    <div class="search-container">
      <!-- 标题栏 -->
      <div class="header-bar">
        <div class="back-inline" :class="{show: result.found || result.has_suggestion}" @click="handleTitleClick">
          <ion-icon name="chevron-back"></ion-icon>
        </div>
        <h1 class="page-title"><a @click="handleTitleClick">MATRIXPILOT</a></h1>
      </div>
      
      <!-- 搜索框 -->
      <div class="glass-pill">
        <input 
          type="text" 
          class="search-input" 
          placeholder="输入账号昵称..." 
          v-model="userInput" 
          @input="onInput"
        >
        <button class="search-btn" @click="doSearch()">
          <ion-icon name="search"></ion-icon>
        </button>
      </div>

      <!-- Emoji 提示 -->
      <div v-if="showEmojiTip" class="emoji-tip">
        <ion-icon name="bulb"></ion-icon> 
        昵称中的 Emoji 已自动适配为记录格式 (??)
      </div>

      <!-- 搜索历史 -->
      <div v-if="!userInput && searchHistory.length > 0 && !result.found" class="history-container">
        <div class="history-header">
          <div class="history-title">最近搜索</div>
          <ion-icon name="trash-outline" @click="clearHistory"></ion-icon>
        </div>
        <div>
          <div v-for="h in searchHistory" :key="h" class="history-pill" @click="selectHistory(h)">
            <ion-icon name="time-outline"></ion-icon>
            {{ h }}
          </div>
        </div>
      </div>

      <!-- 搜索建议 -->
      <div v-if="!result.found && result.has_suggestion && result.display_suggestions?.length" class="suggestion-container">
        <div class="suggestion-title">请选择对应账号进行查询：</div>
        <div 
          class="suggestion-item" 
          v-for="s in result.display_suggestions" 
          :key="s.secret" 
          @click="selectSuggestion(s)"
        >
          <span class="suggestion-text">{{ s.display }}</span>
          <ion-icon name="chevron-forward-circle"></ion-icon>
        </div>
      </div>

      <!-- 结果卡片 -->
      <div v-if="result.found" class="result-card">
        <!-- 日期筛选 -->
        <div class="date-filter-row">
          <div class="date-input-item">
            <span class="date-prefix" v-show="!startDate">From</span>
            <input type="date" v-model="startDate" @change="doSearch(userInput)">
          </div>
          <div class="date-input-item">
            <span class="date-prefix" v-show="!endDate">To</span>
            <input type="date" v-model="endDate" @change="doSearch(userInput)">
          </div>
          <div 
            class="date-clear-btn" 
            :style="{ color: (startDate || endDate) ? 'var(--danger)' : 'var(--text-sub)' }" 
            @click="clearDates"
          >
            <ion-icon name="trash"></ion-icon>
          </div>
        </div>

        <!-- 用户信息 -->
        <div class="user-info">
          <div class="inbox-label">Inbox</div>
          <div class="nickname">{{ result.display_nickname }}</div>
        </div>
        
        <!-- 统计数据 -->
        <div class="stat-grid">
          <div class="stat-item">
            <span class="stat-val">{{ result.total_sum }}</span>
            <span class="stat-label">累计产出</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-val physical">{{ result.physical_count }}</span>
            <span class="stat-label">实物中奖</span>
          </div>
        </div>

        <!-- 轨迹明细 -->
        <div class="logs-section">
          <div class="logs-title">
            <ion-icon name="analytics"></ion-icon> 
            轨迹明细 ({{ result.logs.length }}条)
          </div>
          <div class="log-row" v-for="log in result.logs" :key="log.date + log.item_type">
            <div class="log-left">
              <div class="log-date">{{ formatLogDate(log.date) }}</div>
              <div class="log-node">节点：{{ log.node || '未知' }}</div>
            </div>
            <div class="log-right">
              <div class="log-quantity" :class="{ diamond: log.item_type === '钻石', physical: log.item_type !== '钻石' }">
                <template v-if="log.item_type === '钻石'">+{{ log.quantity }}</template>
                <template v-else>实物掉落</template>
              </div>
              <div class="log-item-type">{{ log.item_type }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="bottom-action-group" v-if="result.found">
        <div class="action-circle-btn" @click="generateShareCard">
          <ion-icon name="share"></ion-icon>
        </div>
        <div class="action-circle-btn" @click="wxModal.show = true">
          <ion-icon name="logo-wechat"></ion-icon>
        </div>
      </div>

      <!-- FAQ 区域 -->
      <div class="qa-section" v-show="!result.found && !result.has_suggestion && faqList && faqList.length > 0">
        <div class="qa-title">FAQ</div>
        <details class="qa-item" v-for="(item, idx) in faqList" :key="idx">
          <summary class="qa-summary">
            <div class="qa-summary-content">
              <ion-icon :name="item.icon || 'help-circle-outline'" class="qa-item-icon"></ion-icon>
              <span>{{ item.q }}</span>
            </div>
            <ion-icon name="chevron-down" class="qa-toggle-icon"></ion-icon>
          </summary>
          <div class="qa-content" v-html="item.a"></div>
        </details>
      </div>

      <!-- 底部微信按钮 -->
      <div class="footer-action" v-show="!result.found && !result.has_suggestion">
        <div class="action-circle-btn" @click="wxModal.show = true">
          <ion-icon name="logo-wechat"></ion-icon>
        </div>
      </div>
    </div>

    <!-- 导出卡片模板（隐藏） -->
    <div id="export-card-template" ref="exportCard">
      <div class="export-tag">MATRIXPILOT</div>
      <div class="export-nickname">{{ result.display_nickname }}</div>
      
      <div class="export-stats-box">
        <div class="export-stats-row">
          <div class="export-stats-item">
            <div class="export-stats-val success">{{ result.win_times }}</div>
            <div class="export-stats-label">中奖次数</div>
          </div>
          <div class="export-divider-v"></div>
          <div class="export-stats-item">
            <div class="export-stats-val primary">{{ result.total_sum }}</div>
            <div class="export-stats-label">累计产出</div>
          </div>
        </div>

        <div class="export-divider-h"></div>

        <div class="export-stats-row">
          <div class="export-stats-item">
            <div class="export-stats-val orange">{{ result.max_win }}</div>
            <div class="export-stats-label">最高单笔</div>
          </div>
          <div class="export-divider-v"></div>
          <div class="export-stats-item">
            <div class="export-stats-val danger">{{ result.physical_count }}</div>
            <div class="export-stats-label">实物中奖</div>
          </div>
        </div>
      </div>

      <div class="export-quote">" {{ currentHitokoto }} "</div>
      <div class="export-footer">Powered by MatrixPilot</div>
    </div>

    <!-- 截图预览 -->
    <div v-if="screenshot.show" class="screenshot-overlay" @click="screenshot.show = false">
      <img :src="screenshot.url" class="preview-img" @click.stop>
      <div class="preview-tip">长按图片保存到相册</div>
      <ion-icon name="close-circle" class="close-icon" @click="screenshot.show = false"></ion-icon>
    </div>

    <!-- 微信弹窗 -->
    <div v-if="wxModal.show" class="modal-mask" @click="wxModal.show = false">
      <div class="pop-modal" @click.stop>
        <ion-icon name="close-circle" class="modal-close" @click="wxModal.show = false"></ion-icon>
        <img :src="qrImgSrc" class="qr-image">
        <div class="wx-id">WeChat<span class="wx-handle">@imulee</span></div>
        <button class="copy-btn" @click="copyWxId">复制</button>
      </div>
    </div>

    <!-- 返回顶部 -->
    <div class="back-to-top" :class="{show: showScrollTop}" @click="scrollToTop">
      <ion-icon name="chevron-up"></ion-icon>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import axios from 'axios'

// 状态
const userInput = ref('')
const startDate = ref('')
const endDate = ref('')
const result = ref({ found: false, has_suggestion: false, logs: [] })
const showScrollTop = ref(false)
const showEmojiTip = ref(false)
const searchHistory = ref([])
const faqList = ref([])
const screenshot = ref({ show: false, url: '' })
const wxModal = ref({ show: false, copyId: 'imulee' })
const qrImgSrc = ref('')
const currentHitokoto = ref('')
const exportCard = ref(null)

// 配置
const quotes = [
  "万事胜意，来日方长。",
  "凡是过往，皆为序章。",
  "与其向往，不如出发。",
  "心之向往，素履以往。",
  "星光不问赶路人。",
  "纵有疾风起，不言弃。",
  "从此星辰璀璨。",
  "山河错落，你是曙光。",
  "万物可爱，人间值得。"
]

// Emoji 处理
let tipTimer = null
const handleEmojiReplace = (val) => {
  if (!val) return
  const emojiRegex = /[\uD800-\uDBFF][\uDC00-\uDFFF]|\p{Emoji_Presentation}|\p{Extended_Pictographic}/gu
  if (emojiRegex.test(val)) {
    showEmojiTip.value = true
    clearTimeout(tipTimer)
    tipTimer = setTimeout(() => { showEmojiTip.value = false }, 3500)
  }
}

watch(userInput, (newVal) => handleEmojiReplace(newVal))

// 日期格式化
const formatLogDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.substring(5, 16).replace(/-/g, '/')
}

// 标题点击
const handleTitleClick = () => {
  userInput.value = ''
  startDate.value = ''
  endDate.value = ''
  result.value = { found: false, has_suggestion: false, suggestions: [], display_suggestions: [], display_nickname: '', logs: [] }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 搜索
let debounceTimer = null
const onInput = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { doSearch() }, 300)
}

const doSearch = async (targetName = null) => {
  const query = targetName || userInput.value.trim()
  if (!query) {
    result.value = { found: false, has_suggestion: false, suggestions: [], display_suggestions: [], display_nickname: '', logs: [] }
    return
  }
  
  const emojiRegex = /[\uD800-\uDBFF][\uDC00-\uDFFF]|\p{Emoji_Presentation}|\p{Extended_Pictographic}/gu
  const secretQuery = query.replace(emojiRegex, '??')

  try {
    const res = await axios.get(`/api/public_search?nickname=${encodeURIComponent(secretQuery)}&start_date=${startDate.value}&end_date=${endDate.value}`)
    
    let finalData = { ...res.data, logs: res.data.logs || [] }
    
    if (finalData.found && finalData.real_nickname && finalData.real_nickname.toLowerCase() === secretQuery.toLowerCase()) {
      finalData.display_nickname = query
    } else {
      finalData.display_nickname = finalData.real_nickname
    }

    if (finalData.has_suggestion && finalData.suggestions) {
      const safeSecretQuery = secretQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      const regex = new RegExp(safeSecretQuery, 'i')
      
      finalData.display_suggestions = finalData.suggestions.map(s => {
        let displayStr = s
        if (secretQuery) {
          displayStr = s.replace(regex, query)
        }
        return { secret: s, display: displayStr }
      })
    } else {
      finalData.display_suggestions = []
    }

    result.value = finalData

    if (finalData.found) {
      let history = [...searchHistory.value]
      const nameToSave = finalData.display_nickname
      const idx = history.indexOf(nameToSave)
      if (idx !== -1) history.splice(idx, 1)
      history.unshift(nameToSave)
      if (history.length > 8) history = history.slice(0, 8)
      searchHistory.value = history
      localStorage.setItem('mp_search_history', JSON.stringify(history))
    }
  } catch (e) {
    console.error('搜索失败', e)
  }
}

// 选择建议
const selectSuggestion = (s) => {
  userInput.value = s.display
  doSearch(s.display)
}

// 选择历史
const selectHistory = (h) => {
  userInput.value = h
  doSearch(h)
}

// 清除历史
const clearHistory = () => {
  searchHistory.value = []
  localStorage.removeItem('mp_search_history')
}

// 清除日期
const clearDates = () => {
  startDate.value = ''
  endDate.value = ''
  doSearch()
}

// 生成分享卡片
const generateShareCard = async () => {
  currentHitokoto.value = quotes[Math.floor(Math.random() * quotes.length)]
  await nextTick()
  
  // 动态加载 html2canvas
  if (!window.html2canvas) {
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/html2canvas@1.4.1/dist/html2canvas.min.js'
    script.onload = () => captureCard()
    document.head.appendChild(script)
  } else {
    captureCard()
  }
}

const captureCard = () => {
  if (!exportCard.value) return
  window.html2canvas(exportCard.value, { 
    scale: 3, 
    backgroundColor: null, 
    useCORS: true, 
    logging: false 
  }).then(canvas => {
    screenshot.value.url = canvas.toDataURL('image/png', 1.0)
    screenshot.value.show = true
  })
}

// 复制微信ID
const copyWxId = () => {
  navigator.clipboard.writeText(wxModal.value.copyId).then(() => {
    alert("✅ 已复制: imulee")
  })
}

// 滚动
const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })
const handleScroll = () => { showScrollTop.value = window.scrollY > 300 }

// 加载 FAQ
const loadFaq = async () => {
  try {
    const res = await axios.get('/api/faq')
    faqList.value = res.data.faq || []
  } catch (e) {
    // 默认 FAQ
    faqList.value = [
      { q: "数据多久更新一次？", a: "数据由系统各节点实时上报，通常延迟不超过 1 分钟。", icon: "time-outline" },
      { q: "为什么查不到我的账号？", a: "1. 可能是您输入了错别字或漏掉了符号。<br>2. 如果您的昵称带有表情，请尝试直接输入原表情。", icon: "search-outline" },
      { q: "如何保存与分享战绩？", a: "查询成功后，点击页面下方的「分享」图标，即可一键生成您的专属数据报告海报。", icon: "share" }
    ]
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  
  // 加载搜索历史
  try {
    const hist = localStorage.getItem('mp_search_history')
    if (hist) searchHistory.value = JSON.parse(hist)
  } catch (e) {}
  
  // 加载 FAQ
  loadFaq()
  
  // 预加载二维码
  const fullQrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://u.wechat.com/MLOieu3qukfxdsa-btCnd3o?s=2'
  qrImgSrc.value = fullQrUrl
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');

.search-page {
  min-height: 100vh;
  min-height: 100dvh;
  background: linear-gradient(to bottom, var(--grad-top, #addcee) 0%, var(--app-bg, #f1f5f6) 100%);
  background-attachment: fixed;
  padding: calc(env(safe-area-inset-top, 0px) + 15px) 0 60px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

@media (prefers-color-scheme: dark) {
  .search-page {
    --grad-top: #0A2540;
    --app-bg: #1C1C1E;
    --card-bg: rgba(28, 28, 30, 0.65);
    --text-main: #FFFFFF;
    --text-sub: #AEAEB2;
  }
}

.search-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 标题栏 */
.header-bar {
  position: relative;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
}

.page-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  font-weight: 900;
  margin: 0;
  text-align: center;
  letter-spacing: 3px;
  text-transform: uppercase;
}

.page-title a {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.back-inline {
  position: absolute;
  left: 0;
  top: 0;
  width: 48px;
  height: 48px;
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary, #007AFF);
  opacity: 0;
  transform: scale(0.5);
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.back-inline.show {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}

.back-inline ion-icon {
  font-size: 24px;
}

/* 搜索框 */
.glass-pill {
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  height: 64px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  padding: 0 12px 0 20px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: var(--text-main, #1C1C1E);
}

.search-input::placeholder {
  color: var(--text-sub, #A8A8A8);
}

.search-btn {
  background: var(--primary, #007AFF);
  color: white;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.2s;
}

.search-btn:active {
  transform: scale(0.95);
}

/* Emoji 提示 */
.emoji-tip {
  font-size: 12px;
  color: var(--ios-orange, #FF9500);
  text-align: center;
  margin-top: -10px;
  margin-bottom: 15px;
  font-weight: 600;
}

/* 历史记录 */
.history-container {
  margin-bottom: 20px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 0 5px;
}

.history-title {
  font-size: 12px;
  color: var(--text-sub, #8E8E93);
  font-weight: 700;
  letter-spacing: 1px;
}

.history-header ion-icon {
  font-size: 16px;
  color: var(--text-sub, #8E8E93);
  cursor: pointer;
  opacity: 0.6;
}

.history-pill {
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  border-radius: 16px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-main, #1C1C1E);
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  margin: 0 8px 8px 0;
  transition: 0.2s;
}

.history-pill:active {
  transform: scale(0.95);
  opacity: 0.8;
}

.history-pill ion-icon {
  margin-right: 4px;
  font-size: 14px;
  opacity: 0.6;
}

/* 建议列表 */
.suggestion-container {
  margin-bottom: 20px;
}

.suggestion-title {
  font-size: 12px;
  color: var(--text-sub, #8E8E93);
  font-weight: 700;
  margin-bottom: 10px;
  padding-left: 10px;
  letter-spacing: 1px;
}

.suggestion-item {
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  border-radius: 24px;
  padding: 18px 20px;
  margin-bottom: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 16px;
  color: var(--text-main, #1C1C1E);
  transition: transform 0.2s, opacity 0.2s;
}

.suggestion-item:active {
  transform: scale(0.98);
  opacity: 0.8;
}

.suggestion-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.suggestion-item ion-icon {
  font-size: 24px;
  color: var(--text-sub, #8E8E93);
  opacity: 0.5;
  flex-shrink: 0;
}

/* 结果卡片 */
.result-card {
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border-radius: 24px;
  padding: 25px 20px;
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  animation: slideUpResult 0.5s ease;
}

@keyframes slideUpResult {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 日期筛选 */
.date-filter-row {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 25px;
}

.date-input-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  min-width: 0;
  border-radius: 16px;
  height: 48px;
  overflow: hidden;
  background: transparent;
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
}

.date-input-item input {
  border: none;
  background: transparent;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-main, #1C1C1E);
  width: 100%;
  outline: none;
  text-align: center;
  height: 100%;
}

.date-prefix {
  position: absolute;
  font-size: 10px;
  color: var(--text-sub, #8E8E93);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.date-clear-btn {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: transparent;
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  cursor: pointer;
  transition: 0.2s;
}

.date-clear-btn:active {
  transform: scale(0.92);
  opacity: 0.7;
}

/* 用户信息 */
.user-info {
  text-align: center;
  margin-bottom: 5px;
}

.inbox-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 10px;
  color: var(--text-sub, #8E8E93);
  letter-spacing: 2px;
  font-weight: 800;
}

.nickname {
  font-size: 24px;
  font-weight: 700;
  margin-top: 5px;
  color: var(--text-main, #1C1C1E);
}

/* 统计 */
.stat-grid {
  display: flex;
  justify-content: space-around;
  gap: 8px;
  text-align: center;
  margin-top: 15px;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-val {
  font-size: 26px;
  font-weight: 800;
  color: var(--primary, #007AFF);
  font-family: ui-rounded, system-ui;
}

.stat-val.physical {
  color: var(--ios-orange, #FF9500);
}

.stat-label {
  font-size: 12px;
  color: var(--text-sub, #8E8E93);
  margin-top: 8px;
  font-weight: 600;
}

.stat-divider {
  width: 1px;
  height: 35px;
  background: var(--glass-border, rgba(0, 0, 0, 0.05));
  align-self: flex-end;
  margin-bottom: 5px;
}

/* 日志列表 */
.logs-section {
  margin-top: 40px;
}

.logs-title {
  font-weight: 800;
  font-size: 13px;
  margin-bottom: 12px;
  color: var(--text-sub, #8E8E93);
  display: flex;
  align-items: center;
  letter-spacing: 1px;
}

.logs-title ion-icon {
  margin-right: 6px;
}

.log-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
}

.log-date {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main, #1C1C1E);
}

.log-node {
  font-size: 11px;
  color: var(--text-sub, #8E8E93);
  margin-top: 2px;
}

.log-quantity {
  font-weight: 800;
  text-align: right;
}

.log-quantity.diamond {
  color: var(--primary, #007AFF);
}

.log-quantity.physical {
  color: var(--ios-orange, #FF9500);
}

.log-item-type {
  font-size: 10px;
  color: var(--text-sub, #8E8E93);
  margin-top: 2px;
  text-align: right;
}

/* 操作按钮 */
.bottom-action-group,
.footer-action {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin: 40px auto 20px;
  padding-bottom: 10px;
}

.action-circle-btn {
  width: 56px;
  height: 56px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  transition: 0.3s;
}

.action-circle-btn ion-icon {
  font-size: 24px;
}

.action-circle-btn:first-child ion-icon {
  color: var(--primary, #007AFF);
}

.action-circle-btn:last-child ion-icon {
  color: #07C160;
}

/* FAQ */
.qa-section {
  padding-bottom: 20px;
  margin-top: 40px;
}

.qa-title {
  text-align: center;
  font-size: 15px;
  font-weight: 800;
  color: var(--text-sub, #8E8E93);
  letter-spacing: 12px;
  margin-bottom: 20px;
  margin-left: 12px;
  text-transform: uppercase;
}

.qa-item {
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  border-radius: 24px;
  margin-bottom: 12px;
  overflow: hidden;
}

.qa-summary {
  padding: 18px 20px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main, #1C1C1E);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  list-style: none;
}

.qa-summary-content {
  display: flex;
  align-items: center;
  flex: 1;
}

.qa-item-icon {
  font-size: 22px;
  color: var(--primary, #007AFF);
  margin-right: 12px;
}

.qa-toggle-icon {
  font-size: 18px;
  color: var(--text-sub, #8E8E93);
  opacity: 0.5;
  transition: transform 0.3s;
}

details[open] .qa-toggle-icon {
  transform: rotate(180deg);
}

.qa-content {
  padding: 0 20px 20px 54px;
  font-size: 13px;
  color: var(--text-sub, #8E8E93);
  line-height: 1.6;
}

/* 返回顶部 */
.back-to-top {
  position: fixed;
  right: 24px;
  bottom: 100px;
  width: 48px;
  height: 48px;
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary, #007AFF);
  opacity: 0;
  transform: scale(0.5);
  pointer-events: none;
  z-index: 2000;
  transition: all 0.3s;
}

.back-to-top.show {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}

/* 截图预览 */
.screenshot-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(15px);
  z-index: 5000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.preview-img {
  max-width: 85%;
  max-height: 70vh;
  border-radius: 40px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.preview-tip {
  color: white;
  margin-top: 25px;
  font-size: 15px;
  font-weight: 700;
  background: var(--primary, #007AFF);
  padding: 12px 30px;
  border-radius: 30px;
}

.close-icon {
  color: white;
  font-size: 40px;
  margin-top: 30px;
  opacity: 0.6;
  cursor: pointer;
}

/* 微信弹窗 */
.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(5px);
  z-index: 3000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.pop-modal {
  width: 100%;
  max-width: 340px;
  padding: 30px 25px 25px;
  border-radius: 28px;
  text-align: center;
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(50px);
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
  position: relative;
  animation: popInModal 0.3s ease;
}

@keyframes popInModal {
  from { transform: scale(0.85); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 26px;
  color: var(--text-sub, #8E8E93);
  cursor: pointer;
}

.qr-image {
  width: 210px;
  height: 210px;
  border-radius: 16px;
  margin-bottom: 20px;
  background: white;
  padding: 5px;
}

.wx-id {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-main, #1C1C1E);
  margin-bottom: 25px;
}

.wx-handle {
  color: #07C160;
}

.copy-btn {
  height: 50px;
  background: var(--primary, #007AFF);
  color: white;
  border: none;
  border-radius: 25px;
  width: 100%;
  font-weight: 700;
  cursor: pointer;
}

/* 导出卡片模板 */
#export-card-template {
  position: absolute;
  top: -9999px;
  left: -9999px;
  width: 380px;
  border-radius: 24px;
  text-align: center;
  padding: 40px 30px 30px;
  background: linear-gradient(to bottom, #addcee 0%, #f1f5f6 100%);
}

@media (prefers-color-scheme: dark) {
  #export-card-template {
    background: linear-gradient(to bottom, #0A2540 0%, #1C1C1E 100%);
  }
}

.export-tag {
  font-family: 'Orbitron', sans-serif;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 3px;
  color: var(--text-sub, #8E8E93);
  opacity: 0.8;
}

.export-nickname {
  font-size: 32px;
  font-weight: 800;
  margin: 25px 0 20px;
  letter-spacing: -1px;
  color: var(--text-main, #1C1C1E);
}

.export-stats-box {
  margin: 20px 0 30px;
  padding: 25px 20px;
  border-radius: 24px;
  background: var(--card-bg, rgba(255, 255, 255, 0.85));
  border: 1px solid var(--glass-border, rgba(0, 0, 0, 0.05));
}

.export-stats-row {
  display: flex;
  gap: 10px;
}

.export-stats-item {
  flex: 1;
  text-align: center;
}

.export-stats-val {
  font-size: 30px;
  font-weight: 900;
  font-family: ui-rounded, system-ui;
}

.export-stats-val.success { color: #34C759; }
.export-stats-val.primary { color: #007AFF; }
.export-stats-val.orange { color: #FF9500; }
.export-stats-val.danger { color: #FF3B30; }

.export-stats-label {
  font-size: 11px;
  margin-top: 6px;
  font-weight: 400;
  color: var(--text-sub, #8E8E93);
}

.export-divider-h {
  width: 100%;
  height: 1px;
  margin: 15px 0;
  background: var(--glass-border, rgba(0, 0, 0, 0.05));
}

.export-divider-v {
  width: 1px;
  height: 35px;
  align-self: center;
  background: var(--glass-border, rgba(0, 0, 0, 0.05));
}

.export-quote {
  font-size: 13px;
  color: var(--text-sub, #8E8E93);
  line-height: 1.6;
  min-height: 35px;
  opacity: 0.8;
}

.export-footer {
  margin-top: 50px;
  font-size: 9px;
  font-weight: 400;
  letter-spacing: 1px;
  color: var(--text-sub, #8E8E93);
  opacity: 0.5;
}
</style>
