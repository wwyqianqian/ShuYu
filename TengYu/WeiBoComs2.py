# -*- coding:utf-8 -*-
__author__ = 'TengYu'
import requests
import xlwt
import json
import time
import re
from datetime import timedelta
from datetime import datetime
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')


headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Cookie': '_T_WM=bd8c955b7c4aa61d7eb9c289820cfcc2; _WEIBO_UID=6859542316; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhZHJqGrTV4w9_Zac4umjWe5JpX5K-hUgL.Fo-feoe4Sh20SoB2dJLoI0YLxKBLBonL1h5LxKqLBKzLBKqLxKBLBonL1h.LxK-LBKBLBK.LxK-LBKBLBo2LxKBLBonL1h.LxK-LBo.LBoBt; SCF=AmbYRKrcsHBa6xB4EHNdXpdiTqL3vBjUUGc3KKeh0yL9Zy3qoxNEpXGQtG0SPspwf_mJg4btLrIXs6HvLSJxozM.; _T_WL=1; SUB=_2A25xF88-DeRhGeBG7lsU9CzPyjqIHXVS-9F2rDV6PUJbkdAKLW_3kW1NRhmid0xMHGrr6trnRy70mYNGFfQTBxel; SUHB=0N21TOT8l1YOVH; SSOLoginState=1544798062'
    }
headers1 = {
    'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Cookie':'SINAGLOBAL=930931665359.751.1541833145678; UOR=,,login.sina.com.cn; SCF=AmbYRKrcsHBa6xB4EHNdXpdiTqL3vBjUUGc3KKeh0yL9waoSgyallHPMYB_OKcgIm3KESV2Z5UKeJkOETQjP6sA.; SUHB=0V5lIb22-VjzD5; ALF=1548397627; SUB=_2A25xJ29rDeRhGeBG7lsU9CzPyjqIHXVS6HEjrDV8PUJbkNAKLWn-kW1NRhmidwZ1pLQEAwnUu4mbXTPY-jBcRrl9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWM6IxVnr7Nm_qQQDJO0c0_5JpX5oz75NHD95Qc1h-4SKBEe02cWs4Dqcj9i--RiKnRiK.Xi--NiKyFiK.NdJvzdNH09Btt; wb_view_log_6859542316=1536*8641.25; YF-Page-G0=b9385a03a044baf8db46b84f3ff125a0; _s_tentry=-; Apache=6629158109517.954.1546398096951; ULV=1546398097080:36:3:3:6629158109517.954.1546398096951:1546359683710'
}



#工具类，用来去除爬取的正文中一些不需要的链接、标签等
class Tool:
    deleteImg = re.compile('<img.*?>')
    newLine =re.compile('<tr>|<div>|</tr>|</div>')
    deleteAite = re.compile('//.*?')
    deleteAddr = re.compile('<a.*?>.*?</a>|<a href='+'\'https:')
    deleteTag = re.compile('<.*?>')
    deleteWord = re.compile('回复@|回覆@|回覆|回复|:')

    @classmethod
    def replace(cls,x):
        x = re.sub(cls.deleteWord,'',x)
        x = re.sub(cls.deleteImg,'',x)
        x = re.sub(cls.deleteAite,'',x)
        x = re.sub(cls.deleteAddr, '', x)
        x = re.sub(cls.newLine,'',x)
        x = re.sub(cls.deleteTag,'',x)
        return x.strip()


def deleteAite(text):
    if re.search('//@',text,flags=0):
        loc = re.search('//@',text,flags=0).span()
        if loc[0] == 0:
            return ' '
        else:
            return text[:loc[0]]
    return text


def get_emoj(text):
    emoj = set()
    r = re.findall(r'[[](.*?)[]]',text)
    for i in range(len(r)):
        if r[i] not in emoj:
            emoj.add(r[i])
    return emoj


