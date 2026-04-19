<template>
    <div class="neon-page">
        <div class="page-header" style="margin-bottom: 16px; display: flex; align-items: center; width: 100%;">
            <div style="display: flex; align-items: center; flex-shrink: 0; padding-right: 4px;">
                <h1 class="big-title" style="margin: 0; padding-right: 8px;">Today</h1>
                <div class="nav-icon-pure" @click="resetRound" title="重置当前视图统计">
                    <ion-icon name="refresh-outline" style="font-size: 22px;"></ion-icon>
                </div>
            </div>

            <NodeSelector v-model="globalNodeFilter" :nodeList="nodeList" />
        </div>

        <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
            <div v-if="lpStats.unparsed_count > 0" class="neon-card"
                style="background: rgba(255, 59, 48, 0.12); border: 1px solid rgba(255, 59, 48, 0.25); padding: 16px; animation: popIn 0.3s ease-out;">
                <div style="display: flex; align-items: center; color: #FF453A; font-weight: bold; font-size: 16px; margin-bottom: 8px;">
                    <ion-icon name="warning" style="font-size: 22px; margin-right: 8px;"></ion-icon>拦截到未知日志格式！
                </div>
                <div style="color: var(--text-main); font-size: 13px; line-height: 1.5;">
                    集群隔离区拦截了 <b>{{ lpStats.unparsed_count || 0 }}</b> 批无法解析的底层数据。<br>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 12px;">
                    <button class="ios-btn-primary ios-btn-danger" style="flex: 1; height: 36px; font-size: 13px;" @click="viewUnparsedLogs">
                        <ion-icon name="search-outline" style="margin-right: 4px; font-size: 16px; vertical-align: text-bottom;"></ion-icon>透视拦截详情
                    </button>
                </div>
            </div>

            <!-- ===== 霓虹渐变全页背景 ===== -->
            <div class="neon-hero-section" style="border-radius: 24px; padding: 32px 20px; position: relative; overflow: hidden;">
                <!-- 霓虹光晕效果 -->
                <div class="neon-glow-1"></div>
                <div class="neon-glow-2"></div>
                <div class="neon-glow-3"></div>
                
                <div style="position: relative; z-index: 2; text-align: center;">
                    <div style="display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.7); font-size: 13px; font-weight: 600; margin-bottom: 8px; letter-spacing: 0.5px;">
                        <ion-icon name="flash" style="color: #FFD60A; font-size: 16px; margin-right: 8px;"></ion-icon>
                        今日核心产出
                    </div>
                    <div style="font-size: 4.2rem; font-weight: 900; color: #FFF; font-family: ui-rounded, -apple-system, sans-serif; line-height: 1.1; letter-spacing: -2px; text-shadow: 0 2px 20px rgba(0,0,0,0.3);">
                        {{ lpStats.total_wins || 0 }}
                    </div>
                </div>

                <!-- 下方三个统计项 -->
                <div style="display: flex; gap: 12px; margin-top: 28px; position: relative; z-index: 2;">
                    <div style="flex: 1; background: rgba(255,255,255,0.12); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 16px; padding: 16px 8px; text-align: center; border: 1px solid rgba(255,255,255,0.15);">
                        <ion-icon name="gift-outline" style="font-size: 22px; color: #FF9F0A; margin-bottom: 6px;"></ion-icon>
                        <div style="font-size: 1.5rem; font-weight: 800; color: #FFF; font-family: ui-rounded, sans-serif;">{{ lpStats.total_physical_wins || 0 }}</div>
                        <div style="font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 4px;">实物掉落</div>
                    </div>
                    <div style="flex: 1; background: rgba(255,255,255,0.12); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 16px; padding: 16px 8px; text-align: center; border: 1px solid rgba(255,255,255,0.15);">
                        <ion-icon name="time-outline" style="font-size: 22px; color: #64D2FF; margin-bottom: 6px;"></ion-icon>
                        <div style="font-size: 1.5rem; font-weight: 800; color: #FFF; font-family: ui-rounded, sans-serif;">{{ mpWarningCount || 0 }}</div>
                        <div style="font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 4px;">等待执行</div>
                    </div>
                    <div style="flex: 1; background: rgba(255,255,255,0.12); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 16px; padding: 16px 8px; text-align: center; border: 1px solid rgba(255,255,255,0.15);">
                        <ion-icon name="layers-outline" style="font-size: 22px; color: #BF5AF2; margin-bottom: 6px;"></ion-icon>
                        <div style="font-size: 1.5rem; font-weight: 800; color: #FFF; font-family: ui-rounded, sans-serif;">{{ mpTotalQuantity || 0 }}</div>
                        <div style="font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 4px;">累计记录</div>
                    </div>
                </div>
            </div>
        </div>

        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding: 0 4px;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.25rem; font-weight: bold; color: var(--text-main);">收益排行</span>
                    <div class="nav-icon-pure" style="margin-left: 12px;" @click="hideNicknames = !hideNicknames">
                        <ion-icon :name="hideNicknames ? 'eye-off-outline' : 'eye-outline'" style="font-size: 20px;"></ion-icon>
                    </div>
                </div>
                <span style="font-size: 11px; color: var(--text-sub); font-family: 'PingFang SC', 'SFMono-Regular', monospace; cursor: pointer; padding: 4px 8px; background: rgba(0,0,0,0.04); border-radius: 6px; font-weight: 500; transition: 0.2s;"
                    v-if="lpStats.date_range" @click="cycleDisplayTime">
                    {{ getDisplayTime() }}
                </span>
            </div>
            <div class="neon-card" style="margin-top: 0; padding: 16px 4px;">
                <div v-for="(user, i) in lpStats.rank_list" :key="i" class="item-row" style="padding: 14px 0;">
                    <div style="flex: 1; overflow: hidden; padding-right: 12px;">
                        <div style="font-weight: 500; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 14px;">
                            {{ hideNicknames ? '***' : user.nickname }}
                            <span v-if="user.node_name" style="font-size: 11px; color: var(--primary); background: var(--primary-shadow); padding: 2px 6px; border-radius: 6px; margin-left: 6px; vertical-align: middle;">{{ user.node_name }}</span>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="color: var(--text-sub); font-size: 13px; font-weight: 500; margin-right: 16px;">{{ user.win_times }} 次</span>
                        <span style="color: var(--primary); font-size: 18px; font-weight: bold; min-width: 40px; text-align: right;">{{ user.win_sum }}</span>
                    </div>
                </div>
                <div v-if="!lpStats.rank_list || lpStats.rank_list.length===0" style="text-align: center; color: var(--text-sub); padding: 30px 0;">暂无产出数据</div>
            </div>
        </div>

        <CustomModal v-model:show="showAddRecord" :title="mpForm.isReset ? '本轮一键结算' : '新增收益记录'">
            <form @submit.prevent="mpAddRecord">
                <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px;">
                    <div style="background: var(--app-bg); border-radius: 12px; padding: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                        <label style="font-size: 12px; color: var(--text-sub); font-weight: 500; margin-bottom: 2px;">本轮时间</label>
                        <input type="datetime-local" v-model="mpForm.date" max="2099-12-31T23:59" required
                            style="background: transparent; border: none; width: 100%; font-size: 18px; font-weight: 700; color: var(--text-main); text-align: center; outline: none; font-family: -apple-system, sans-serif; padding: 0; box-sizing: border-box;">
                    </div>
                    <div style="background: var(--app-bg); border-radius: 12px; padding: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                        <label style="font-size: 12px; color: var(--text-sub); font-weight: 500; margin-bottom: 2px;">下轮预计 (+{{ mpSettings.interval_hours }}h)</label>
                        <input type="datetime-local" :value="mpNextRoundPreviewT" disabled class="ios-input"
                            style="background: transparent; border: none; width: 100%; height: auto; font-size: 18px; font-weight: 700; text-align: center; padding: 0; margin: 0;">
                    </div>
                </div>

                <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                    <div style="flex: 1;">
                        <label style="font-size: 12px; color: var(--text-sub); font-weight: 600; margin-left: 4px; margin-bottom: 6px; display: block;">结算来源节点</label>
                        <select v-model="mpForm.deviceId" @change="updateBaseQuantity" class="ios-select" style="border: none; background: var(--app-bg); width: 100%;" required>
                            <option v-for="node in nodeList" :key="node.device_id" :value="node.device_id">{{ node.nickname }}</option>
                            <option v-if="!nodeList || nodeList.length === 0" value="" disabled>暂无节点</option>
                        </select>
                    </div>
                    <div style="flex: 1;">
                        <label style="font-size: 12px; color: var(--text-sub); font-weight: 600; margin-left: 4px; margin-bottom: 6px; display: block;">结算至分组</label>
                        <select v-model="mpForm.group" class="ios-select" style="border: none; background: var(--app-bg); width: 100%;" required>
                            <option v-for="item in mpItems" :key="item.id" :value="item.name">{{ item.name }}</option>
                            <option v-if="!mpItems || mpItems.length === 0" value="" disabled>请先添加</option>
                        </select>
                    </div>
                </div>

                <div style="background: var(--app-bg); border-radius: 12px; padding: 12px 8px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; text-align: center;">
                    <div style="flex: 1;">
                        <label style="font-size: 11px; color: var(--text-sub); font-weight: 600; margin-bottom: 4px; display: block;">提取总数</label>
                        <input type="number" v-model.number="mpForm.baseQuantity" class="ios-input" style="border: none; background: transparent; text-align: center; padding: 0; height: 36px; font-size: 18px; font-weight: bold; color: var(--text-main);" placeholder="0" required>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: center; padding-top: 15px;">
                        <ion-icon name="remove" style="color: var(--text-sub); font-size: 16px;"></ion-icon>
                    </div>
                    <div style="flex: 1;">
                        <label style="font-size: 11px; color: var(--ios-orange); font-weight: 600; margin-bottom: 4px; display: block;">消耗数量</label>
                        <input type="number" v-model.number="mpForm.cost" class="ios-input" style="border: none; background: transparent; text-align: center; padding: 0; height: 36px; font-size: 18px; font-weight: bold; color: var(--ios-orange);" placeholder="0" required>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: center; padding-top: 15px; font-weight: bold; color: var(--text-sub); font-size: 16px; margin: 0 4px;">=</div>
                    <div style="flex: 1;">
                        <label style="font-size: 11px; color: var(--primary); font-weight: 600; margin-bottom: 4px; display: block;">实际数量</label>
                        <div style="height: 36px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; color: var(--primary); font-family: ui-rounded, sans-serif;">
                            {{ (mpForm.baseQuantity || 0) - (mpForm.cost || 0) }}
                        </div>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <button type="submit" class="ios-btn-primary" :class="{loading: isSubmitting}">
                        <ion-icon v-if="!isSubmitting" name="checkmark-circle" style="font-size: 22px; margin-right: 8px;"></ion-icon>
                        <ion-icon v-else name="sync" class="spin" style="font-size: 22px; margin-right: 8px;"></ion-icon>
                        <span>确认结算</span>
                    </button>
                    <button type="button" v-if="mpForm.isReset" class="ios-btn-primary ios-btn-secondary" style="color: var(--danger); border-color: var(--danger);" @click="pureResetRound">
                        <ion-icon name="trash-bin-outline" style="font-size: 20px; margin-right: 6px;"></ion-icon>不记录本轮数据并重置
                    </button>
                </div>
            </form>
        </CustomModal>

        <CustomModal v-model:show="unparsedViewModal.show">
            <template #title>
                <div style="color: var(--danger); display: flex; align-items: center;">
                    <ion-icon name="search-outline" style="margin-right: 8px; font-size: 22px;"></ion-icon>被拦截的数据透视
                </div>
            </template>
            <div style="font-size: 13px; color: var(--text-sub); margin-bottom: 12px; line-height: 1.5;">
                以下是最近一次被拦截的日志原始内容。请仔细鉴别它是有效的新格式，还是无用的系统提示：
            </div>
            <textarea class="ios-input" style="width: 100%; min-height: 180px; resize: none; background: var(--app-bg); border: 1px solid var(--border-color); font-family: monospace; font-size: 12px; line-height: 1.5; padding: 12px; margin-bottom: 20px; white-space: pre-wrap; overflow-x: auto; box-sizing: border-box;" readonly>{{ unparsedViewModal.content }}</textarea>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <button class="ios-btn-primary" style="height: 44px;" @click="jumpToCreateParser">👉 提取此数据，生成新的解析引擎</button>
                <button class="ios-btn-primary ios-btn-secondary" style="height: 44px; color: var(--danger); border-color: var(--danger);" @click="clearUnparsedQueue">🗑️ 鉴定为无用垃圾，彻底销毁</button>
            </div>
        </CustomModal>

    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useMainStore, getLocalISOTime } from '../store.js';

