import requests
import json
import re
import os
import time

count = 1

def getObj(num, url):	
    headers = {
        'authority': 'www.zhihu.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9,zh-HK;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5',
        'cookie': '',
    }
    params = (
        ('include', 'data[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,is_parent_author,is_author'),
        ('limit', '10'), 
        ('offset', str(num)), 
        ('order', 'normal'),
        ('status', 'open'),
    )

    # response = requests.get('https://www.zhihu.com/api/v4/answers/527558575/root_comments?include=data%5B%2A%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&limit=10&offset=0&order=normal&status=open', headers=headers)
    response = requests.get(str(url), headers=headers, params=params)
    response.encoding = 'utf-8' 
    res_data = json.loads(response.text)
    # load JSON to object 

    print("当前链接 params 的 offset 值为" + params[2][1] + ", 文件中正在写入抓取到的评论:")
    print("-------------------------------------------------------------------")
    return res_data
    

def printComs(num, url):
    global count
    dataObj = getObj(num, url)
    # print(dataObj)   
    for i in range(len(dataObj["data"])):
        contents = dataObj["data"][i]["content"]
        if contents[0] == "<" :
            res = r'<p>(.*?)</p>'
            m = re.findall(res, contents, re.S|re.M)
            for value in m:
                with open('/Users/qianqian/Desktop/comm.txt', 'a', encoding='utf-8') as f:
                    print(str(count) + ". " + str(value), file=f)
                count = count + 1
        else:
            with open('/Users/qianqian/Desktop/comm.txt', 'a', encoding='utf-8') as f:
                print(str(count) + ". " + str(contents), file=f)
            count = count + 1


def setURL():
    url = "https://www.zhihu.com/api/v4/answers/527558575/root_comments"
    for num in range(0, 280, 10):      
        printComs(num, url)
        
        
def main():
    setURL()
    print("运行结束，总共爬取 " + str(count) + " 条数据")


main()