#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Copyright © 2019 - wwyqianqian <i@wwyqq.me>
# Source code: https://github.com/wwyqianqian/ShuYu/blob/master/ZhiHuCom2File.py


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
        'cookie':'',
    }
    params = {
        'include': 'data[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,is_parent_author,is_author',
        'limit': '10', 
        'offset': str(num), 
        'order': 'normal',
        'status': 'open',
    }

    # response = requests.get('https://www.zhihu.com/api/v4/answers/527558575/root_comments?include=data%5B%2A%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&limit=10&offset=0&order=normal&status=open', headers=headers)
    response = requests.get(str(url), headers=headers, params=params)
    response.encoding = 'utf-8' 
    # load JSON to object
    res_data = json.loads(response.text)

    print("当前链接 params 的 offset 值为" + str(num) + ", 文件中正在写入抓取到的评论:")
    print("-------------------------------------------------------------------")
    return res_data
    

def printComs(num, url):
    global count
    dataObj = getObj(num, url)

    with open('/Users/qianqian/Desktop/comm.txt', 'a', encoding='utf-8') as f:  
        for i in range(len(dataObj["data"])):
            contents = dataObj["data"][i]["content"]
            if contents[0] == "<" :
                res = r'<p>(.*?)</p>'
                m = re.findall(res, contents, re.S|re.M)
                for value in m:               
                    f.write(f'{str(count)}. {str(value)}\n')
                    count = count + 1
            else:
                f.write(f'{str(count)}. {str(contents)}\n')
                count = count + 1

def setURL():
    url = "https://www.zhihu.com/api/v4/answers/527558575/root_comments"
    for num in range(0, 280, 10):      
        printComs(num, url)
        time.sleep(3)      
        
def main():
    setURL()
    print("运行结束，总共爬取 " + str(count-1) + " 条数据")


main()


# -------------------------------------------------------------------------------
# OUTPUT: /Users/qianqian/Desktop/comm.txt
# 1. 咱先不说难吃不难吃的事情，咱中国人出门左转菜市场，现杀的鲫鱼、鲢鱼、鲈鱼、鲤鱼、草鱼哪个买不到？买冷冻的美国鲤鱼怕不是石乐志
# 2. 而且卖价还比国内活鱼高好几倍。能卖的出去才见了鬼了。
# 3. 那万一有人觉得美国进口的东西就是好呢
# 4. 是这样的，我们当时也考虑用原生态，进口等标签，但是随手一搜关于美国鲤鱼的关键词都是：泛滥、超标、污染、重金属、破坏生态……可以说名声在外，深入人心，当然，不排除恶意夸大的成分，但是扭转全网认知是需要时间和巨大投入的
# 5. 后期听说搞了鱼丸、火锅鱼片这些东西
# 6. 没有天敌，任其发育的草食鱼一般不好吃。
# 7. 实在不行，做猫罐头啊，来自主子的怒吼
# 8. 可能正是因为不好吃，才没有天敌
# 9. 真的难吃吗，
# 10. 而且卖价还比国内活鱼高好几倍。能卖的出去才见了鬼了。
# 11. 不能深加工吗？鱼肉好歹是优质蛋白质吧
# 12. 叉子都戳不破，看来真不能吃
# 13. 没有天敌，任其发育的草食鱼一般不好吃。
# 14. 做成重口味的熏鱼不知道怎么样
# 15. 一听说个头一人抱不起来就知道好吃不了……听说有人在美国直接建厂加工成鱼丸卖回国了，不知道市场如何
# 16. 估计黄了，刚淘宝了一下
# 17. 实在不行，做猫罐头啊，来自主子的怒吼
# 18. 做蛋白粉
# 19. 支持做成猫罐头
# 20. 草鱼长太大了肯定不好吃
# 21. 做猫粮应该可以
# 22. 做猫罐头怎么样
# 23. 脏，美国那边五大湖。。。重金属污染
# ……………………