import CustomModal from '../components/CustomModal.vue';
import NodeSelector from '../components/NodeSelector.vue';

const router = useRouter();
const globalState = useMainStore();

const lpStats = computed(() => globalState.lpStats);
const nodeList = computed(() => globalState.nodeList);
const globalNodeFilter = computed({
    get: () => globalState.globalNodeFilter,
    set: (val) => { globalState.globalNodeFilter = val; }
});
const mpSettings = computed(() => globalState.mpSettings);
const mpItems = computed(() => globalState.mpItems);

const hideNicknames = ref(false);
const timeDisplayIndex = ref(0);

const cycleDisplayTime = () => {
    if (globalNodeFilter.value === 'ALL' && lpStats.value.all_ranges && lpStats.value.all_ranges.length > 1) {
        timeDisplayIndex.value = (timeDisplayIndex.value + 1) % lpStats.value.all_ranges.length;
    }
};

const getDisplayTime = () => {
    if (globalNodeFilter.value !== 'ALL') return lpStats.value.date_range;
    if (lpStats.value.all_ranges && lpStats.value.all_ranges.length > 0) return lpStats.value.all_ranges[timeDisplayIndex.value];
    return lpStats.value.date_range;
};

watch(globalNodeFilter, () => { 
    timeDisplayIndex.value = 0; 
    globalState.loadLpData(); 
});

