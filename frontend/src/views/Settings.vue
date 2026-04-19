<template>
    <div>
        <div class="page-header">
            <h1 class="big-title">配置</h1>
        </div>

        <div class="section-header">数据管理</div>
        <div class="settings-card" style="padding: 0 20px; margin-bottom: 24px;">
            <div class="item-row" @click="openSetting('group')" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="cube-outline" style="font-size: 20px; color: var(--ios-orange); margin-right: 10px;"></ion-icon>管理分组
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 14px; color: var(--text-sub);">{{ mpItems ? mpItems.length : 0 }} 个</span>
                    <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
                </div>
            </div>
            
            <div class="item-row" @click="openSetting('interval')" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="time-outline" style="font-size: 20px; color: var(--success); margin-right: 10px;"></ion-icon>时间周期
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 14px; color: var(--text-sub);">{{ mpSettings.interval_hours }}h</span>
                    <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
                </div>
            </div>

            <div class="item-row" @click="openAccountManage" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="people-outline" style="font-size: 20px; color: var(--primary); margin-right: 10px;"></ion-icon>账号管理
                </div>
                <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
            </div>

            <div class="item-row" @click="openSetting('faq')" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="chatbubbles-outline" style="font-size: 20px; color: #5AC8FA; margin-right: 10px;"></ion-icon>FAQ 配置
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 14px; color: var(--text-sub);">{{ settingsForm.faqList ? settingsForm.faqList.length : 0 }} 条</span>
                    <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
                </div>
            </div>

            <div class="item-row" @click="openSetting('parsers')" style="height: 54px; border-bottom: none;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="color-wand-outline" style="font-size: 20px; color: #AF52DE; margin-right: 10px;"></ion-icon>自定义规则
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 14px; color: var(--text-sub);">{{ settingsForm.customParsers ? settingsForm.customParsers.length : 0 }} 个引擎</span>
                    <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
                </div>
            </div>
        </div>

        <div class="section-header">节点通知</div>
        <div class="settings-card" style="padding: 0 20px; margin-bottom: 24px;">
            <div class="item-row" @click="openSetting('nodes')" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="server-outline" style="font-size: 20px; color: var(--primary); margin-right: 10px;"></ion-icon>节点状态
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="status-badge" :class="onlineNodesCount > 0 ? 'status-running' : 'status-offline'" style="padding: 0; background: transparent; margin-right: -4px;">
                        <div class="static-dot" style="margin:0; width: 8px; height: 8px;" :style="{ background: onlineNodesCount > 0 ? 'var(--success)' : 'var(--text-sub)' }"></div>
                    </div>
                    <span style="font-size: 14px; color: var(--text-sub);">{{ onlineNodesCount }} / {{ nodeList ? nodeList.length : 0 }} 在线</span>
                    <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
                </div>
            </div>

            <div class="item-row" @click="openSetting('download')" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="cloud-download-outline" style="font-size: 20px; color: #34C759; margin-right: 10px;"></ion-icon>客户端下载
                </div>
                <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
            </div>

            <div class="item-row" @click="openSetting('bark')" style="height: 54px; border-bottom: none;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main); flex: 1;">
                    <ion-icon name="paper-plane-outline" style="font-size: 20px; color: var(--danger); margin-right: 10px;"></ion-icon>Bark API 配置
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 14px;" :style="{color: mpSettings.bark_enabled ? 'var(--success)' : 'var(--text-sub)'}">{{ mpSettings.bark_enabled ? '已启用' : (mpSettings.bark_url ? '未启用' : '未配置') }}</span>
                    <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
                </div>
            </div>
        </div>

        <div class="section-header">其他操作</div>
        <div class="settings-card" style="padding: 0 20px;">
            <div class="item-row" @click="copySearchUrl" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main);">
                    <ion-icon name="copy-outline" style="font-size: 20px; color: var(--primary); margin-right: 10px;"></ion-icon>复制查询页面并跳转
                </div>
                <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
            </div>
            
            <div class="item-row" @click="showPwaGuide" style="height: 54px;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--text-main);">
                    <ion-icon name="share-outline" style="font-size: 20px; color: var(--primary); margin-right: 10px;"></ion-icon>添加到主屏幕 (PWA)
                </div>
                <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
            </div>
            
            <a href="/logout" class="item-row" style="text-decoration: none; height: 54px; border-bottom: none; margin-bottom: 0;">
                <div style="display: flex; align-items: center; font-size: 15px; color: var(--danger);">
                    <ion-icon name="log-out-outline" style="font-size: 20px; color: var(--danger); margin-right: 10px;"></ion-icon>退出当前账号
                </div>
                <ion-icon name="chevron-forward" style="color: var(--text-sub); font-size: 16px; opacity: 0.3;"></ion-icon>
            </a>
        </div>

        <div style="text-align: center; margin-top: 35px; margin-bottom: 10px;">
            <span style="color: var(--text-sub); font-size: 13px; font-weight: 500; padding: 6px 16px; background: rgba(0,0,0,0.03); border-radius: 16px;">MatrixPilot UI</span>
        </div>

        <CustomModal v-model:show="settingModals.group" title="管理分组">
            <form @submit.prevent="saveSettings('add_item')" class="compact-input-group" style="margin-bottom: 16px;">
                <input type="text" v-model="settingsForm.newItemName" placeholder="新分组名称" required class="ios-input" style="flex: 1; border: none; background: var(--app-bg); height: 44px; border-radius: 12px;">
                <button type="submit" class="ios-btn-primary ios-btn-secondary" style="height: 44px; width: 80px; flex-shrink: 0; padding: 0; border-radius: 12px;">添加</button>
            </form>
            <div style="background: var(--app-bg); border-radius: 12px; overflow: hidden; padding: 0 16px; border: none;">
                <div class="item-row" v-for="(item, index) in mpItems" :key="item.id" style="height: 46px; display: flex; align-items: center; justify-content: space-between; padding: 0 8px;" :style="{ borderBottom: index === mpItems.length - 1 ? 'none' : '' }">
                    <div style="flex: 1; font-size: 14px; font-weight: 400; color: var(--text-main); cursor: pointer;" @click="openGroupModal(item)">{{ item.name }}</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <ion-icon name="chevron-up-outline" style="font-size: 18px; color: var(--primary); cursor: pointer;" :style="{ opacity: index === 0 ? '0.2' : '1', pointerEvents: index === 0 ? 'none' : 'auto' }" @click.stop="moveItem(index, -1)"></ion-icon>
                        <ion-icon name="chevron-down-outline" style="font-size: 18px; color: var(--primary); cursor: pointer;" :style="{ opacity: index === mpItems.length - 1 ? '0.2' : '1', pointerEvents: index === mpItems.length - 1 ? 'none' : 'auto' }" @click.stop="moveItem(index, 1)"></ion-icon>
                        <ion-icon name="chevron-forward-outline" style="color: var(--text-sub); font-size: 16px; margin-left: 4px; opacity: 0.5;" @click.stop="openGroupModal(item)"></ion-icon>
                    </div>
                </div>
                <div v-if="!mpItems || mpItems.length === 0" style="text-align: center; padding: 20px 0; color: var(--text-sub); font-size: 13px;">暂无分组</div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="settingModals.interval" title="时间周期">
            <div style="font-size: 13px; color: var(--text-sub); margin-bottom: 16px;">设置每轮记录默认递增的小时数：</div>
            <form @submit.prevent="saveSettings('update_interval')" class="compact-input-group">
                <input type="number" v-model="settingsForm.interval_hours" required class="ios-input" style="flex: 1; border: none; background: var(--app-bg); height: 44px; border-radius: 12px;">
                <button type="submit" class="ios-btn-primary ios-btn-secondary" style="height: 44px; width: 80px; flex-shrink: 0; padding: 0; border-radius: 12px;">保存</button>
            </form>
        </CustomModal>

        <CustomModal v-model:show="settingModals.faq" title="FAQ 配置" width="500px">
            <div v-for="(item, index) in settingsForm.faqList" :key="index" style="background: var(--app-bg); border-radius: 12px; padding: 12px; margin-bottom: 12px; display: flex; flex-direction: column; gap: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div @click="openIconPicker(index)" style="width: 44px; height: 44px; border: 1px solid var(--border-color); border-radius: 10px; display: flex; align-items: center; justify-content: center; background: var(--card-bg); cursor: pointer; flex-shrink: 0;">
                        <ion-icon :name="item.icon || 'help-circle-outline'" style="font-size: 24px; color: var(--primary);"></ion-icon>
                    </div>
                    <div style="height: 44px; display: flex; gap: 6px; align-items: center; flex-shrink: 0;">
                        <ion-icon name="arrow-up-circle" style="font-size: 24px; color: var(--primary); cursor: pointer;" :style="{ opacity: index === 0 ? '0.2' : '1', pointerEvents: index === 0 ? 'none' : 'auto' }" @click="moveFaq(index, -1)"></ion-icon>
                        <ion-icon name="arrow-down-circle" style="font-size: 24px; color: var(--primary); cursor: pointer;" :style="{ opacity: index === settingsForm.faqList.length - 1 ? '0.2' : '1', pointerEvents: index === settingsForm.faqList.length - 1 ? 'none' : 'auto' }" @click="moveFaq(index, 1)"></ion-icon>
                        <div style="width: 1px; height: 16px; background: var(--border-color); margin: 0 2px;"></div>
                        <ion-icon name="close-circle" style="font-size: 24px; color: var(--danger); cursor: pointer;" @click="settingsForm.faqList.splice(index, 1)"></ion-icon>
                    </div>
                </div>
                <div style="width: 100%; border: 1px solid var(--border-color); border-radius: 10px; background: var(--card-bg); overflow: hidden; display: flex; flex-direction: column; box-sizing: border-box;">
                    <input type="text" v-model="item.q" placeholder="问题标题 (Q)" style="height: 44px; border: none; border-bottom: 1px dashed var(--border-color); background: transparent; font-size: 14px; font-weight: bold; padding: 0 12px; outline: none; color: var(--text-main); box-sizing: border-box; width: 100%;">
                    <textarea v-model="item.a" placeholder="详细回答 (A) 支持<br>换行" style="height: 70px; border: none; background: transparent; resize: none; color: var(--text-sub); line-height: 1.4; padding: 10px 12px; font-size: 13px; outline: none; box-sizing: border-box; width: 100%;"></textarea>
                </div>
            </div>
            <div style="display: flex; gap: 10px;">
                <button type="button" class="ios-btn-primary ios-btn-secondary" style="flex: 1; height: 42px;" @click="settingsForm.faqList.push({q: '', a: '', icon: 'help-circle-outline'})">+ 新增</button>
                <button type="button" class="ios-btn-primary" style="flex: 1.5; height: 42px;" @click="saveSettings('update_faq')">保存发布</button>
            </div>
        </CustomModal>

        <CustomModal v-model:show="settingModals.parsers" title="自定义规则" width="500px">
            <div v-for="(tpl, idx) in settingsForm.customParsers" :key="tpl.id" style="background: var(--app-bg); border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; border: none;">
                <div>
                    <div style="font-weight: 600; color: var(--text-main);">{{ tpl.name }}</div>
                    <div style="font-size: 12px; color: var(--text-sub); margin-top: 4px; font-family: monospace;">{{ tpl.mode === 'split' ? '以 "' + tpl.separator + '" 进行可视化分割' : 'Regex 高级正则引擎' }}</div>
                </div>
                <div style="display: flex; gap: 12px;">
                    <ion-icon name="create-outline" style="color: var(--primary); font-size: 20px; padding: 4px; cursor: pointer;" @click="editCustomParser(tpl)"></ion-icon>
                    <ion-icon name="trash-outline" style="color: var(--danger); font-size: 20px; padding: 4px; cursor: pointer;" @click="deleteCustomParser(idx)"></ion-icon>
                </div>
            </div>
            <div v-if="!settingsForm.customParsers || settingsForm.customParsers.length === 0" style="text-align: center; padding: 20px 0; color: var(--text-sub); font-size: 13px;">暂无自定义解析引擎</div>
            <div style="display: flex; gap: 12px; margin-top: 12px;">
                <button type="button" class="ios-btn-primary ios-btn-secondary" style="flex: 1; height: 42px; margin: 0;" @click="openParserModal()">+ 可视化</button>
                <button type="button" class="ios-btn-primary ios-btn-secondary" style="flex: 1; height: 42px; color: var(--ios-orange); border-color: var(--ios-orange); margin: 0;" @click="openRegexModal()">+ 智能正则</button>
            </div>
        </CustomModal>

        <CustomModal v-model:show="settingModals.nodes" title="节点状态">
            <div v-if="!nodeList || nodeList.length === 0" style="text-align: center; padding: 30px 0; color: var(--text-sub);">
                <ion-icon name="server-outline" style="font-size: 32px; opacity: 0.5; margin-bottom: 8px;"></ion-icon>
                <div style="font-size: 13px;">暂无客户端连接</div>
            </div>
            <div v-else style="background: var(--app-bg); border-radius: 12px; overflow: hidden;">
                <div v-for="(node, index) in nodeList" :key="node.device_id" style="padding: 14px 16px; display: flex; justify-content: space-between; align-items: center;" :style="{ borderBottom: index === nodeList.length - 1 ? 'none' : '1px solid var(--border-color)' }">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; margin-bottom: 4px;">
                            <span style="font-weight: 500; font-size: 15px;" :style="{ color: node.is_online ? 'var(--text-main)' : 'var(--text-sub)' }">{{ node.nickname }}</span>
                            <span v-if="!node.is_online" style="font-size: 10px; color: var(--text-sub); background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px; margin-left: 8px;">离线</span>
                        </div>
                        <div style="font-size: 11px; color: var(--text-sub); font-family: monospace;">ID: {{ node.device_id.substring(0, 12) }}...</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div class="status-badge" :class="node.is_online ? 'status-running' : 'status-offline'" style="padding: 0; background: transparent;">
                            <div class="static-dot" style="margin:0; width: 10px; height: 10px;" :style="{ background: node.is_online ? 'var(--success)' : 'var(--text-sub)', boxShadow: node.is_online ? '0 0 8px var(--success)' : 'none' }"></div>
                        </div>
                        <div @click.stop="deleteNode(node)" style="color: var(--danger); display: flex; align-items: center; padding: 4px; cursor: pointer;">
                            <ion-icon name="trash-outline" style="font-size: 18px;"></ion-icon>
                        </div>
                    </div>
                </div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="settingModals.download" title="客户端下载">
            <div v-if="loadingFiles" style="text-align: center; padding: 30px 0; color: var(--text-sub);">
                <ion-icon name="sync" class="spin" style="font-size: 24px; color: var(--primary);"></ion-icon>
                <div style="font-size: 13px; margin-top: 8px;">获取文件中...</div>
            </div>
            <div v-else-if="!clientFiles || clientFiles.length === 0" style="text-align: center; padding: 30px 0; color: var(--text-sub);">
                <ion-icon name="cube-outline" style="font-size: 32px; opacity: 0.5; margin-bottom: 8px;"></ion-icon>
                <div style="font-size: 13px;">/file 文件夹内暂无安装包</div>
            </div>
            <div v-else style="background: var(--app-bg); border-radius: 12px; overflow: hidden;">
                <div v-for="(file, index) in clientFiles" :key="file.name" style="padding: 14px 16px; display: flex; justify-content: space-between; align-items: center;" :style="{ borderBottom: index === clientFiles.length - 1 ? 'none' : '1px solid var(--border-color)' }">
                    <div style="flex: 1; min-width: 0; padding-right: 12px;">
                        <div style="font-size: 15px; font-weight: 500; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ file.name }}</div>
                        <div style="font-size: 11px; color: var(--text-sub); margin-top: 4px; font-family: monospace;">{{ file.size }} • 更新于 {{ file.mtime }}</div>
                    </div>
                    <a :href="'/download/client/' + file.name" class="ios-btn-primary" style="height: 30px; width: auto; padding: 0 16px; font-size: 12px; text-decoration: none; display: flex; align-items: center; margin: 0; border-radius: 15px; box-shadow: none;">下载</a>
                </div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="settingModals.bark" title="Bark 推送" :closeOnMask="true">
            <form @submit.prevent="saveSettings('update_bark')" style="display:flex; flex-direction:column; gap:16px;">
                <!-- 主开关 -->
                <div class="bark-header">
                    <div class="bark-header-text">
                        <span class="bark-header-title">轮次提醒</span>
                        <span class="bark-header-desc">定时推送轮次进度</span>
                    </div>
                    <label class="bark-toggle">
                        <input type="checkbox" v-model="settingsForm.bark_enabled">
                        <span class="bark-toggle-track">
                            <span class="bark-toggle-thumb"></span>
                        </span>
                    </label>
                </div>

                <!-- 配置区域 -->
                <transition name="fade-slide">
                    <div v-if="settingsForm.bark_enabled" class="bark-body">
                        <!-- 服务器配置卡片 -->
                        <div class="bark-card">
                            <div class="bark-card-header">
                                <ion-icon name="server-outline" class="bark-card-icon" style="color: var(--primary);"></ion-icon>
                                <span class="bark-card-title">服务器配置</span>
                            </div>
                            <div class="bark-card-body">
                                <div class="bark-field">
                                    <label>BARK_KEY</label>
                                    <input type="text" v-model="settingsForm.bark_url" placeholder="https://api.day.app/Key 或自定义服务器" class="bark-input-dark">
                                </div>
                                <div class="bark-field">
                                    <label>图标地址</label>
                                    <input type="text" v-model="settingsForm.bark_icon" placeholder="默认使用应用图标" class="bark-input-dark">
                                </div>
                            </div>
                        </div>

                        <!-- 推送内容卡片 -->
                        <div class="bark-card">
                            <div class="bark-card-header">
                                <ion-icon name="chatbubble-outline" class="bark-card-icon" style="color: var(--ios-orange);"></ion-icon>
                                <span class="bark-card-title">推送内容</span>
                            </div>
                            <div class="bark-card-body">
                                <div class="bark-field">
                                    <label>标题 <span class="bark-var">支持 {group} {time}</span></label>
                                    <input type="text" v-model="settingsForm.bark_title" class="bark-input-dark">
                                </div>
                                <div class="bark-field">
                                    <label>内容</label>
                                    <textarea v-model="settingsForm.bark_body" class="bark-textarea-dark" rows="2"></textarea>
                                </div>
                            </div>
                        </div>

                        <!-- 实物掉落推送卡片 -->
                        <div class="bark-card" :class="{ disabled: !settingsForm.bark_enabled }">
                            <div class="bark-card-header">
                                <ion-icon name="gift-outline" class="bark-card-icon" style="color: var(--danger);"></ion-icon>
                                <span class="bark-card-title">实物掉落推送</span>
                                <label class="bark-toggle-mini" style="margin-left: auto;">
                                    <input type="checkbox" v-model="settingsForm.bark_notify_physical" :disabled="!settingsForm.bark_enabled">
                                    <span class="bark-toggle-track-mini">
                                        <span class="bark-toggle-thumb-mini"></span>
                                    </span>
                                </label>
                            </div>
                            <transition name="fade-slide">
                                <div v-if="settingsForm.bark_notify_physical" class="bark-card-body">
                                    <div class="bark-field">
                                        <label>标题 <span class="bark-var">支持 {nickname} {item}</span></label>
                                        <input type="text" v-model="settingsForm.bark_physical_title" class="bark-input-dark">
                                    </div>
                                    <div class="bark-field">
                                        <label>内容</label>
                                        <textarea v-model="settingsForm.bark_physical_body" class="bark-textarea-dark" rows="2"></textarea>
                                    </div>
                                </div>
                            </transition>
                        </div>
                    </div>
                </transition>

                <!-- 按钮 -->
                <div class="bark-footer">
                    <button type="button" class="bark-btn bark-btn-sec" @click="testBark">
                        <ion-icon v-if="testingBark" name="sync" class="spin"></ion-icon>
                        <ion-icon v-else name="paper-plane-outline"></ion-icon>
                        测试
                    </button>
                    <button type="submit" class="bark-btn bark-btn-pri">
                        <ion-icon name="checkmark-outline"></ion-icon>
                        保存
                    </button>
                </div>
            </form>
        </CustomModal>

        <CustomModal v-model:show="pwaModal.show" title="添加到桌面">
            <div style="text-align: center; padding-bottom: 10px;">
                <ion-icon name="share-outline" style="font-size: 48px; color: var(--primary); margin-bottom: 16px;"></ion-icon>
                <p style="color:var(--text-sub); font-size:14px; margin-bottom:24px; line-height:1.6; text-align: left; padding: 0 10px;">
                    1. 点击 Safari 底部 <b>分享</b> 图标<br>
                    2. 下滑选择 <b>“添加到主屏幕”</b><br>
                    3. 享受全屏 0 刷新原生体验！
                </p>
                <button class="ios-btn-primary" @click="pwaModal.show = false" style="background: var(--app-bg); color: var(--primary); height: 48px; border-radius: 12px;">知道了</button>
            </div>
        </CustomModal>

        <CustomModal v-model:show="accountManageModal.show" title="全库账号数据管理" width="500px">
            <div class="ios-search-bar" style="height: 48px; margin-bottom: 16px; background: var(--app-bg); border: none; padding: 0 16px; border-radius: 12px; box-sizing: border-box; flex-shrink: 0;">
                <ion-icon name="search" class="ios-search-icon" style="flex-shrink: 0;"></ion-icon>
                <input type="text" class="ios-search-input" style="flex: 1; min-width: 0; padding: 0; height: 100%; box-sizing: border-box;" placeholder="检索全库需管理的账号..." v-model="accountManageModal.searchText">
                <ion-icon name="close-circle" style="color:var(--text-sub); font-size:18px; opacity:0.6; cursor: pointer; flex-shrink: 0;" v-show="accountManageModal.searchText" @click="accountManageModal.searchText = ''"></ion-icon>
            </div>

            <div v-if="accountManageModal.loading" style="text-align: center; padding: 30px 0; color: var(--text-sub);">读取全库名单中...</div>
            <div v-else-if="!filteredManageUserList || filteredManageUserList.length === 0" style="text-align: center; padding: 30px 0; color: var(--text-sub);">全库无此账号</div>
            <div v-else style="background: var(--app-bg); border-radius: 12px; border: none; overflow: hidden; margin-bottom: 4px;">
                <div v-for="(user, idx) in filteredManageUserList" :key="user" style="display: flex; justify-content: space-between; align-items: center; padding: 14px 16px;" :style="{ borderBottom: idx === filteredManageUserList.length - 1 ? 'none' : '1px solid var(--border-color)' }">
                    <span style="font-weight: 500; font-size: 14px; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-right: 12px;">{{ user }}</span>
                    <div style="display: flex; gap: 16px; align-items: center; flex-shrink: 0;">
                        <ion-icon name="git-merge-outline" style="font-size: 18px; color: var(--primary); cursor: pointer;" @click="prepMerge(user)"></ion-icon>
                        <div style="width: 1px; height: 14px; background: var(--border-color);"></div>
                        <ion-icon name="trash-outline" style="font-size: 18px; color: var(--danger); cursor: pointer;" @click="confirmDelete(user)"></ion-icon>
                    </div>
                </div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="mergeModal.show" title="数据归并">
            <div style="text-align: center;">
                <p style="font-size: 13px; color: var(--text-sub); line-height: 1.6; margin: 0 0 20px 0;">将全库中账号 <b style="color:var(--text-main);">{{ mergeModal.oldName }}</b> 的轨迹<br>全部合并到哪个新昵称？</p>

                <div style="position: relative; margin-bottom: 24px; text-align: left;">
                    <div class="ios-search-bar" style="height: 46px; margin: 0; background: var(--app-bg); border: none; border-radius: 12px; padding: 0 12px; box-sizing: border-box; display: flex; align-items: center;">
                        <ion-icon name="search" class="ios-search-icon" style="flex-shrink: 0; margin-right: 8px;"></ion-icon>
                        <input type="text" class="ios-search-input" v-model="mergeModal.newName" placeholder="输入或点选目标新昵称" style="flex: 1; min-width: 0; padding: 0; height: 100%; box-sizing: border-box; background: transparent; border: none; outline: none; color: var(--text-main); font-size: 14px;">
                        <ion-icon name="close-circle" style="color:var(--text-sub); font-size:18px; opacity:0.6; cursor: pointer; flex-shrink: 0;" v-show="mergeModal.newName" @click="mergeModal.newName = ''"></ion-icon>
                    </div>

                    <div v-if="suggestedMergeUsers && suggestedMergeUsers.length > 0" style="background: var(--app-bg); border: none; border-radius: 12px; max-height: 150px; overflow-y: auto; margin-top: 8px;">
                        <div v-for="(u, idx) in suggestedMergeUsers" :key="u" @click="selectMergeUser(u)" style="padding: 12px 16px; cursor: pointer; display: flex; align-items: center;" :style="{ borderBottom: idx === suggestedMergeUsers.length - 1 ? 'none' : '1px solid var(--border-color)' }">
                            <ion-icon name="person-outline" style="color: var(--text-sub); margin-right: 10px; font-size: 16px; opacity: 0.6;"></ion-icon>
                            <span style="font-size: 14px; color: var(--text-main); font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ u }}</span>
                        </div>
                    </div>
                </div>

                <div style="display: flex; gap: 12px;">
                    <button class="ios-btn-primary ios-btn-secondary" style="flex: 1;" @click="mergeModal.show = false">取消</button>
                    <button class="ios-btn-primary" style="flex: 1;" @click="executeMerge">确认合并</button>
                </div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="mpModal.group.show" title="编辑分组">
            <form @submit.prevent="saveSettings('edit_item')">
                <div style="margin-bottom:24px;">
                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; display: block; margin-bottom: 6px;">分组名称</label>
                    <input type="text" v-model="mpModal.group.name" class="ios-input" style="height: 48px; border: none; background: var(--app-bg);" required>
                </div>
                <div style="display: flex; gap: 12px; margin-bottom: 12px;">
                    <button type="button" class="ios-btn-primary ios-btn-secondary" style="flex: 1;" @click="mpModal.group.show = false">取消</button>
                    <button type="submit" class="ios-btn-primary" style="flex: 1;">保存</button>
                </div>
            </form>
            <button class="ios-btn-primary ios-btn-danger" style="height: 52px;" @click="deleteGroup"><ion-icon name="trash" style="margin-right: 6px; font-size: 18px;"></ion-icon> 删除该分组</button>
        </CustomModal>

        <CustomModal v-model:show="iconPickerModal.show" title="选择 QA 图标" width="340px">
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; padding: 5px;">
                <div v-for="icon in availableIcons" :key="icon" @click="selectIcon(icon)" class="icon-grid-item" :style="{ background: iconPickerModal.currentIcon === icon ? 'var(--primary-shadow)' : 'var(--app-bg)', border: iconPickerModal.currentIcon === icon ? '2px solid var(--primary)' : '1px solid transparent' }">
                    <ion-icon :name="icon" style="font-size: 26px;" :style="{ color: iconPickerModal.currentIcon === icon ? 'var(--primary)' : 'var(--text-main)' }"></ion-icon>
                </div>
            </div>
        </CustomModal>

        <CustomModal v-model:show="parserModal.show" title="创建自定义解析规则" width="500px">
            <label style="font-size:12px; color:var(--text-sub); font-weight: 600; display: block; margin-bottom: 6px;">模板名称</label>
            <input type="text" v-model="parserModal.name" class="ios-input" style="border: none; background: var(--app-bg); margin-bottom: 16px;">

            <label style="font-size:12px; color:var(--primary); font-weight: 600; display: block; margin-bottom: 6px;">第一步：填入一段最新格式的真实日志记录</label>
            <textarea v-model="parserModal.sampleLog" class="ios-input" style="height: 80px; resize: none; padding: 12px; border: none; background: var(--primary-shadow); margin-bottom: 16px; font-size: 13px; line-height: 1.4;" placeholder="直接粘贴单行日志，不要换行..."></textarea>

            <label style="font-size:12px; color:var(--ios-orange); font-weight: 600; display: block; margin-bottom: 6px;">第二步：提取它们之间的分隔符 (如：----)</label>
            <input type="text" v-model="parserModal.separator" class="ios-input" style="border: none; background: var(--app-bg); margin-bottom: 16px;">

            <div v-if="parserModal.sampleLog && parserModal.separator" style="margin-bottom: 20px;">
                <div style="font-size:12px; color:var(--success); font-weight: 600; margin-bottom: 8px;">第三步：系统已切片完毕，请手动映射数据列：</div>
                <div style="background: var(--app-bg); border-radius: 12px; padding: 12px; border: none; max-height: 250px; overflow-y: auto;">
                    <div v-for="(part, idx) in parserPreviewParts" :key="idx" style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px dashed var(--border-color);">
                        <div style="font-size: 13px; color: var(--text-main); font-weight: bold; margin-bottom: 6px; word-break: break-all;">第 {{idx + 1}} 列: <span style="color: var(--primary); font-weight: normal;">{{ part }}</span></div>
                        <select v-model="parserModal.mappings[idx]" class="ios-select" style="height: 36px; font-size: 13px; border: none; background: var(--card-bg);">
                            <option value="ignore">❌ 忽略这列（无用数据）</option>
                            <option value="time">🕒 绑定为：时间</option>
                            <option value="nick">👤 绑定为：昵称</option>
                            <option value="val">💎 绑定为：混合产出 (物品+数量)</option>
                            <option value="item">🎁 绑定为：仅物品名称</option>
                            <option value="qty">🔢 绑定为：仅数量</option>
                        </select>
                    </div>
                </div>
            </div>
            <button class="ios-btn-primary" style="width: 100%; margin-bottom: 10px;" @click="saveCustomParser">一键生成引擎配置</button>
        </CustomModal>

        <CustomModal v-model:show="regexModal.show" title="创建智能解析规则" width="550px">
            <label style="font-size:12px; color:var(--text-sub); font-weight: 600; margin-bottom: 6px; display: block;">模板名称</label>
            <input type="text" v-model="regexModal.name" class="ios-input" style="border: none; background: var(--app-bg); margin-bottom: 16px;" placeholder="例如: 嘉中利抖音格式">

            <div style="display:flex; gap:10px; margin-bottom:15px; background:var(--app-bg); padding:4px; border-radius:12px;">
                <button type="button" :style="{flex:1, height:'34px', borderRadius:'8px', border:'none', background: regexModal.smartMode ? 'var(--primary)' : 'transparent', color: regexModal.smartMode ? '#FFF' : 'var(--text-main)', fontWeight:'bold', fontSize:'13px', cursor: 'pointer'}" @click="regexModal.smartMode = true">🤖 傻瓜生成</button>
                <button type="button" :style="{flex:1, height:'34px', borderRadius:'8px', border:'none', background: !regexModal.smartMode ? 'var(--primary)' : 'transparent', color: !regexModal.smartMode ? '#FFF' : 'var(--text-main)', fontWeight:'bold', fontSize:'13px', cursor: 'pointer'}" @click="regexModal.smartMode = false">💻 专业模式</button>
            </div>

            <div v-if="regexModal.smartMode" style="margin-bottom: 15px;">
                <label style="font-size:12px; color:var(--text-sub); font-weight: 600; margin-bottom: 6px; display: block;">1. 粘贴真实日志并拆解</label>
                <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                    <textarea v-model="regexModal.smartSample" class="ios-input" rows="2" style="font-family: monospace; font-size: 12px; background: var(--app-bg); border: none; flex: 1; resize: none; padding: 10px; border-radius: 8px;" placeholder="在此粘贴日志原文..."></textarea>
                    <button type="button" class="ios-btn-primary" style="width: 60px; font-size: 12px; background: var(--primary); color: #fff; border: none; padding: 0; border-radius: 8px;" @click="doExplode()">拆解</button>
                </div>

                <div v-if="regexModal.explodedTokens && regexModal.explodedTokens.length > 0" style="animation: popIn 0.3s ease-out;">
                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; margin-bottom: 6px; display: block;">2. 选择画笔，点选对应数据</label>
                    <div style="font-size:11px; color:var(--text-sub); margin-bottom: 8px;">未点选文字自动适应，标点符号已默认作为精准锚点边界。</div>

                    <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">
                        <div @click="setBrush('time')" style="padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; transition: 0.2s;" :style="{ background: regexModal.activeBrush === 'time' ? 'rgba(0,122,255,0.15)' : 'transparent', color: 'var(--text-main)', border: regexModal.activeBrush === 'time' ? '1px solid rgba(0,122,255,0.4)' : '1px solid var(--border-color)' }">🕒 时间</div>
                        <div @click="setBrush('nick')" style="padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; transition: 0.2s;" :style="{ background: regexModal.activeBrush === 'nick' ? 'rgba(255,204,0,0.3)' : 'transparent', color: 'var(--text-main)', border: regexModal.activeBrush === 'nick' ? '1px solid rgba(255,204,0,0.5)' : '1px solid var(--border-color)' }">👤 昵称</div>
                        <div @click="setBrush('item')" style="padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; transition: 0.2s;" :style="{ background: regexModal.activeBrush === 'item' ? 'rgba(52,199,89,0.2)' : 'transparent', color: 'var(--text-main)', border: regexModal.activeBrush === 'item' ? '1px solid rgba(52,199,89,0.4)' : '1px solid var(--border-color)' }">🎁 物品</div>
                        <div @click="setBrush('qty')" style="padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; transition: 0.2s;" :style="{ background: regexModal.activeBrush === 'qty' ? 'rgba(90,200,250,0.25)' : 'transparent', color: 'var(--text-main)', border: regexModal.activeBrush === 'qty' ? '1px solid rgba(90,200,250,0.4)' : '1px solid var(--border-color)' }">🔢 数量</div>
                        <div @click="setBrush('ignore')" style="padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; transition: 0.2s;" :style="{ background: regexModal.activeBrush === 'ignore' ? 'var(--app-bg)' : 'transparent', color: 'var(--text-sub)', border: regexModal.activeBrush === 'ignore' ? '1px dashed var(--border-color)' : '1px solid var(--border-color)' }">🗑️ 强制忽略</div>
                        <div @click="setBrush('raw')" style="padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; cursor: pointer; transition: 0.2s; background: transparent; border: 1px solid var(--border-color); color: var(--text-main);">↩️ 撤销</div>
                    </div>

                    <div style="padding:10px; background:var(--app-bg); border-radius:8px; margin-bottom:12px; max-height: 200px; overflow-y: auto;">
                        <span v-for="(t, idx) in regexModal.explodedTokens" :key="idx" @click="paintToken(idx)" :style="getTokenStyle(t)">
                            {{ t.text.trim() === '' ? '␣' : t.text }}
                        </span>
                    </div>

                    <label style="font-size:12px; color:var(--text-sub); font-weight: 600; margin-bottom: 6px; display: block;">3. 实时匹配测试</label>
                    <div style="font-size: 12px; padding: 10px; background: var(--app-bg); border-radius: 8px; white-space: pre-wrap; font-family: monospace; color: var(--text-main);">{{ testRegex() || '等待数据处理...' }}</div>
                </div>
            </div>

            <div v-else style="margin-bottom: 15px;">
                <label style="font-size:12px; color:var(--text-sub); font-weight: 600; margin-bottom: 6px; display: block;">底层正则表达式 (PCRE 引擎)</label>
                <textarea v-model="regexModal.pattern" class="ios-input" rows="4" style="font-family: monospace; font-size: 12px; background: var(--app-bg); border: none;"></textarea>
                <div style="font-size:11px; color:var(--ios-orange); margin-top: 6px;">* 支持 3/4 捕获组。如果您使用傻瓜模式，此代码将自动生成。</div>
            </div>

            <div style="display: flex; gap: 12px; margin-top: auto;">
                <button type="button" class="ios-btn-primary ios-btn-secondary" style="flex: 1;" @click="regexModal.show = false">取消</button>
                <button type="button" class="ios-btn-primary" style="flex: 1;" @click="saveRegexParser">保存规则</button>
            </div>
        </CustomModal>

    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useMainStore } from '../store.js';

