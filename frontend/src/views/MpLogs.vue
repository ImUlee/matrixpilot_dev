<template>
    <div>
        <div class="page-header">
            <h1 class="big-title">收益记录</h1>
            <div style="display: flex; gap: 16px; align-items: center;">
                <button class="nav-icon-pure" :class="{'edit-active': mpLogMode === 'edit'}" @click="toggleMpLogMode('edit')" title="编辑记录">
                    <ion-icon name="create-outline" style="font-size: 24px;"></ion-icon>
                </button>
                <button class="nav-icon-pure" :class="{'delete-active': mpLogMode === 'delete'}" @click="toggleMpLogMode('delete')" title="删除记录">
                    <ion-icon name="trash-outline" style="font-size: 24px;"></ion-icon>
                </button>
                <button class="ios-btn-primary" style="height: 36px; width: auto; padding: 0 16px; border-radius: 18px; font-size: 14px; margin-left: 4px;" @click="openAddRecord">
                    <ion-icon name="add" style="font-size: 18px; margin-right: 4px; margin-left: -2px;"></ion-icon>新增
                </button>
            </div>
        </div>

        <div class="apple-card">
            <div style="display: flex; justify-content: space-between; padding: 0 4px 12px 4px; border-bottom: 1px solid var(--border-color); color: var(--text-sub); font-size: 12px; font-weight: 600;">
                <div>分组 / 状态</div>
                <div>本轮产出</div>
            </div>

            <div style="max-height: 63.3vh; overflow-y: auto; padding-top: 8px;">
                <details class="item-row log-details-group" v-for="r in mpRecords" :key="r.id" style="padding: 0; display: block; border-bottom: 1px solid var(--border-color);">
                    <summary class="log-summary" style="align-items: center; display: flex; padding: 14px 4px; cursor: pointer; outline: none; list-style: none;" @click="handleMpLogClick($event, r)">
                        <div class="icon-wrapper-left" style="overflow:hidden; transition:0.3s;" :style="{width: mpLogMode==='delete'?'34px':'0', opacity: mpLogMode==='delete'?'1':'0'}">
                            <div style="width: 22px; height: 22px; background: var(--danger); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;"><div style="width:12px; height:2px; background:white;"></div></div>
                        </div>
                        <div style="flex: 1; overflow: hidden; padding-right: 12px;">
                            <div style="font-weight: 500; color: var(--text-main); text-overflow: ellipsis; overflow: hidden; white-space: nowrap; font-size: 14px;">{{ r.group }}</div>
                            <div v-html="getMpRecordStatusHtml(r)" style="font-size: 12px; color: var(--text-sub); margin-top: 4px;"></div>
                        </div>
                        <div style="display: flex; align-items: center; justify-content: flex-end; max-width: 65%;">
                            <div style="color: var(--primary); text-align: right; word-break: break-word; line-height: 1.4;"><span style="font-size: 16px; font-weight: bold;">{{ r.quantity }}</span></div>
                            <div class="icon-wrapper-right" style="overflow: hidden; transition: 0.3s; display: flex; align-items: center;" :style="{width: mpLogMode==='edit'?'26px':'0', opacity: mpLogMode==='edit'?'1':'0', marginLeft: mpLogMode==='edit'?'8px':'0'}"><ion-icon name="create" style="font-size: 18px; color: var(--primary);"></ion-icon></div>
                        </div>
                    </summary>
                    <div style="padding: 4px 4px 16px 4px;">
                        <div style="background: var(--app-bg); border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 12px;">
                            <div style="display: flex; justify-content: space-between; font-size: 13px;"><span style="color: var(--text-sub);">本轮分组</span><span style="font-weight: 600;">{{ r.group }}</span></div>
                            <div style="display: flex; justify-content: space-between; font-size: 13px;"><span style="color: var(--text-sub);">本轮产出</span><span style="font-weight: 600; font-family: ui-rounded, sans-serif; color: var(--primary);">{{ r.quantity }}</span></div>
                            <div style="display: flex; justify-content: space-between; font-size: 13px;"><span style="color: var(--text-sub);">结束时间</span><span style="font-weight: 600;">{{ r.date }}</span></div>
                            <div style="display: flex; justify-content: space-between; font-size: 13px;"><span style="color: var(--text-sub);">预计下轮</span><span style="font-weight: 600; color: var(--primary);">{{ r.next_time !== '--' ? r.next_time : '暂无' }}</span></div>
                        </div>
                    </div>
                </details>
                <div v-if="!mpRecords || mpRecords.length === 0" style="text-align: center; color: var(--text-sub); padding: 30px 0;">暂无记录</div>
            </div>
        </div>

        <CustomModal v-model:show="mpModal.log.show" title="修改记账数据">
            <form @submit.prevent="saveMpLogEdit">
                <div style="margin-bottom:16px;">
                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; display: block; margin-bottom: 6px;">日期时间</label>
                    <input type="datetime-local" v-model="mpModal.log.date" class="ios-input" style="height: 48px; border: 1px solid var(--border-color);" max="2099-12-31T23:59">
                </div>
                <div style="margin-bottom:24px;">
                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; display: block; margin-bottom: 6px;">数值</label>
                    <input type="number" v-model="mpModal.log.value" class="ios-input" style="height: 48px; border: 1px solid var(--border-color);">
                </div>
                <div style="display: flex; gap: 12px;">
                    <button type="button" class="ios-btn-primary ios-btn-secondary" style="flex: 1;" @click="mpModal.log.show = false">取消</button>
                    <button type="submit" class="ios-btn-primary" style="flex: 1;">保存</button>
                </div>
            </form>
        </CustomModal>

        <CustomModal v-model:show="showAddRecord" title="新增收益记录">
            <form @submit.prevent="mpAddRecord">
                <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px;">
                    <div style="background: var(--app-bg); border-radius: 12px; padding: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                        <label style="font-size: 12px; color: var(--text-sub); font-weight: 500; margin-bottom: 2px;">本轮时间</label>
                        <input type="datetime-local" v-model="mpForm.date" max="2099-12-31T23:59" required style="background: transparent; border: none; width: 100%; font-size: 18px; font-weight: 700; color: var(--text-main); text-align: center; outline: none; font-family: -apple-system, sans-serif; padding: 0; box-sizing: border-box;">
                    </div>
                    <div style="background: var(--app-bg); border-radius: 12px; padding: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                        <label style="font-size: 12px; color: var(--text-sub); font-weight: 500; margin-bottom: 2px;">下轮预计 (+{{ mpSettings.interval_hours }}h)</label>
                        <input type="datetime-local" :value="mpNextRoundPreviewT" disabled class="ios-input" style="background: transparent; border: none; width: 100%; height: auto; font-size: 18px; font-weight: 700; text-align: center; padding: 0; margin: 0;">
                    </div>
                </div>

                <div style="margin-bottom: 24px;">
                    <label style="font-size: 12px; color: var(--text-sub); font-weight: 600; margin-left: 4px; margin-bottom: 6px; display: block;">结算至分组</label>
                    <select v-model="mpForm.group" class="ios-select" style="border: none; background: var(--app-bg); width: 100%;" required>
                        <option v-for="item in mpItems" :key="item.id" :value="item.name">{{ item.name }}</option>
                        <option v-if="!mpItems || mpItems.length === 0" value="" disabled>请先到设置页添加分组</option>
                    </select>
                </div>

                <div style="background: var(--app-bg); border-radius: 12px; padding: 12px 8px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; text-align: center;">
                    <div style="flex: 1;">
                        <label style="font-size: 11px; color: var(--text-sub); font-weight: 600; margin-bottom: 4px; display: block;">提取总数</label>
                        <input type="number" v-model.number="mpForm.baseQuantity" class="ios-input" style="border: none; background: transparent; text-align: center; padding: 0; height: 36px; font-size: 18px; font-weight: bold; color: var(--text-main);" placeholder="0" required>
                    </div>
                </div>
                <button type="submit" class="ios-btn-primary" :class="{loading: isSubmitting}">确认新增</button>
            </form>
        </CustomModal>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useMainStore, getLocalISOTime } from '../store.js';
