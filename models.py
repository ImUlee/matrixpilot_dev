from extensions import db

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))      
    next_time = db.Column(db.String(50)) 
    data = db.Column(db.JSON) 
    notified = db.Column(db.Boolean, default=False)          

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    sort_order = db.Column(db.Integer, default=0)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interval_hours = db.Column(db.Integer, default=72)
    
    # Bark 通知配置
    bark_enabled = db.Column(db.Boolean, default=False)  # 是否启用Bark通知
    bark_url = db.Column(db.String(255))
    bark_title = db.Column(db.String(100), default="MatrixPilot 提醒")
    bark_body = db.Column(db.String(255), default="分组【{group}】预计下轮时间已到！")
    bark_icon = db.Column(db.String(255), default="") 
    
    # 实物推送配置
    bark_notify_physical = db.Column(db.Boolean, default=False)  # 是否启用实物推送
    bark_physical_title = db.Column(db.String(100), default="🎁 实物掉落提醒")
    bark_physical_body = db.Column(db.String(255), default="【{nickname}】抽中 {item} x{quantity}")
    
    faq_json = db.Column(db.Text)
    parsers_json = db.Column(db.Text, default="[]")