import CustomModal from '../components/CustomModal.vue'; // 引入全局弹窗组件

const globalState = useMainStore();
const router = useRouter();

const mpItems = computed(() => globalState.mpItems);
const mpSettings = computed(() => globalState.mpSettings);
const nodeList = computed(() => globalState.nodeList);
const clientFiles = computed(() => globalState.clientFiles);
// 🌟 新增：动态计算真正处于在线状态的节点数量
const onlineNodesCount = computed(() => {
    if (!nodeList.value) return 0;
    return nodeList.value.filter(n => n.is_online).length;
});
const settingsForm = ref({ 
    newItemName: '', interval_hours: 72, 
    bark_enabled: false, bark_url: '', bark_title: '', bark_body: '', bark_icon: '', 
    bark_notify_physical: false, bark_physical_title: '', bark_physical_body: '',
    faqList: [], customParsers: [] 
});

// 同步 Store 状态到本地表单（仅初始化时执行一次）
let isInitialized = false;
watch(() => globalState.mpSettings, (val) => {
    if(val && !isInitialized) {
        isInitialized = true;
        settingsForm.value.interval_hours = val.interval_hours || 72;
        settingsForm.value.bark_enabled = val.bark_enabled || false;
        settingsForm.value.bark_url = val.bark_url || '';
        settingsForm.value.bark_title = val.bark_title || '';
        settingsForm.value.bark_body = val.bark_body || '';
        settingsForm.value.bark_icon = val.bark_icon || '';
        settingsForm.value.bark_notify_physical = val.bark_notify_physical || false;
        settingsForm.value.bark_physical_title = val.bark_physical_title || '';
        settingsForm.value.bark_physical_body = val.bark_physical_body || '';
        settingsForm.value.faqList = JSON.parse(JSON.stringify(val.faqList || []));
        settingsForm.value.customParsers = JSON.parse(JSON.stringify(val.customParsers || []));
    }
}, { immediate: true });