import CustomModal from '../components/CustomModal.vue';

const globalState = useMainStore(); // 挂载 Pinia

const mpRecords = computed(() => globalState.mpRecords);
const mpSettings = computed(() => globalState.mpSettings);
const mpItems = computed(() => globalState.mpItems);

const mpLogMode = ref('normal');
const mpModal = ref({ log: { show: false, id: null, date: '', value: '' } });

const toggleMpLogMode = (m) => { mpLogMode.value = mpLogMode.value === m ? 'normal' : m; };

const handleMpLogClick = async (e, r) => {
    if (mpLogMode.value === 'edit') {
        e.preventDefault();
        mpModal.value.log = { show: true, id: r.id, date: r.date.replace(' ', 'T'), value: r.quantity };
    } else if (mpLogMode.value === 'delete') {
        e.preventDefault();
        if (confirm('⚠️ 确定彻底删除？')) {
            await axios.delete(`/api/record/${r.id}`);
            globalState.fetchMpData();
        }
    }
};

const saveMpLogEdit = async () => {
    await axios.put(`/api/record/${mpModal.value.log.id}`, { date: mpModal.value.log.date, value: mpModal.value.log.value });
    mpModal.value.log.show = false;
    globalState.fetchMpData();
    mpLogMode.value = 'normal';
};

