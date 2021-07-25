import requests
import zlib
import json
import base64
import time
from Structure import Project


def AddSalt(ori: bytearray):
    # 从网页JS当中提取到的混淆盐值，每隔一位做一次异或运算
    Salt = '%#54$^%&SDF^A*52#@7'
    i = 0
    for ch in ori:
        if i % 2 == 0:
            ch = ch ^ ord(Salt[(i // 2) % len(Salt)])
        ori[i] = ch
        i += 1
    return ori


def EncodeData(ori: str):
    # 开头的数字是原始报文长度
    Length = len(ori)
    Message = str.encode(ori)
    # 首先用zlib进行压缩
    Compressed = bytearray(zlib.compress(Message))
    # 然后加盐混淆
    Salted = AddSalt(Compressed)
    # 最后将结果转化为base64编码
    Result = base64.b64encode(Salted).decode('utf-8')
    # 将长度头和base64编码的报文组合起来
    return str(Length) + '$' + Result


def DecodeData(ori: str):
    # 分离报文长度头
    # TODO: 增加报文头长度的验证
    Source = ori.split('$')[1]
    # base64解码
    B64back = bytearray(base64.b64decode(Source))
    # 重新进行加盐计算，恢复原始结果
    Decompressed = AddSalt(B64back)
    # zlib解压
    Result = zlib.decompress(Decompressed).decode('utf-8')
    # 提取json
    return json.loads(Result)


def SendRequest(url: str, data: str):
    Headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://www.tao-ba.club',
        'Cookie': 'l10n=zh-cn',
        'Accept-Language': 'zh-cn',
        'Host': 'www.tao-ba.club',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
        'Referer': 'https://www.tao-ba.club/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    Data = EncodeData(data)
    Res = requests.post(url=url, data=Data, headers=Headers)
    ResText = Res.text
    return DecodeData(ResText)

def process_amount(goods):
    goods_df = goods
    total_amount = 0
    for i in goods_df:
        total_amount += i['price']*i['sells']
    return total_amount

def process_volume(goods):
    goods_df = goods
    total_volume = 0
    for i in goods_df:
        total_volume += i['sells']
    return total_volume

def GetDetail(pro_id: int):
    # 获得项目基本信息
    Data = '{{"id":"{0}","requestTime":{1},"pf":"h5"}}'.format(pro_id, int(time.time() * 1000))
    Response = SendRequest('https://www.tao-ba.club/idols/detail', Data)
    title = Response['datas']['title']
    star = Response['datas']['star']
    desc = Response['datas']['desc'].replace("<br />"," ")
    start_time = int(Response['datas']['start'])
    end_time = int(Response['datas']['expire'])
    memo =  Response['datas']['memo']
    goods = Response['datas']['goods']
    amount = process_amount(goods)
    volume = process_volume(goods)

    return Project(title,star,desc,start_time,end_time,memo,amount,volume)

if __name__ == '__main__':
    hxh=GetDetail(20210)
    print(hxh)