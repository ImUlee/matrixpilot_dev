<template>
    <div>
        <div class="page-header">
            <h1 class="big-title">历史记录</h1>
            <div style="display: flex; gap: 12px; align-items: center;">
                <div class="nav-icon-pure"
                    :style="{ color: historyLogsModal.show && historyLogsModal.date === 'all_physicals' ? 'var(--ios-orange)' : 'var(--text-sub)' }"
                    @click="viewAllPhysicals" title="全库实物汇总">
                    <ion-icon :name="historyLogsModal.show && historyLogsModal.date === 'all_physicals' ? 'gift' : 'gift-outline'"></ion-icon>
                </div>
                <div class="nav-icon-pure" @click="hideHistory = !hideHistory">
                    <ion-icon :name="hideHistory ? 'eye-off-outline' : 'eye-outline'"></ion-icon>
                </div>
                <div class="nav-icon-pure" @click="openUserFilter" :class="{ 'edit-active': historyFilterUser }">
                    <ion-icon :name="historyFilterUser ? 'funnel' : 'funnel-outline'"></ion-icon>
                </div>
            </div>
        </div>

        <div>
            <div v-if="historyFilterUser" class="apple-card" style="background: linear-gradient(135deg, rgba(0,122,255,0.08), rgba(52,199,89,0.05)); border: 1px solid rgba(0,122,255,0.15); display: flex; justify-content: space-between; align-items: center; padding: 20px; margin-bottom: 20px;">
                <div style="flex: 1; min-width: 0; padding-right: 15px;">
                    <div style="color: var(--text-sub); font-weight: bold; font-size: 12px;">累计产出</div>
                    <div style="font-size: 16px; font-weight: bold; color: var(--text-main); margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {{ hideNicknames && historyFilterUser !== '【全库时段总和】' ? '***' : historyFilterUser }}
                    </div>
                    <div style="color: var(--text-sub); font-size: 11px; margin-top: 4px; font-family: monospace;">{{ historyFilterDateRange }}</div>
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="color: var(--primary); font-weight: bold; font-size: 2rem; margin-right: 16px; font-family: ui-rounded, sans-serif;">{{ historyFilterTotal }}</span>
                    <div class="nav-icon-pure" @click="clearUserFilter"><ion-icon name="close-circle"></ion-icon></div>
                </div>
            </div>

            <div v-if="!lpStats.history_data || lpStats.history_data.length===0" style="text-align: center; padding: 40px 0; color: var(--text-sub);">暂无历史数据</div>

            <details class="settings-card" v-for="day in lpStats.history_data" :key="day.date" @toggle="e => updateExpandedState(day.date, e.target.open)">
                <summary class="settings-summary" style="height: 60px;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-weight: bold; font-size: 16px; color: var(--text-main);">{{ day.date }}</span>
                        <span v-if="day.date === localToday" style="background: var(--primary); color: #FFF; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 6px; margin-left: 8px;">实时</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="color: var(--primary); font-weight: bold; font-size: 18px; margin-right: 12px;">
                            {{ (hideHistory && !expandedDates[day.date]) ? '***' : ('+' + day.daily_sum) }}
                        </span>
                        <ion-icon name="chevron-down-outline" class="arrow-icon"></ion-icon>
                    </div>
                </summary>
                <div class="details-content" style="padding-top: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px;">
                        <span style="color: var(--text-sub);">参与账号数量</span><span style="font-weight: bold; color: var(--text-main);">{{ day.user_count }}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 20px; font-size: 14px;">
                        <span style="color: var(--text-sub);">当日总产出</span><span style="font-weight: bold; color: var(--text-main);">{{ day.daily_sum }}</span>
                    </div>
                    <button class="ios-btn-primary" style="height: 44px; width: 100%;" @click="viewHistoryLogs(day.date)">查看产出明细</button>
                </div>
            </details>
        </div>

        <CustomModal v-model:show="historyLogsModal.show">
            <template #title>
                <div style="display: flex; align-items: center; font-size: 18px;">
                    <ion-icon v-if="historyLogsModal.date === 'all_physicals'" name="gift" style="color: var(--ios-orange); margin-right: 8px; font-size: 22px; flex-shrink: 0;"></ion-icon>
                    <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px;">{{ historyLogsModal.date === 'all_physicals' ? '全库历史实物' : historyLogsModal.date + ' 明细' }}</span>
                </div>
            </template>

            <template #header-right>
                <div v-if="historyLogsModal.date !== 'all_physicals'" 
                     @click="toggleHistoryFilter" 
                     title="仅看实物"
                     style="display: flex; align-items: center; cursor: pointer; transition: 0.2s;" 
                     :style="{ color: historyLogsModal.filterPhysicals ? 'var(--ios-orange)' : 'var(--text-sub)' }">
                    <ion-icon :name="historyLogsModal.filterPhysicals ? 'gift' : 'gift-outline'" style="font-size: 24px;"></ion-icon>
                </div>
            </template>

            <div style="flex: 1; overflow-y: auto; padding-right: 4px;">
                <div v-if="historyLogsModal.loading" style="text-align: center; padding: 40px 0; color: var(--text-sub);">
                    <ion-icon name="sync" class="spin" style="font-size: 32px; color: var(--primary); margin-bottom: 12px;"></ion-icon>
                    <div style="font-size: 14px;">正在读取底层数据...</div>
                </div>
                <div v-else-if="!filteredHistoryLogs || filteredHistoryLogs.length === 0" style="text-align: center; padding: 40px 0; color: var(--text-sub);">
                    暂无实物或日志记录
                </div>
                <div v-else>
                    <div class="item-row" v-for="(log, idx) in filteredHistoryLogs" :key="idx" style="padding: 12px 12px 12px 0; display: flex; align-items: center; border-bottom: 1px solid var(--border-color);">
                        <div style="flex: 1; overflow: hidden; padding-right: 12px;">
                            <div style="font-weight: 500; color: var(--text-main); text-overflow: ellipsis; overflow: hidden; white-space: nowrap; font-size: 14px;">
                                {{ hideNicknames ? '***' : log.nickname }}
                                <span v-if="log.node_name" style="font-size: 11px; color: var(--primary); background: var(--primary-shadow); padding: 2px 6px; border-radius: 6px; margin-left: 6px; vertical-align: middle;">{{ log.node_name }}</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-sub); margin-top: 4px;">{{ formatShortDate(log.log_time) }}</div>
                        </div>
                        <div style="color: var(--primary); text-align: right; max-width: 65%; word-break: break-word; line-height: 1.4;">
                            <span v-if="log.item_type === '钻石' || log.item_type === '动态'" style="font-size: 16px; font-weight: bold;">{{ log.quantity }}</span>
                            <span v-else style="font-size: 13px; font-weight: 600;">{{ log.item_type }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="userFilterModal.show" title="全库深度查询">
            <div style="background: rgba(0,122,255,0.08); color: var(--primary); border-radius: 12px; padding: 12px; text-align: center; font-size: 14px; font-weight: bold; cursor: pointer; margin-bottom: 16px; flex-shrink: 0;" @click="userFilterModal.showAdvanced = !userFilterModal.showAdvanced">
                <ion-icon :name="userFilterModal.showAdvanced ? 'chevron-up-outline' : 'options-outline'" style="margin-right: 4px; vertical-align: text-bottom;"></ion-icon>
                {{ userFilterModal.showAdvanced ? '收起高级筛选' : '高级筛选 (无视节点 / 搜索)' }}
            </div>
            
            <div v-show="userFilterModal.showAdvanced" style="background: var(--app-bg); border-radius: 16px; padding: 16px; margin-bottom: 16px; border: 1px solid var(--border-color); flex-shrink: 0; width: 100%; box-sizing: border-box;">
                <div style="display: flex; flex-direction: column; gap: 12px; width: 100%; box-sizing: border-box;">
                    <input type="text" class="ios-input" style="height: 44px; width: 100%; border: 1px solid var(--border-color); padding: 0 12px; box-sizing: border-box;" placeholder="起始时间 (可选)" onfocus="this.type='datetime-local'" onblur="if(!this.value) this.type='text'" v-model="userFilterModal.startDate">
                    <input type="text" class="ios-input" style="height: 44px; width: 100%; border: 1px solid var(--border-color); padding: 0 12px; box-sizing: border-box;" placeholder="结束时间 (可选)" onfocus="this.type='datetime-local'" onblur="if(!this.value) this.type='text'" v-model="userFilterModal.endDate">
                    <div style="display: flex; gap: 10px; align-items: center; width: 100%; box-sizing: border-box;">
                        <div class="ios-search-bar" style="margin: 0; flex: 1; min-width: 0; height: 44px; border: 1px solid var(--border-color); background: var(--card-bg); padding: 0 12px; box-sizing: border-box;">
                            <ion-icon name="search" class="ios-search-icon" style="flex-shrink: 0;"></ion-icon>
                            <input type="text" class="ios-search-input" style="flex: 1; min-width: 0; padding: 0; height: 100%; box-sizing: border-box;" placeholder="全局跨节点搜索..." v-model="userFilterModal.searchText" @keyup.enter="executeSearch">
                            <ion-icon name="close-circle" style="color:var(--text-sub); font-size:16px; opacity:0.6; cursor: pointer; flex-shrink: 0;" v-show="userFilterModal.searchText" @click="userFilterModal.searchText = ''"></ion-icon>
                        </div>
                        <button class="ios-btn-primary" style="width: 72px; padding: 0; height: 44px; border-radius: 12px; flex-shrink: 0; margin: 0; box-sizing: border-box;" @click="executeSearch">查询</button>
                    </div>
                </div>
            </div>

            <div style="font-size: 12px; color: var(--text-sub); font-weight: bold; margin-bottom: 8px; flex-shrink: 0;">全库名单</div>
            <div style="flex: 1; overflow-y: auto; padding-right: 4px;">
                <div v-if="userFilterModal.loading" style="text-align: center; padding: 30px 0; color: var(--text-sub);">加载全库数据中...</div>
                <div v-else-if="!filteredUserList || filteredUserList.length === 0" style="text-align: center; padding: 30px 0; color: var(--text-sub);">全库无此账号</div>
                <div v-for="user in filteredUserList" :key="user" class="item-row" style="padding: 12px 12px 12px 0; border-bottom: 1px solid var(--border-color);" @click="applyUserFilter(user)">
                    <span style="font-weight: 500; color: var(--text-main); cursor: pointer;">{{ hideNicknames ? '***' : user }}</span>
                    <ion-icon name="chevron-forward" style="font-size: 16px; color: var(--text-sub);"></ion-icon>
                </div>
            </div>
        </CustomModal>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useMainStore, formatShortDate } from '../store.js';