// 监听总开关变化，联动关闭实物推送
watch(() => settingsForm.value.bark_enabled, (newVal, oldVal) => {
    // 当总开关从 true 变为 false 时，自动关闭实物推送
    if (oldVal === true && newVal === false) {
        settingsForm.value.bark_notify_physical = false;
    }
});

// ===================== 新增：抽屉式弹窗状态中心 =====================
const settingModals = ref({
    group: false,
    interval: false,
    faq: false,
    parsers: false,
    nodes: false,
    download: false,
    bark: false
});

// 统一打开配置面板
const openSetting = (key) => {
    if (key === 'download') fetchClientFilesWrapper(); // 点击下载前先获取文件列表
    settingModals.value[key] = true;
};

// ===================== 之前就有的弹窗状态 =====================
const mpModal = ref({ group: { show: false, id: null, name: '' } });
const iconPickerModal = ref({ show: false, targetIndex: -1, currentIcon: '' });
const availableIcons = ['help-circle-outline', 'alert-circle-outline', 'information-circle-outline', 'bulb-outline', 'chatbubble-outline', 'chatbubbles-outline', 'document-text-outline', 'flame-outline', 'flash-outline', 'star-outline', 'heart-outline', 'leaf-outline', 'planet-outline', 'rocket-outline', 'sparkles-outline', 'sunny-outline', 'water-outline', 'gift-outline', 'trophy-outline', 'medal-outline'];
const pwaModal = ref({ show: false });
const accountManageModal = ref({ show: false, loading: false, users: [], searchText: "" });
const mergeModal = ref({ show: false, oldName: "", newName: "" });
const parserModal = ref({ show: false, id: '', name: '', sampleLog: '', separator: '----', mappings: {} });
const regexModal = ref({ show: false, id: '', name: '智能正则解析', pattern: '', item_type: '钻石', smartMode: true, smartSample: '', smartTemplate: '', activeBrush: 'time', explodedTokens: [] });

