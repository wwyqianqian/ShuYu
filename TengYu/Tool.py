# -*- coding:utf-8 -*-
__author__ = 'TengYu'
import re

#工具类，用来去除爬取的正文中一些不需要的链接、标签等
class Tool:
    deleteImg = re.compile('<img.*?>')
    newLine =re.compile('<tr>|<div>|</tr>|</div>')
    deleteAite = re.compile('//.*?:')
    deleteAddr = re.compile('<a.*?>.*?</a>|<a href='+'\'https:')
    deleteTag = re.compile('<.*?>')
    deleteWord = re.compile('回复@|回覆@|回覆|回复')

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
