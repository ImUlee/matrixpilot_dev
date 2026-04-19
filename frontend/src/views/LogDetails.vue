<template>
    <div>
        <div class="page-header">
            <h1 class="big-title">产出明细</h1>
            <div style="display: flex; gap: 12px; align-items: center;">
                <div class="nav-icon-pure" :class="{'edit-active': lpLogMode === 'edit'}"
                    @click="lpLogMode = lpLogMode === 'edit' ? 'normal' : 'edit'" title="编辑单条记录">
                    <ion-icon name="create-outline"></ion-icon>
                </div>
                <div class="nav-icon-pure" :style="{ color: filterPhysicals ? 'var(--ios-orange)' : 'var(--text-sub)' }"
                    @click="filterPhysicals = !filterPhysicals" title="仅看实物">
                    <ion-icon :name="filterPhysicals ? 'gift' : 'gift-outline'"></ion-icon>
                </div>
            </div>
        </div>

        <div>
            <div class="apple-card">
                <div class="ios-search-bar" style="height: 46px; padding: 0 12px; margin-bottom: 16px; border: 1px solid var(--border-color);">
                    <ion-icon name="search" class="ios-search-icon" style="flex-shrink: 0;"></ion-icon>
                    <select v-model="searchType" style="border:none; background:transparent; color:var(--text-main); font-weight:600; outline:none; -webkit-appearance:none; padding-right:4px; flex-shrink: 0; cursor: pointer;">
                        <option value="nick">昵称</option>
                        <option value="date">日期</option>
                    </select>
                    <ion-icon name="chevron-down" style="font-size: 12px; color: var(--text-sub); margin-right: 8px; flex-shrink: 0; pointer-events: none;"></ion-icon>
                    <div style="width: 1px; height: 16px; background: var(--text-sub); opacity: 0.3; margin-right: 12px; flex-shrink: 0;"></div>
                    <input type="text" class="ios-search-input" placeholder="输入搜索内容..." v-model="searchText" style="flex: 1; min-width: 0; height: 100%; box-sizing: border-box;">
                    <ion-icon name="close-circle" style="color: var(--text-sub); font-size: 18px; opacity: 0.6; cursor: pointer; flex-shrink: 0;" v-show="searchText" @click="searchText = ''"></ion-icon>
                </div>

                <div style="display: flex; justify-content: space-between; padding: 0 4px 12px 4px; border-bottom: 1px solid var(--border-color); color: var(--text-sub); font-size: 12px; font-weight: 600;">
                    <div style="display: flex; align-items: center;">昵称 / 日期 
                        <ion-icon :name="hideNicknames ? 'eye-off-outline' : 'eye-outline'" style="font-size: 14px; margin-left: 6px; cursor: pointer;" @click="hideNicknames = !hideNicknames"></ion-icon>
                    </div>
                    <div>明细</div>
                </div>

                <div style="max-height: 56vh; overflow-y: auto; padding-top: 8px;">
                    <div class="item-row" v-for="item in filteredDetails" :key="item.id"
                        style="align-items: center; display: flex; padding: 14px 4px; cursor: pointer;"
                        @click="handleLpLogClick(item)">
                        <div style="flex: 1; overflow: hidden; padding-right: 12px;">
                            <div style="font-weight: 500; color: var(--text-main); text-overflow: ellipsis; overflow: hidden; white-space: nowrap; font-size: 14px;">
                                {{ hideNicknames ? '***' : item.nickname }}
                                <span v-if="item.node_name" style="font-size: 11px; color: var(--primary); background: var(--primary-shadow); padding: 2px 6px; border-radius: 6px; margin-left: 6px; vertical-align: middle;">{{ item.node_name }}</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-sub); margin-top: 4px;">
                                {{ formatShortDate(item.log_time) }}
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; justify-content: flex-end; max-width: 65%;">
                            <div style="color: var(--primary); text-align: right; word-break: break-word; line-height: 1.4;">
                                <span v-if="item.item_type === '钻石' || item.item_type === '动态'" style="font-size: 16px; font-weight: bold;">{{ item.quantity }}</span>
                                <span v-else style="font-size: 13px; font-weight: 600;">{{ item.item_type }}</span>
                            </div>
                            <div style="overflow: hidden; transition: 0.3s; display: flex; align-items: center;"
                                :style="{width: lpLogMode==='edit'?'26px':'0', opacity: lpLogMode==='edit'?'1':'0', marginLeft: lpLogMode==='edit'?'8px':'0'}">
                                <ion-icon name="create" style="font-size: 18px; color: var(--primary);"></ion-icon>
                            </div>
                        </div>
                    </div>
                    <div v-if="!filteredDetails || filteredDetails.length===0" style="text-align: center; color: var(--text-sub); padding: 30px 0;">暂无匹配明细</div>
                </div>
            </div>
        </div>

        <div class="custom-modal-overlay" :class="{active: lpSingleEditModal.show}" :style="{display: lpSingleEditModal.show ? 'flex' : 'none'}" @click="lpSingleEditModal.show = false">
            <div class="pop-in" @click.stop>
                <div style="display:flex; justify-content:space-between; margin-bottom:24px; align-items: center;">
                    <h5 style="font-weight:bold; margin:0; font-size: 20px;">修改单条产出</h5>
                    <ion-icon name="close-circle" style="font-size:28px; color:var(--text-sub); cursor:pointer;" @click="lpSingleEditModal.show = false"></ion-icon>
                </div>
                <div style="margin-bottom:16px;">
                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; display: block; margin-bottom: 6px;">账号 / 时间</label>
                    <input type="text" class="ios-input" style="border: 1px solid var(--border-color); opacity: 0.7; font-size: 14px;"
                        :value="(lpSingleEditModal.data.nickname || '') + ' - ' + formatShortDate(lpSingleEditModal.data.log_time)" disabled>
                </div>
                <div style="margin-bottom:24px;">
                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; display: block; margin-bottom: 6px;">{{ lpSingleEditModal.data.item_type }} 数量</label>
                    <input type="number" class="ios-input" style="border: 1px solid var(--border-color);" v-model.number="lpSingleEditModal.data.quantity">
                </div>
                <div style="display: flex; gap: 12px;">
                    <button class="ios-btn-primary ios-btn-secondary" style="flex: 1;" @click="lpSingleEditModal.show = false">取消</button>
                    <button class="ios-btn-primary" style="flex: 1;" @click="saveLpSingleEdit">保存修改</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useMainStore, formatShortDate } from '../store.js';