import CustomModal from '../components/CustomModal.vue';

const globalState = useMainStore();
const localToday = computed(() => globalState.localToday);

const lpStats = computed(() => globalState.lpStats);
const hideHistory = ref(false);
const hideNicknames = ref(false);
const expandedDates = ref({});

const historyLogsModal = ref({ show: false, loading: false, date: "", logs: [], filterPhysicals: false });

const filteredHistoryLogs = computed(() => {
    if (!historyLogsModal.value.logs) return [];
    if (historyLogsModal.value.filterPhysicals && historyLogsModal.value.date !== 'all_physicals') {
        return historyLogsModal.value.logs.filter(l => l.item_type !== '钻石' && l.item_type !== '动态');
    }
    return historyLogsModal.value.logs;
});

const viewHistoryLogs = async (date) => {
    historyLogsModal.value.date = date;
    historyLogsModal.value.show = true;
    historyLogsModal.value.loading = true;
    historyLogsModal.value.logs = [];
    if (date !== 'all_physicals') historyLogsModal.value.filterPhysicals = false;
    try {
        const res = await axios.get(`/api/history_logs?date=${date}`);
        historyLogsModal.value.logs = res.data.logs;
    } catch (e) {} finally { historyLogsModal.value.loading = false; }
};

const viewAllPhysicals = () => viewHistoryLogs('all_physicals');
const toggleHistoryFilter = () => { historyLogsModal.value.filterPhysicals = !historyLogsModal.value.filterPhysicals; };
const updateExpandedState = (date, isOpen) => { expandedDates.value[date] = isOpen; };

