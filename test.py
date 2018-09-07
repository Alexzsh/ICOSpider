import urllib.request
import re
import collections
from lxml import etree
import time
from multiprocessing import Pool
from multiprocessing import Process
from selenium import webdriver
import json
import asyncio,aiofile,aiohttp,logging
# import stem
# import stem.connection
# from stem.control import Controller
# from stem import Signal

from threading import Thread
#simulate a browser to be prevented
header = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}

proxies={
    "http" : "127.0.0.1:1086",
    "https" : "127.0.0.1:1086"
}
#proxy="127.0.0.1:8118"
# Build ProxyHandler object by given proxy
proxy_support=urllib.request.ProxyHandler(proxies)
# Build opener with ProxyHandler object
opener = urllib.request.build_opener(proxy_support)
# Install opener to request
urllib.request.install_opener(opener)

result={}
async def getResponseAsync(url):
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url) as resp:
            return await resp.text()

async def getAlexaRank(web):
    tag = "AlexaRank"
    if web == '':
        return
    url = ('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % web)
    data = await getResponseAsync(url)
    # data = data.decode('gbk')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(data, 'lxml')
    global_rank=soup.reach['rank']
    country_rank=soup.country['rank']
    # selector = etree.XML(data)
    # global_rank = selector.xpath('//SD/REACH/@RANK')
    # country_rank = selector.xpath('//SD/COUNTRY/@RANK')
    dict_res = {}
    if len(global_rank) == 0:
        dict_res['GlobalRank'] = 0
        result[tag] = dict_res
        return
    else:
        dict_res['GlobalRank'] = global_rank[0]
    if len(country_rank) != 0:
        dict_res['COUNTRY_RANK'] = country_rank[0]
    result[tag] = dict_res
    print('alexa over',dict_res)
class ICOTerm():
    def __init__(self, term_dict):
        self.web = term_dict['web']
        self.youtube = term_dict['youtube']
        self.github = term_dict['github']
        # self.etherscan = term_dict['???']
        self.telegram = term_dict['telegram']
        # self.twitter = term_dict['twitter']
        self.result = {}					# storage the result
        self.result['id'] = term_dict['id']
        self.result['name'] = term_dict['name']
processes, Terms, res = {}, {}, {}
# postData=collections.defaultdict(list)
file = open('ico_projs.json', "r")
fileJson = json.load(file)
for ico_proj in fileJson:
    result = ICOTerm(ico_proj)
    Terms[ico_proj["id"]] = result

tasks=[getAlexaRank(v.web) for k,v in Terms.items()]
loop=asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

# sss='''<!--
#  Need more Alexa data?  Find our APIs here: https://aws.amazon.com/alexa/
# -->
# <ALEXA VER="0.9" URL="sparkster.me/" HOME="0" AID="=" IDN="sparkster.me/">
# <RLS PREFIX="http://" more="0"> </RLS>
# <SD TITLE="A" FLAGS="" HOST="sparkster.me"> </SD>
# <SD>
# <POPULARITY URL="sparkster.me/" TEXT="102940" SOURCE="panel"/>
# <REACH RANK="112749"/>
# <RANK DELTA="-132942"/>
# <COUNTRY CODE="IN" NAME="India" RANK="75540"/>
# </SD>
# </ALEXA>'''
#
# from bs4 import BeautifulSoup
# soup=BeautifulSoup(sss,'lxml')
# # for i in soup.descendants:
# #     print(i)
