# -*- coding:utf-8 -*-
__author__ = 'TengYu'
import requests
import re
from lxml import etree
import json
import time
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Cookie':'Ecp_ClientId=4190131151000750743; __utmz=25615083.1548918649.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); RsPerPage=20; Ecp_IpLoginFail=190213171.115.109.68; ASP.NET_SessionId=ytcbtb45uy0xz22yz1j1wa55; SID=120143; KNS_DisplayModel=; firstEnterUrlInSession=http%3A//gb.oversea.cnki.net/kns55/brief/result.aspx%3FdbPrefix%3DCMFD; __utma=25615083.731457225.1548918649.1550152889.1550200837.9; __utmc=25615083; VisitorCapacity=1; LID=WEEvREcwSlJHSldTTEYzU3EydDRPZTZYK0hpYU5ZNWp0Rkd2WWQyV0xSTT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"17371253372","ShowName":"1608375901%40qq.com","UserType":"jf","r":"pmc3xX"}; IsLogin=17371253372; pageReferrInSession=http%3A//gb.oversea.cnki.net/Kns55/logindigital.aspx; FileNameS=cnki%3A; CurTop10KeyWord=%2c%u65b0%u95fb%u5b66%2c%u533b%u7597%u4fdd%u9669; c_m_LinID=LinID=WEEvREcwSlJHSldTTEYzU3EydDRPZTZYK0hpYU5ZNWp0Rkd2WWQyV0xSTT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=02/15/2019 12:08:28; c_m_expire=2019-02-15 12:08:28'
}
class PageList(object):
    def __init__(self,maxpage):
        self.maxpage = maxpage

    def getUrl(self):
        f1 = open("title_4_4.txt",'w')
        f2 = open("subtitle.txt",'w')
        f3 = open("keywords_4_4.txt",'w')
        excel = xlwt.Workbook(encoding='utf-8')
        sheet = excel.add_sheet('sheet1')
        sheet.write(0, 0, '论文中文题目')
        sheet.write(0, 1, '论文作者')
        sheet.write(0, 2, '作者学校')
        sheet.write(0, 3, '学位授予年度')
        sheet.write(0, 4, '下载频次')
        sheet.write(0, 5, '引用频次')
        begin = 6
        while begin < 18:
            sheet.write(0, begin, '关键词'+str(begin - 6))
            begin += 1
        while begin < 25:
            sheet.write(0, begin, '副标题'+ str(begin - 18))
            begin += 1
        firstPage = 150
        try:
            tempurl = " "
            num = 0
            while firstPage < self.maxpage:
                tempurl = "http://gb.oversea.cnki.net/kns55/brief/brief.aspx?curpage="+\
                          str(firstPage)+"&RecordsPerPage=20&QueryID=13&ID=&turnpage=1&tpagemode=L&dbPrefix=CMFD&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&sKuaKuID=13"
                response = requests.get(tempurl, headers=headers).content
                selector = etree.HTML(response)
                trs = selector.xpath("//tr")
                firstTds = 11
                # print(len(trs))
                print("已经抓取"+str(num)+"条数据")
                while firstTds < 51:
                    num = num + 1
                    tr = trs[firstTds]
                    td = tr.xpath(".//td")
                    titletd = td[2]
                    titlehref = titletd.xpath(".//a/@href")
                    # print(titlehref)
                    # print(titletd.xpath("string(.)"))
                    href = str(titlehref[0])
                    # print(href)  #获取论文详细内容链接
                    detailurl = "http://gb.oversea.cnki.net" + href
                    print(detailurl)
                    authortd = td[3]  # 获取作者信息
                    schooltd = td[4]  # 获取学校信息
                    yeartd = td[5]  # 获取年份信息
                    yinyongtd = td[6]  # 获取引用次数信息
                    xiazaitd = td[7]  # 获取下载次数信息
                    author = str(authortd.xpath("string(.)").encode('utf-8'))
                    school = str(schooltd.xpath("string(.)").encode('utf-8'))
                    year = str(yeartd.xpath("string(.)").encode('utf-8'))
                    yinyong = "0"
                    xiazai = "0"
                    yinyongs = str(yinyongtd.xpath("string(.)").encode('utf-8'))
                    xiazais = str(xiazaitd.xpath("string(.)").encode('utf-8'))
                    if yinyongs.isspace():
                        yinyong = "0"
                    else:
                        yinyong = yinyongs.replace(' ', '')
                    if xiazais.isspace():
                        xiazai = "0"
                    else:
                        xiazai = xiazais.replace(' ', '')

                    firstTds += 2
                    # 获取具体数据信息，访问构造的detailurl
                    detail = requests.get(detailurl, headers=headers).content
                    sel = etree.HTML(detail)
                    divs = sel.xpath("//div[@id='main']")
                    title = divs[0].xpath("//div[@id='title']")[0]
                    span = title.xpath("//h1//span")[0]
                    st = str(span.xpath("string(.)").encode('utf-8'))
                    print(st)  # 论文题目
                    divs = sel.xpath(".//div[@class='summary pad10']")[0]
                    detailinfo = str(divs.xpath("string(.)").encode('utf-8'))
                    ps = divs.xpath(".//p")
                    f1.write(st+"\n")
                    sheet.write(num, 0, st)
                    sheet.write(num, 1, author)
                    sheet.write(num, 2, school)
                    sheet.write(num, 3, year)
                    sheet.write(num, 4, xiazai)
                    sheet.write(num, 5, yinyong)
                    try:
                        keywordsdiv = sel.xpath(".//div[@class='keywords']")[0]
                        span = keywordsdiv.xpath(".//span[@id='ChDivKeyWord']")[0]
                        hrefs = span.xpath(".//a")
                        i = 0
                        first = 6
                        while i < len(hrefs):
                            words = str(hrefs[i].xpath("string(.)").encode('utf-8'))
                            print(words)
                            f3.write(words+"\n")
                            sheet.write(num, first, words)
                            first += 1
                            i += 1
                    except  Exception as es:
                        print(es)
                    try:
                        if u'副题名' in detailinfo:
                            index = detailinfo.find('【副题名】')
                            loc = index + 15
                            then = 18
                            while detailinfo[loc] != '【':
                                subtitile = ""
                                while detailinfo[loc] != ' ' and detailinfo[loc] != ',':
                                    subtitile += detailinfo[loc]
                                    loc += 1
                                sheet.write(num, then, subtitile)
                                f2.write(subtitile + "\n")
                                then += 1
                    except Exception as es:
                        print(es)
                    time.sleep(1)
                firstPage += 1
                time.sleep(5)
        except Exception as es:
            print (es)
        excel.save("ylbx_4.xls")
        pass

pagelist = PageList(200)
pagelist.getUrl()