const testingBark = ref(false);
const loadingFiles = ref(false);

// ===================== 保存与网络请求逻辑 =====================
const saveSettings = async (actionStr) => {
    const payload = { action: actionStr };
    
    if (actionStr === 'add_item') { 
        if(!settingsForm.value.newItemName) return;
        payload.name = settingsForm.value.newItemName; 
        settingsForm.value.newItemName = ''; 
    }
    else if (actionStr === 'update_interval') { payload.interval_hours = settingsForm.value.interval_hours; }
    else if (actionStr === 'update_bark') {
        payload.bark_url = settingsForm.value.bark_url;
        payload.bark_title = settingsForm.value.bark_title;
        payload.bark_body = settingsForm.value.bark_body;
        payload.bark_icon = settingsForm.value.bark_icon;
        payload.bark_notify_physical = settingsForm.value.bark_notify_physical;
        payload.bark_enabled = settingsForm.value.bark_enabled;
        payload.bark_physical_title = settingsForm.value.bark_physical_title;
        payload.bark_physical_body = settingsForm.value.bark_physical_body;
    }
    else if (actionStr === 'edit_item') { 
        payload.id = mpModal.value.group.id; payload.name = mpModal.value.group.name; mpModal.value.group.show = false; 
    }
    else if (actionStr === 'update_faq') { payload.faq_list = settingsForm.value.faqList; }

    try {
        await axios.post('/api/settings', payload);
        await globalState.fetchMpData();

        // 成功保存后，自动关闭对应弹窗让体验更顺滑
        if (actionStr === 'update_interval') settingModals.value.interval = false;
        if (actionStr === 'update_bark') settingModals.value.bark = false;
        if (actionStr === 'update_faq') settingModals.value.faq = false;

    } catch (e) { alert("❌ 保存失败"); }
};