const mpTotalQuantity = computed(() => globalState.mpRecords.reduce((sum, r) => sum + parseInt(r.quantity || 0), 0));
const mpLatestRecordIds = computed(() => {
    const latest = new Set(); const seen = new Set();
    globalState.mpRecords.forEach(r => { if (!seen.has(r.group)) { seen.add(r.group); latest.add(r.id); } });
    return latest;
});
const mpWarningCount = computed(() => {
    let count = 0;
    globalState.mpRecords.forEach(r => {
        if (mpLatestRecordIds.value.has(r.id) && r.next_time && r.next_time !== '--') {
            if (new Date(r.next_time.replace(' ', 'T') + ':00') <= globalState.nowTime) count++;
        }
    });
    return count;
});

const unparsedViewModal = ref({ show: false, content: '' });

const viewUnparsedLogs = () => {
    unparsedViewModal.value.content = lpStats.value.latest_unparsed_sample || '暂无样本数据';
    unparsedViewModal.value.show = true;
};

const clearUnparsedQueue = async () => {
    if (!confirm("确定要彻底丢弃集群中所有被拦截的未知数据吗？\n清空后红色预警将立即解除！此操作不可恢复。")) return;
    try {
        await axios.post('/api/clear_unparsed');
        unparsedViewModal.value.show = false;
        globalState.loadLpData();
    } catch (e) { alert("清空操作失败"); }
};

