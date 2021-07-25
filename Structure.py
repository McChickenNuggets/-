import time

### 获取桃叭项目信息
class Project:
    def __init__(self, title='', star = '', desc='', start_time=0, end_time=0, memo= '',amount=0, volume=0):
        self.star = star
        self.desc = desc
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.memo = memo
        self.amount = amount
        self.volume = volume

    def __str__(self):
        profiles = '偶像名称:' + str(self.star) + '\n'
        profiles += '项目名称:' + str(self.title) + '\n'
        profiles += '项目总金额:' + str(self.amount) + '\t'+'\t'
        profiles += '总件数:' + str(self.volume) + '\n'
        profiles += '项目描述' + str(self.desc) + '\n'
        profiles += '开始时间:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time)) + '\n'
        profiles += '结束时间:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.end_time)) + '\n'
        profiles += '项目备注:' + str(self.memo) + '\n'
        return profiles