const historyFilterUser = ref("");
const historyFilterTotal = ref(0);
const historyFilterDateRange = ref("");
const userFilterModal = ref({ show: false, showAdvanced: false, loading: false, users: [], searchText: "", startDate: "", endDate: "" });

const filteredUserList = computed(() => {
    const raw = userFilterModal.value.searchText.trim().toLowerCase();
    if (!raw) return userFilterModal.value.users;
    return userFilterModal.value.users.filter(u => u.toLowerCase().includes(raw));
});

const openUserFilter = async () => {
    userFilterModal.value.show = true;
    userFilterModal.value.showAdvanced = false;
    userFilterModal.value.searchText = "";
    if (userFilterModal.value.users.length === 0) {
        userFilterModal.value.loading = true;
        try { const res = await axios.get(`/api/user_total?global=1`); userFilterModal.value.users = res.data.users || []; } catch (e) {} finally { userFilterModal.value.loading = false; }
    }
};

const executeSearch = () => {
    const raw = userFilterModal.value.searchText.trim();
    if (!raw) {
        if (!userFilterModal.value.startDate && !userFilterModal.value.endDate) return alert("全库范围查询请至少设置时间范围！");
        queryAllUsers();
    } else { applyUserFilter(raw); }
};

const queryAllUsers = async () => {
    historyFilterUser.value = "【全库时段总和】"; userFilterModal.value.show = false; historyFilterTotal.value = "...";
    let ds = userFilterModal.value.startDate, de = userFilterModal.value.endDate;
    let query = `/api/user_total?global=1&calc_all=1`;
    if (ds) query += `&start_date=${ds}`; if (de) query += `&end_date=${de}`;
    historyFilterDateRange.value = `${ds ? ds.replace('T', ' ') : '最早期'} 至 ${de ? de.replace('T', ' ') : '最新'} (全库检索)`;
    try { const res = await axios.get(query); historyFilterTotal.value = res.data.total || 0; } catch (e) { historyFilterTotal.value = 0; }
};

const applyUserFilter = async (nickname) => {
    historyFilterUser.value = nickname; userFilterModal.value.show = false; historyFilterTotal.value = "...";
    let ds = userFilterModal.value.startDate, de = userFilterModal.value.endDate;
    let query = `/api/user_total?nickname=${encodeURIComponent(nickname)}&global=1`;
    if (ds) query += `&start_date=${ds}`; if (de) query += `&end_date=${de}`;
    historyFilterDateRange.value = (!ds && !de) ? "所有时间 (全库检索)" : `${ds ? ds.replace('T', ' ') : '早期'} 至 ${de ? de.replace('T', ' ') : '最新'} (全库检索)`;
    try { const res = await axios.get(query); historyFilterTotal.value = res.data.total || 0; } catch (e) { historyFilterTotal.value = 0; }
};

const clearUserFilter = () => { historyFilterUser.value = ""; historyFilterTotal.value = 0; };
</script>