const globalState = useMainStore();

// ================= 搜索与显示状态 =================
const searchText = ref("");
const searchType = ref("nick");
const filterPhysicals = ref(false);
const hideNicknames = ref(false);
const lpLogMode = ref('normal');

// ================= 列表过滤计算 =================
const filteredDetails = computed(() => {
    if (!globalState.lpStats.details) return [];
    const rawSearch = searchText.value.trim();
    return globalState.lpStats.details.filter(i => {
        if (filterPhysicals.value && (i.item_type === '钻石' || i.item_type === '动态')) return false;
        if (!rawSearch) return true;
        if (searchType.value === 'nick') return i.nickname.replace(/\s+/g, '').toLowerCase().includes(rawSearch.replace(/\s+/g, '').toLowerCase());
        else return i.log_time.substring(0, 10).replace(/\D/g, '').includes(rawSearch.replace(/\D/g, ''));
    });
});

// ================= 编辑逻辑 =================
const lpSingleEditModal = ref({ show: false, data: {} });

const handleLpLogClick = (item) => {
    if (lpLogMode.value === 'edit') {
        lpSingleEditModal.value.data = { ...item };
        lpSingleEditModal.value.show = true;
    }
};

const saveLpSingleEdit = async () => {
    try {
        await axios.put(`/api/logs/${lpSingleEditModal.value.data.id}`, { quantity: lpSingleEditModal.value.data.quantity });
        lpSingleEditModal.value.show = false;
        lpLogMode.value = 'normal';
        loadLpData();
    } catch (e) { alert("保存失败"); }
};
</script>