class LxmCOM(object):

    def __init__(self,weiboid,uid,maxpage):
        self.weiboid = weiboid
        self.uid = uid
        self.maxpage = maxpage


    def get_url(self):
        excel = xlwt.Workbook(encoding='utf-8')
        sheet = excel.add_sheet('sheet1')
        sheet.write(0, 0, '评论ID')
        sheet.write(0, 1, '评论内容')
        sheet.write(0, 2, '评论者地域')
        sheet.write(0, 3, '评论者性别')
        sheet.write(0, 4, '评论时间')
        #sheet.write(0, 5, '评论者年龄')
        """sheet.write(0, 4, 'loc')
        sheet.write(0, 5, 'text')
        sheet.write(0, 6, 'like')"""
        for m in range(4, 8):
            sheet.write(0, m+1, '评论表情符号'+str(m-3))
        count = 0
        i = 1
        try:
            while i < self.maxpage and count < 2000:
                url = 'https://weibo.cn/comment/'+self.weiboid+'??&uid='+self.uid+'&&page={}'.format(i)
                print (url)
                i += 1
                response = requests.get(url, 'html.parser', headers=headers).content
                selector = etree.HTML(response)
                divs = selector.xpath("//div[@class='c']")
                j = 1
                while j < len(divs):
                    try:
                        div = divs[j]
                        j += 1
                        a = div.xpath(".//a")
                        t = div.xpath(".//span[@class='ctt']")[0]
                        ctt = str(t.xpath("string(.)").encode('utf-8'))
                        if "回复" in ctt:
                            LOC = ctt.find(':')
                            ctt = ctt[LOC + 1:]
                        ctt = Tool.replace(ctt)
                        if "@" in ctt:
                            if ctt.find("@") == 1:
                                if " " in ctt:
                                    loc = ctt.find(':')
                                    loc1 = ctt.find(" ")
                                    ctt = ctt[loc1 + 1:]
                                else:
                                    ctt = ""
                            else:
                                ctt = ctt[:ctt.find("@")]
                        if "图片评论" in ctt:
                            if "http" in ctt:
                                ctt = ""
                        if ctt == "" or ctt == " ":
                            continue
                        if ctt is None:
                            continue
                        print(ctt)
                        count += 1
                        cc = div.xpath(".//span[@class='cc']")
                        ct = cc[0]
                        created_at = str(ct.xpath(".//a/text()")[0].encode('utf-8'))
                        index1 = created_at.index("[")
                        index2 = created_at.index("]")
                        Time = str(div.xpath(".//span[@class='ct']/text()")[0].encode('utf-8'))
                        if '刚刚' in Time:
                            Time = datetime.now().strftime(
                            '%Y-%m-%d %H:%M')
                        elif '分钟' in Time:
                            loc = Time.find('分钟')
                            num = Time[:loc-1]
                            num = timedelta(minutes=int(num))
                            Time =  (datetime.now() - num).strftime(
                            "%Y-%m-%d %H:%M")
                        elif '今天' in Time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            t = Time[3:9]
                            Time = today+' '+t
                        elif '月' in Time:
                            year = datetime.now().strftime("%Y")
                            loc1 = Time.index('月')
                            loc2 = Time.index('日')
                            loc3 = Time.index(' ')
                            month = Time[0:loc1]
                            day = Time[loc1+3:loc2]
                            #t = Time[loc3+1:loc3+6]
                            Time = (
                                    year + "-" + month + "-" + day + " ")
                        else:
                            Time = Time[:15]

                        like_counts = created_at[index1+1:index2]
                        userid = a[0].xpath("./@href")
                        if '/u/' in str(userid):
                            user = str(userid)[5:-2]
                        else:
                            user = str(userid)[3:-2]
                        new_url = 'https://weibo.cn/' + str(user)
                        res = requests.get(new_url, 'html.parser', headers=headers).content
                        time.sleep(1)
                        se = etree.HTML(res)
                        tds = se.xpath("//div[@class='u']//td[@valign='top']")
                        td = tds[0]
                        ID = td.xpath('.//a/@href')
                        user = str(ID)[3:-14]
                        info_url = "https://m.weibo.cn/api/container/getIndex?containerid=230283" + str(
                            user) + "_-_INFO"  # 转发人信息的url
                        r = requests.get(info_url)
                        time.sleep(1)
                        infojson = json.loads(r.text)
                        infodata = infojson.get('data')
                        cards = infodata.get('cards')
                        sex = ''
                        loc = ''
                        name = ''
                        #old = ''
                        for l in range(0, len(cards)):
                            temp = cards[l]
                            card_group = temp.get('card_group')
                            for m in range(0, len(card_group)):
                                s = card_group[m]
                                if s.get('item_name') == '昵称':
                                    name = s.get('item_content')

                                if s.get('item_name') == '性别':
                                    sex = s.get('item_content')

                                if s.get('item_name') == '所在地':
                                    loc = s.get('item_content')
                                    loc = re.split(r' ', loc)[0]

                                """if s.get('item_name') == '生日':
                                    if '年' in str(s.get('item_content')):
                                        index = str(s.get('item_content')).find('年')
                                        old = str(s.get('item_content'))[:index-1]
                                    else:
                                        old = str(s.get('item_content'))"""
                        if sex == '':
                            sex = '未知'
                        if loc == '':
                            loc = '未知'
                        if name == '':
                            name = '未知'
                        sheet.write(count, 0, user)

                        #sheet.write(count, 2, str(name))
                        #sheet.write(count, 3, str(Time))
                        sheet.write(count, 1, str(ctt))
                        sheet.write(count, 2, str(loc))
                        sheet.write(count, 3, str(sex))
                        sheet.write(count, 4, str(Time))
                        #sheet.write(count, 4, str(old))
                        #sheet.write(count, 6, str(like_counts))
                        if get_emoj(ctt) is not None:
                            emoji = get_emoj(ctt)
                            l = 5
                            while emoji:
                                sheet.write(count, l, str(emoji.pop()))
                                l += 1
                    except Exception as e:
                        print (e)
                print("已经抓取"+str(count)+"条数据")
                time.sleep(5)
        except Exception as e:
            print (e)
        excel.save('gg_1.xls')
        pass


if __name__ == "__main__":
    weiboid = "H7ofk6jZu"
    uid = "2803301701"
    maxpage = 20
    COM = LxmCOM(weiboid,uid,maxpage)
    COM.get_url()
    url='https://weibo.cn/comment/HfpSBBFkv??&uid=2028810631'