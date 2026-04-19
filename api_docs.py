"""API文档配置

使用Flask-RESTX生成Swagger文档
"""
from flask_restx import Api

# 创建API实例
api = Api(
    version='1.0',
    title='MatrixPilot API',
    description='MatrixPilot 智能中控管理平台 API文档',
    doc='/api/docs',
    prefix='/api'
)

# 定义命名空间
ns_auth = api.namespace('auth', description='认证相关接口')
ns_stats = api.namespace('stats', description='统计数据接口')
ns_nodes = api.namespace('nodes', description='节点管理接口')
ns_search = api.namespace('search', description='搜索查询接口')
ns_settings = api.namespace('settings', description='系统设置接口')
ns_records = api.namespace('records', description='记录管理接口')

# 定义通用模型
from flask_restx import fields

# 认证模型
login_model = api.model('Login', {
    'pin': fields.String(required=True, description='访问密码', example='******')
})

login_response = api.model('LoginResponse', {
    'success': fields.Boolean(description='是否成功'),
    'message': fields.String(description='响应消息')
})

auth_status = api.model('AuthStatus', {
    'logged_in': fields.Boolean(description='登录状态')
})

# 统计模型
stats_model = api.model('Stats', {
    'total_users': fields.Integer(description='总用户数'),
    'total_wins': fields.Integer(description='总中奖数'),
    'total_physical_wins': fields.Integer(description='实物中奖数'),
    'rank_list': fields.List(fields.Raw, description='排行榜'),
    'details': fields.List(fields.Raw, description='详细数据')
})

# 节点模型
node_model = api.model('Node', {
    'device_id': fields.String(description='设备ID'),
    'nickname': fields.String(description='节点昵称'),
    'log_count': fields.Integer(description='日志数量'),
    'last_log_time': fields.String(description='最后日志时间'),
    'is_active': fields.Boolean(description='是否活跃')
})

nodes_response = api.model('NodesResponse', {
    'status': fields.String(description='状态'),
    'nodes': fields.List(fields.Nested(node_model), description='节点列表')
})

# 搜索模型
search_result = api.model('SearchResult', {
    'found': fields.Boolean(description='是否找到'),
    'has_suggestion': fields.Boolean(description='是否有建议'),
    'display_nickname': fields.String(description='显示昵称'),
    'total_sum': fields.Integer(description='累计产出'),
    'physical_count': fields.Integer(description='实物中奖'),
    'logs': fields.List(fields.Raw, description='日志列表')
})

# FAQ模型
faq_item = api.model('FAQItem', {
    'q': fields.String(description='问题'),
    'a': fields.String(description='答案'),
    'icon': fields.String(description='图标')
})

faq_response = api.model('FAQResponse', {
    'faq': fields.List(fields.Nested(faq_item), description='FAQ列表')
})

# 错误模型
error_model = api.model('Error', {
    'success': fields.Boolean(description='是否成功', default=False),
    'error': fields.String(description='错误信息')
})
