import requests
import json
import re

def getObj():	
    headers = {
    
    }
    params = (
        ('include', 'data[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,is_parent_author,is_author'),
        ('limit', '10'), 
        ('offset', '0'), # 0 10 20 ......
        ('order', 'normal'),
        ('status', 'open'),
    )

    # response = requests.get('https://www.zhihu.com/api/v4/answers/527558575/root_comments?include=data%5B%2A%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&limit=10&offset=0&order=normal&status=open', headers=headers)
    response = requests.get('https://www.zhihu.com/api/v4/answers/527558575/root_comments', headers=headers, params=params)
    res_data = json.loads(response.text) # load JSON to object
    print("当前链接 params 的 offset 值为" + params[2][1] + ", 下面为抓取到的评论:")
    print("-------------------------------------------------------------------")
    return res_data
    

def printComs():
    dataObj = getObj()
    # print(dataObj)

    for i in range(len(dataObj["data"])):
        contents = dataObj["data"][i]["content"]

        if contents[0] == "<" :
            res = r'<p>(.*?)</p>'
            m = re.findall(res, contents, re.S|re.M)
            for value in m:
                print(value)
        else:
            print(contents)


def main():
    printComs()


main()