const jumpToCreateParser = () => {
    unparsedViewModal.value.show = false;
    router.push('/settings'); 
};

const showAddRecord = ref(false);
const isSubmitting = ref(false);
const mpForm = ref({ date: '', group: '', deviceId: 'ALL', baseQuantity: 0, cost: 0, isReset: false });

const mpNextRoundPreviewT = computed(() => {
    if (!mpForm.value.date) return '';
    const d = new Date(mpForm.value.date);
    d.setHours(d.getHours() + parseInt(mpSettings.value.interval_hours));
    if (isNaN(d)) return '';
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0') + 'T' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
});

const updateBaseQuantity = () => {
    let sum = 0;
    if (lpStats.value.rank_list) {
        lpStats.value.rank_list.forEach(r => {
            if (r.device_id === mpForm.value.deviceId) { sum += parseInt(r.win_sum || 0); }
        });
    }
    mpForm.value.baseQuantity = sum;
};

const resetRound = () => {
    mpForm.value.date = getLocalISOTime();
    mpForm.value.deviceId = globalNodeFilter.value !== 'ALL' ? globalNodeFilter.value : (nodeList.value.length > 0 ? nodeList.value[0].device_id : '');
    mpForm.value.cost = 0;
    mpForm.value.isReset = true;
    if (mpItems.value.length > 0 && !mpForm.value.group) mpForm.value.group = mpItems.value[0].name;
    updateBaseQuantity();
    showAddRecord.value = true;
};

