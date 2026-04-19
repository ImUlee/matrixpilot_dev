<template>
    <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center; overflow: hidden; height: 36px; margin-left: 8px;">
        <div v-if="isOpen" style="display: flex; overflow-x: auto; scrollbar-width: none; -ms-overflow-style: none; align-items: center; gap: 8px; max-width: 100%; padding: 0 4px;">
            <div style="flex-shrink: 0; padding: 4px 14px; border-radius: 14px; font-size: 13px; font-weight: bold; cursor: pointer; white-space: nowrap;"
                :style="{ background: modelValue === 'ALL' ? 'var(--primary)' : 'var(--app-bg)', color: modelValue === 'ALL' ? '#fff' : 'var(--text-sub)' }"
                @click="selectNode('ALL')">全部</div>

            <div v-for="node in nodeList" :key="node.device_id"
                style="flex-shrink: 0; padding: 4px 14px; border-radius: 14px; font-size: 13px; font-weight: bold; cursor: pointer; white-space: nowrap;"
                :style="{ background: modelValue === node.device_id ? 'var(--primary)' : 'var(--app-bg)', color: modelValue === node.device_id ? '#fff' : 'var(--text-sub)' }"
                @click="selectNode(node.device_id)">{{ node.nickname }}
            </div>
        </div>
        
        <div v-else @click="isOpen = true"
            style="border: 1.5px solid var(--primary); border-radius: 14px; padding: 4px 12px; color: var(--primary); font-weight: bold; font-size: 13px; display: flex; align-items: center; gap: 6px; cursor: pointer; white-space: nowrap; max-width: 100%; background: transparent;">
            <span style="overflow: hidden; text-overflow: ellipsis;">
                {{ modelValue === 'ALL' ? '全部' : (nodeList.find(n => n.device_id === modelValue)?.nickname || '未知节点') }}
            </span>
            <ion-icon name="swap-horizontal" style="font-size: 14px; flex-shrink: 0;"></ion-icon>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// 接收父组件传来的当前选中值和节点列表
const props = defineProps({
    modelValue: { type: String, required: true },
    nodeList: { type: Array, default: () => [] }
});

// 定义向父组件派发的事件 (支持 v-model)
const emit = defineEmits(['update:modelValue', 'change']);

const isOpen = ref(false);

const selectNode = (id) => {
    emit('update:modelValue', id); // 更新 v-model
    emit('change', id);            // 触发额外 change 事件用于重新拉取数据
    isOpen.value = false;
};
</script>