# -*- coding:utf-8 -*-
__author__ = 'TengYu'

import requests
import xlwt
from Tool import Tool
import json
import time
import re
from Tool import deleteAite
from Tool import get_emoj
import sys
reload(sys)
sys.setdefaultencoding('utf8')


headers = {'User-agent' : '',
           'Cookie':'',
        }

class zhuanfa(object):
    def get_zhuanfa(self):
        excel = xlwt.Workbook(encoding='utf-8')
        sheet = excel.add_sheet('sheet1')
        sheet.write(0, 0, 'id')
        sheet.write(0, 1, 'name')
        sheet.write(0, 2, 'time')
        sheet.write(0, 3, 'text')
        sheet.write(0, 4, 'likes')
        sheet.write(0, 5, 'loc')
        sheet.write(0, 6, 'sex')
        for m in range(7, 12):
            sheet.write(0, m, '表情' + str(m-6))
        count = 0
        i = 0
        while i <= 101 and count < 5000:  #这个地方改数据条数
            url = 'https://m.weibo.cn/api/comments/show?id=4336744058977011&page=' #这个地方改数字比如4308796748087542
            i = i + 1
            url = url + str(i)
            print(url)
            try:
                response = requests.get(url, headers=headers)
                time.sleep(1)
                resjson = json.loads(response.text)
                time.sleep(1) 
                dataset = resjson.get('data')
                data = dataset.get('data')
                for j in range(0, len(data)):
                    try:
                        temp = data[j]
                        # if temp.get('reply_id') is not None:
                        #     continue
                        user = temp.get('user')
                        text = temp.get('text')
                        created_at = temp.get('created_at')
                        attitudes_count = temp.get('attitudes_count')
                        userid = user.get('id')
                        info_url = "https://m.weibo.cn/api/container/getIndex?containerid=230283" + str(
                            userid) + "_-_INFO"  # 转发人信息的url
                        r = requests.get(info_url)
                        infojson = json.loads(r.text)
                        infodata = infojson.get('data')
                        cards = infodata.get('cards')
                        sex = ''
                        loc = ''
                        for l in range(0, len(cards)):
                            temp = cards[l]
                            card_group = temp.get('card_group')
                            for m in range(0, len(card_group)):
                                s = card_group[m]
                                if s.get('item_name') == '性别':
                                    sex = s.get('item_content')
                                if s.get('item_name') == '所在地':
                                    loc = s.get('item_content')
                                    loc = re.split(r' ', loc)[0]
                        if sex is None:
                            sex = '未知'
                        if loc is None:
                            loc = '未知'
                        screen_name = user.get('screen_name')
                        count += 1
                        if get_emoj(text) is not None:
                            emoji = get_emoj(text)
                            l = 7
                            while emoji:
                                sheet.write(count, l, str(emoji.pop()))
                                l += 1
                        #File.write(text.encode('utf-8') + '\n')
                        sheet.write(count, 0, userid)
                        sheet.write(count, 1, str(screen_name))
                        sheet.write(count, 2, created_at)
                        text = deleteAite(text)
                        text = Tool.replace(text)
                        if text is not None:
                            sheet.write(count, 3, text.encode('utf-8'))
                        sheet.write(count, 4, attitudes_count)
                        sheet.write(count, 5, str(loc))
                        sheet.write(count, 6, str(sex))
                    except Exception as e:
                        print (e)
                    time.sleep(3)
                print ("已经获取" + str(count) + "条数据")
                time.sleep(8)
            except Exception as e:
                print (e)
        # File.close()
        excel.save('单身人群超过2000.xls') #这个地方改文件名称


if __name__ == '__main__':
    Zhuanfa = zhuanfa() 
    Zhuanfa.get_zhuanfa()