const pureResetRound = async () => {
    if (!confirm("确定只清零大屏数据吗？\n本次操作不会生成任何收益记录，纯粹为了重新计算！")) return;
    isSubmitting.value = true;
    try {
        await axios.post('/api/reset_round', { device_id: mpForm.value.deviceId, date: mpForm.value.date || getLocalISOTime() });
        await globalState.loadLpData();
        showAddRecord.value = false;
    } catch (e) { alert("重置失败"); }
    isSubmitting.value = false;
};

const mpAddRecord = async () => {
    isSubmitting.value = true;
    const finalQuantity = parseInt(mpForm.value.baseQuantity || 0) - parseInt(mpForm.value.cost || 0);
    try {
        await axios.post('/api/record', { date: mpForm.value.date, group: mpForm.value.group, quantity: finalQuantity });
        if (mpForm.value.isReset) { await axios.post('/api/reset_round', { device_id: mpForm.value.deviceId, date: mpForm.value.date }); }
        await globalState.fetchMpData();
        await globalState.loadLpData();
        showAddRecord.value = false;
    } catch (e) { alert("保存失败！"); }
    isSubmitting.value = false;
};
</script>

<style scoped>
/* 霓虹全页背景 */
.neon-page {
    min-height: 100vh;
    /* 霓虹渐变背景 - 柔和色系 */
    background: 
        radial-gradient(ellipse at 20% 0%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 0%, rgba(74, 222, 128, 0.1) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 100%, rgba(99, 102, 241, 0.12) 0%, transparent 60%),
        linear-gradient(180deg, #FAFAFA 0%, #F0F0F5 50%, #E8E8F0 100%);
    padding-bottom: 80px;
}

/* 霓虹英雄区 */
.neon-hero-section {
    /* 赛博朋克霓虹渐变 */
    background: 
        linear-gradient(135deg, 
            #1a1a2e 0%, 
            #16213e 25%, 
            #1f4068 50%, 
            #2d3a4f 75%, 
            #1a1a2e 100%);
    box-shadow: 
        0 0 60px rgba(99, 102, 241, 0.15),
        0 0 100px rgba(74, 222, 128, 0.08),
        inset 0 1px 0 rgba(255,255,255,0.1);
}

/* 霓虹光晕动画 */
.neon-glow-1 {
    position: absolute;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%);
    top: -80px;
    left: -60px;
    border-radius: 50%;
    animation: float 8s ease-in-out infinite;
}

.neon-glow-2 {
    position: absolute;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(167, 139, 250, 0.35) 0%, transparent 70%);
    top: 20px;
    right: -40px;
    border-radius: 50%;
    animation: float 10s ease-in-out infinite reverse;
}

.neon-glow-3 {
    position: absolute;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(52, 211, 153, 0.25) 0%, transparent 70%);
    bottom: -50px;
    left: 30%;
    border-radius: 50%;
    animation: float 12s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0) scale(1); opacity: 0.8; }
    50% { transform: translateY(-20px) scale(1.1); opacity: 1; }
}

/* 霓虹卡片 - 用于下方列表 */
.neon-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 
        0 4px 24px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
    .neon-page {
        background: 
            radial-gradient(ellipse at 20% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 0%, rgba(74, 222, 128, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 100%, rgba(167, 139, 250, 0.1) 0%, transparent 60%),
            linear-gradient(180deg, #0C0C0E 0%, #141416 50%, #1A1A1C 100%);
    }
    
    .neon-card {
        background: rgba(30, 30, 32, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 
            0 4px 24px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
}
</style>