// ==== 维持原有的具体操作函数 ====
const openGroupModal = (item) => { mpModal.value.group = { show: true, id: item.id, name: item.name }; };
const deleteGroup = async () => { if (confirm('⚠️ 彻底删除该分组？不可恢复！')) { await axios.post('/api/settings', { action: 'delete_item', id: mpModal.value.group.id }); mpModal.value.group.show = false; globalState.fetchMpData(); } };
const moveItem = async (index, direction) => {
    const newIndex = index + direction;
    if (newIndex < 0 || newIndex >= mpItems.value.length) return;
    const items = [...mpItems.value];
    const temp = items[index]; items[index] = items[newIndex]; items[newIndex] = temp;
    try { const idList = items.map(item => item.id); await axios.post('/api/settings', { action: 'reorder_items', ids: idList }); globalState.fetchMpData(); } catch (e) {}
};

const testBark = async () => { testingBark.value = true; try { const res = await axios.post('/api/test_bark', settingsForm.value); alert(res.data.msg); } catch (e) { alert("请求失败"); } testingBark.value = false; };

const moveFaq = (index, direction) => {
    const newIndex = index + direction;
    if (newIndex < 0 || newIndex >= settingsForm.value.faqList.length) return;
    const arr = [...settingsForm.value.faqList];
    const temp = arr[index]; arr[index] = arr[newIndex]; arr[newIndex] = temp;
    settingsForm.value.faqList = arr;
};
const openIconPicker = (index) => { iconPickerModal.value.targetIndex = index; iconPickerModal.value.currentIcon = settingsForm.value.faqList[index].icon || 'help-circle-outline'; iconPickerModal.value.show = true; };
const selectIcon = (icon) => { if (iconPickerModal.value.targetIndex !== -1) { settingsForm.value.faqList[iconPickerModal.value.targetIndex].icon = icon; } iconPickerModal.value.show = false; };