const mpLatestRecordIds = computed(() => {
    const latest = new Set(); const seen = new Set();
    globalState.mpRecords.forEach(r => { if (!seen.has(r.group)) { seen.add(r.group); latest.add(r.id); } });
    return latest;
});

const getMpRecordStatusHtml = (r) => {
    if (!mpLatestRecordIds.value.has(r.id)) return `<div style="font-size: 12px; color: var(--text-sub); font-weight: 500; margin-top: 2px;">本轮结束：${r.date}</div>`;
    if (r.next_time && r.next_time !== '--') {
        if (new Date(r.next_time.replace(' ', 'T') + ':00') > globalState.nowTime) return `<div style="font-size: 12px; color: var(--success); font-weight: 400; margin-top: 2px;">预计下轮：${r.next_time}</div>`;
        else return `<div style="font-size: 12px; color: var(--ios-orange); font-weight: 400; margin-top: 2px;">上号预警：${r.next_time}</div>`;
    }
    return `<div style="font-size: 12px; color: var(--text-sub); font-weight: 400; margin-top: 2px;">本轮结束：${r.date}</div>`;
};

const showAddRecord = ref(false);
const isSubmitting = ref(false);
const mpForm = ref({ date: '', group: '', baseQuantity: 0 });

const openAddRecord = () => {
    mpForm.value.date = getLocalISOTime();
    mpForm.value.baseQuantity = 0;
    if (globalState.mpItems.length > 0 && !mpForm.value.group) mpForm.value.group = globalState.mpItems[0].name;
    showAddRecord.value = true;
};

const mpNextRoundPreviewT = computed(() => {
    if (!mpForm.value.date) return '';
    const d = new Date(mpForm.value.date);
    d.setHours(d.getHours() + parseInt(globalState.mpSettings.interval_hours));
    if (isNaN(d)) return '';
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0') + 'T' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
});

const mpAddRecord = async () => {
    isSubmitting.value = true;
    try {
        await axios.post('/api/record', { date: mpForm.value.date, group: mpForm.value.group, quantity: mpForm.value.baseQuantity });
        await globalState.fetchMpData();
        showAddRecord.value = false;
    } catch (e) { alert("保存失败！"); }
    isSubmitting.value = false;
};
</script>