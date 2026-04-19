<template>
    <Teleport to="body">
        <div class="custom-modal-overlay" :class="{ active: show }" :style="{ display: show ? 'flex' : 'none' }" @click="closeModal">
            <div class="pop-in" @click.stop :style="{ maxWidth: width, maxHeight: '85vh', display: 'flex', flexDirection: 'column' }">
                
                <div style="display:flex; justify-content:space-between; margin-bottom:20px; align-items: center; flex-shrink: 0;">
                    <h5 style="font-weight:bold; margin:0; font-size: 20px;">
                        <slot name="title">{{ title }}</slot>
                    </h5>
                    
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <slot name="header-right"></slot>
                        <ion-icon name="close-circle" style="font-size:28px; color:var(--text-sub); cursor:pointer; transition: 0.2s;" @click="closeModal" class="modal-close-btn"></ion-icon>
                    </div>
                </div>
                
                <div style="flex: 1; overflow-y: auto; padding-right: 4px; margin-right: -4px;">
                    <slot></slot>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
const props = defineProps({
    show: { type: Boolean, default: false },   
    title: { type: String, default: '提示' },  
    width: { type: String, default: '400px' }  
});

const emit = defineEmits(['update:show', 'close']);

const closeModal = () => {
    emit('update:show', false);
    emit('close');
};
</script>

<style scoped>
.modal-close-btn:hover { opacity: 0.7; }
</style>