const deleteNode = async (node) => { if (!confirm(`确定移除 "${node.nickname}"？`)) return; try { await axios.post('/api/manage_nodes', { action: 'delete', target_id: node.device_id }); await globalState.loadNodes(); globalState.loadLpData(); } catch (e) { alert("移出失败"); } };
const fetchClientFilesWrapper = async () => { loadingFiles.value = true; await globalState.fetchClientFiles(); loadingFiles.value = false; };

const copySearchUrl = () => {
    // 动态获取当前的域名和端口，使用 Vue hash 路由
    const url = window.location.origin + '/#/search';
    
    const doRedirect = () => { 
        alert("✅ 查询页面地址已复制，正在为您跳转..."); 
        router.push('/search'); 
    };
    
    // 现代浏览器剪贴板 API
    if (navigator.clipboard && window.isSecureContext) { 
        navigator.clipboard.writeText(url).then(doRedirect).catch(doRedirect); 
    } else { 
        // 兼容降级方案
        try {
            const textArea = document.createElement("textarea"); 
            textArea.value = url;
            textArea.style.position = "fixed"; 
            textArea.style.top = "0"; 
            textArea.style.left = "0"; 
            textArea.style.opacity = "0";
            document.body.appendChild(textArea); 
            textArea.focus(); 
            textArea.select(); 
            document.execCommand('copy'); 
            document.body.removeChild(textArea);
            doRedirect();
        } catch (err) { 
            router.push('/search'); 
        }
    }
};
const showPwaGuide = () => { pwaModal.value.show = true; };

