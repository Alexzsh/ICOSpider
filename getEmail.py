import urllib.request
import re
from lxml import etree
import json,time

header = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
proxies = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
proxy_support = urllib.request.ProxyHandler(proxies)
opener = urllib.request.build_opener(proxy_support)
import ssl
ssl._create_default_https_context=ssl._create_unverified_context

# baseurl="https://icotracker.net/"
# req=urllib.request.Request(baseurl,headers=header)
# # data=opener.open(req).read()
# data=urllib.request.urlopen(req).read()
# seletor=etree.HTML(data)
# item=seletor.xpath('//div[@class="cp-line text-nowrap"]/a//@href')
# item_cleanLinkIn=list(filter(lambda x: 'linkedin' not in str(x),item))
# res_dict = {}
# with open('icoWebsite.txt','w',encoding='utf-8') as fw:
#     for i in item_cleanLinkIn:
#         fw.write(i+'\n')
f=open('icoResult.txt', 'w', encoding='utf-8')
def fun(x):
    print('fun')
    try:
        req = urllib.request.Request(x, headers=headers)
        data = opener.open(req).read()
    except Exception as e:
        print(e)
    print("get data over")
    try:
        seletor = etree.HTML(data)
        item = seletor.xpath('//footer//a/@href')
        rule = re.compile(r'.*@\w*\.\w*')
        res = list(filter(lambda x: rule.match(x), item))
    except Exception as e:
        print(e)
        res = ""

    print("get res over")

    f.write(str(x) + ',' )
    if res=="":
        f.write('null')
    else:
        for i in res:
            f.write(str(i)+',')
    f.write('\n')

    # with open('icoResult.txt','w',encoding='utf-8') as f:
    #     for k,v in enumerate(icoWebsite):
    #         x,res=fun(k,v)
    #         f.write(str(x)+','+str(res)+'\n')
if __name__=='__main__':
    # with open('icoWebsite.txt', 'r', encoding='utf-8') as fr:
    #     icoWebsite = []
    #     icoWebsite.extend(list(web.strip() for web in fr.readlines()))
    # res_dict = {}
    # for i in icoWebsite:
    #     fun(i)
    # from multiprocessing import Pool, Process
    # import time
    #
    # start = time.time()
    # pool = Pool(25)
    # pool.map(fun,icoWebsite)
    # pool.close()
    # pool.join()
    # print("main process over %0.2fs" % (time.time() - start))
    # f.close()
    filename='icoResult.txt'
    import pandas as pd
    # df=pd.read_csv('icoResult.txt',sep=',')
    # print(df.head())
    r=[]
    with open(filename,'r') as f:
        for i in f.readlines():
            if i.endswith(','):
                i.replace(',','')
                r.append(i)
    with open(filename,'w') as fw:
        map(lambda x:fw.write(x),r)