const openAccountManage = async () => {
    accountManageModal.value.show = true; accountManageModal.value.searchText = "";
    if (accountManageModal.value.users.length === 0) {
        accountManageModal.value.loading = true;
        try { const res = await axios.get(`/api/user_total?global=1`); accountManageModal.value.users = res.data.users || []; } catch (e) { } finally { accountManageModal.value.loading = false; }
    } else { axios.get(`/api/user_total?global=1`).then(res => { if (res.data.users) accountManageModal.value.users = res.data.users; }).catch(() => { }); }
};

const filteredManageUserList = computed(() => { const s = accountManageModal.value.searchText.trim().toLowerCase(); if (!s) return accountManageModal.value.users; return accountManageModal.value.users.filter(u => u.toLowerCase().includes(s)); });

const prepMerge = (name) => { mergeModal.value = { show: true, oldName: name, newName: "" }; };
const executeMerge = async () => {
    if (!mergeModal.value.newName.trim()) return alert("目标新昵称不能为空");
    try { const res = await axios.post('/api/manage_history', { action: 'merge', nickname: mergeModal.value.oldName, new_nickname: mergeModal.value.newName.trim() }); alert(res.data.message); mergeModal.value.show = false; openAccountManage(); globalState.loadLpData(); } catch (e) { alert("合并失败"); }
};

const suggestedMergeUsers = computed(() => {
    const search = mergeModal.value.newName.trim().toLowerCase();
    if (!search) return [];
    return accountManageModal.value.users.filter(u => u.toLowerCase().includes(search) && u !== mergeModal.value.oldName).slice(0, 10);
});

const selectMergeUser = (u) => { mergeModal.value.newName = u; };

const confirmDelete = async (name) => {
    if (confirm(`🚨 将永久删除账号 "${name}"，是否继续？`)) {
        try { const res = await axios.post('/api/manage_history', { action: 'delete', nickname: name }); alert(res.data.message); openAccountManage(); globalState.loadLpData(); } catch (e) { alert("删除失败"); }
    }
};

const parserPreviewParts = computed(() => {
    if (parserModal.value.sampleLog) {
        const parts = parserModal.value.sampleLog.split(parserModal.value.separator);
        parts.forEach((_, idx) => { if (!parserModal.value.mappings[idx]) parserModal.value.mappings[idx] = 'ignore'; });
        return parts;
    } else {
        return ['等待解析'];
    }
});

const openParserModal = () => { parserModal.value = { show: true, id: '', name: '', sampleLog: '', separator: '----', mappings: {} }; };
const openRegexModal = () => { regexModal.value = { show: true, id: '', name: '智能正则解析', pattern: '', item_type: '钻石', smartMode: true, smartSample: '', smartTemplate: '', activeBrush: 'time', explodedTokens: [] }; };

const editCustomParser = (tpl) => {
    if (tpl.mode === 'split') {
        parserModal.value = { show: true, id: tpl.id, name: tpl.name, sampleLog: tpl.sampleLog || '', separator: tpl.separator, mappings: {} };
        if (tpl.time_idx !== -1) parserModal.value.mappings[tpl.time_idx] = 'time';
        if (tpl.nick_idx !== -1) parserModal.value.mappings[tpl.nick_idx] = 'nick';
        if (tpl.val_idx !== -1 && tpl.val_idx !== undefined) parserModal.value.mappings[tpl.val_idx] = 'val';
        if (tpl.item_idx !== -1 && tpl.item_idx !== undefined) parserModal.value.mappings[tpl.item_idx] = 'item';
        if (tpl.qty_idx !== -1 && tpl.qty_idx !== undefined) parserModal.value.mappings[tpl.qty_idx] = 'qty';
    } else {
        regexModal.value = { show: true, id: tpl.id, name: tpl.name, pattern: tpl.pattern, item_type: tpl.item_type || '钻石', smartMode: false, smartSample: '', smartTemplate: '', activeBrush: 'time', explodedTokens: [] };
    }
};

const saveCustomParser = async () => {
    if (!parserModal.value.name.trim()) return alert("请填写模板名称");
    let timeIdx = -1, nickIdx = -1, valIdx = -1, itemIdx = -1, qtyIdx = -1;
    Object.entries(parserModal.value.mappings).forEach(([idx, val]) => {
        if (val === 'time') timeIdx = parseInt(idx);
        if (val === 'nick') nickIdx = parseInt(idx);
        if (val === 'val') valIdx = parseInt(idx);
        if (val === 'item') itemIdx = parseInt(idx);
        if (val === 'qty') qtyIdx = parseInt(idx);
    });

    if (timeIdx === -1 || nickIdx === -1) { return alert("必须指派一列【时间】和一列【昵称】"); }
    if (valIdx === -1 && (itemIdx === -1 || qtyIdx === -1)) { return alert("必须指派混合产出，或分别指派物品和数量！"); }

    let exactLen = 0;
    if (parserModal.value.sampleLog && parserModal.value.separator) { exactLen = parserModal.value.sampleLog.split(parserModal.value.separator).length; } 
    else { exactLen = Math.max(timeIdx, nickIdx, valIdx, itemIdx, qtyIdx) + 1; }

    const newParser = {
        id: parserModal.value.id || 'custom_' + Date.now(), name: parserModal.value.name.trim(), mode: 'split',
        separator: parserModal.value.separator, time_idx: timeIdx, nick_idx: nickIdx, val_idx: valIdx,
        item_idx: itemIdx, qty_idx: qtyIdx, sampleLog: parserModal.value.sampleLog, exact_len: exactLen
    };
    
    let updatedList = [...settingsForm.value.customParsers];
    const existIdx = updatedList.findIndex(p => p.id === newParser.id);
    if (existIdx !== -1) updatedList[existIdx] = newParser; else updatedList.push(newParser);
    
    try { await axios.post('/api/settings', { action: 'save_parsers', parsers_json: updatedList }); settingsForm.value.customParsers = updatedList; parserModal.value.show = false; alert("✅ 模板生成成功！"); globalState.loadLpData(); } catch (e) { alert("保存失败"); }
};

const saveRegexParser = async () => {
    if (!regexModal.value.name.trim() || !regexModal.value.pattern.trim()) return alert("不能为空");
    const newParser = {
        id: regexModal.value.id || 'custom_' + Date.now(), name: regexModal.value.name.trim(), mode: 'regex',
        pattern: regexModal.value.pattern.trim(), item_type: regexModal.value.item_type || '钻石'
    };
    let updatedList = [...settingsForm.value.customParsers];
    const existIdx = updatedList.findIndex(p => p.id === newParser.id);
    if (existIdx !== -1) updatedList[existIdx] = newParser; else updatedList.push(newParser);
    
    try { await axios.post('/api/settings', { action: 'save_parsers', parsers_json: updatedList }); settingsForm.value.customParsers = updatedList; regexModal.value.show = false; alert("✅ 正则模板保存成功！"); globalState.loadLpData(); } catch (e) { alert("保存失败"); }
};

const deleteCustomParser = async (idx) => {
    if (!confirm("🚨 确认删除该解析模板？")) return;
    const updatedList = [...settingsForm.value.customParsers]; updatedList.splice(idx, 1);
    try {
        const res = await axios.post('/api/settings', { action: 'save_parsers', parsers_json: updatedList });
        if (res.data.success) { settingsForm.value.customParsers = updatedList; alert("✅ 删除成功！"); }
    } catch (e) { alert("❌ 删除失败"); }
};

const doExplode = () => {
    if (!regexModal.value.smartSample) return;
    const regex = /([\u4e00-\u9fa5]+|[a-zA-Z0-9]+(?:[\.\-\:\_][a-zA-Z0-9]+)*|[^a-zA-Z0-9\u4e00-\u9fa5\s]+|\s+)/g;
    const matches = regexModal.value.smartSample.match(regex) || [];

    regexModal.value.activeBrush = 'time';
    regexModal.value.explodedTokens = matches.filter(m => m !== '').map((m, i) => {
        const isSym = /^[^a-zA-Z0-9\u4e00-\u9fa5\s]+$/.test(m);
        const isSpace = m.trim() === '';
        return { id: i, text: m, type: 'raw', isSymbol: isSym, isSpace: isSpace };
    });
    generateRegexFromTokens();
};

const setBrush = (brushType) => { regexModal.value.activeBrush = brushType; };

const paintToken = (index) => {
    if (regexModal.value.explodedTokens[index].isSpace) return;
    if (regexModal.value.explodedTokens[index]) {
        regexModal.value.explodedTokens[index].type = regexModal.value.activeBrush;
        generateRegexFromTokens();
    }
};

const generateRegexFromTokens = () => {
    let finalRegex = ""; let currentTag = null; const tokens = regexModal.value.explodedTokens;
    for (let i = 0; i < tokens.length; i++) {
        let t = tokens[i]; let type = t.type;
        if (type === 'raw' && t.isSpace && i > 0 && i < tokens.length - 1) {
            if (tokens[i - 1].type === tokens[i + 1].type && !['raw', 'anchor', 'ignore'].includes(tokens[i - 1].type)) type = tokens[i - 1].type;
        }
        if (type !== currentTag && !['raw', 'anchor', 'ignore', 'space'].includes(type)) {
            if (['time', 'nick', 'item'].includes(type)) finalRegex += "(.*?)";
            else if (type === 'qty') finalRegex += "(\\d+)";
            currentTag = type;
        }
        if (type === 'raw') {
            if (t.isSpace) { finalRegex += "\\s+"; currentTag = 'space'; } 
            else if (t.isSymbol) { finalRegex += t.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); currentTag = 'symbol'; } 
            else { finalRegex += ".*?"; currentTag = 'ignore'; }
        } else if (type === 'anchor') { finalRegex += t.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); currentTag = 'anchor';
        } else if (type === 'ignore') { finalRegex += ".*?"; currentTag = 'ignore'; }
    }
    finalRegex = finalRegex.replace(/(?:\.\*\?)+/g, '.*?').replace(/\.\*\?\\s\+\.\*\?/g, '.*?');
    regexModal.value.pattern = finalRegex;
};

const getTokenStyle = (t) => {
    let bg = 'transparent', color = 'var(--text-main)', border = '1px solid transparent', textDec = 'none', cursor = 'pointer';
    if (t.isSpace) cursor = 'default';
    if (t.type === 'time') { bg = 'rgba(0,122,255,0.15)'; border = '1px solid rgba(0,122,255,0.3)'; }
    else if (t.type === 'nick') { bg = 'rgba(255,204,0,0.3)'; border = '1px solid rgba(255,204,0,0.5)'; }
    else if (t.type === 'item') { bg = 'rgba(52,199,89,0.2)'; border = '1px solid rgba(52,199,89,0.4)'; }
    else if (t.type === 'qty') { bg = 'rgba(90,200,250,0.25)'; border = '1px solid rgba(90,200,250,0.4)'; }
    else if (t.type === 'anchor') { bg = 'rgba(0,0,0,0.05)'; border = '1px solid var(--text-sub)'; }
    else if (t.type === 'ignore') { bg = 'var(--app-bg)'; color = 'var(--text-sub)'; border = '1px dashed var(--border-color)'; textDec = 'line-through'; }
    else if (t.type === 'raw') {
        if (t.isSpace) { bg = 'transparent'; border = 'none'; color = 'transparent'; }
        else if (t.isSymbol) { bg = 'transparent'; border = 'none'; }
        else { bg = 'transparent'; border = '1px dashed var(--border-color)'; color = 'var(--text-sub)'; textDec = 'line-through'; }
    }
    return { background: bg, color: color, border: border, textDecoration: textDec, padding: t.isSymbol ? '4px 2px' : '4px 8px', margin: '3px', borderRadius: '6px', fontSize: '13px', fontWeight: 'bold', cursor: cursor, display: 'inline-block', userSelect: 'none', transition: 'all 0.2s', wordBreak: 'break-all' };
};

const testRegex = () => {
    if (!regexModal.value.pattern || !regexModal.value.smartSample) return null;
    try {
        let re = new RegExp(regexModal.value.pattern);
        let match = regexModal.value.smartSample.match(re);
        if (match && match.length >= 5) return `✅ 完美匹配！\n🕒 时间：${match[1]}\n👤 昵称：${match[2]}\n🎁 物品：${match[3]}\n🔢 数量：${match[4]}`;
        else if (match && match.length === 4) return `✅ 完美匹配 (3字段)！\n🕒 时间：${match[1]}\n👤 昵称：${match[2]}\n💎 产出：${match[3]}`;
        else return `❌ 尚未完整匹配...`;
    } catch (e) { return `❌ 引擎编译中...`; }
};
</script>