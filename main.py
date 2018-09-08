import requests
import re
from lxml import etree
from multiprocessing import Pool
from multiprocessing import Process
from selenium import webdriver
import json
import asyncio,aiohttp,logging
from aiofile import Writer,AIOFile
from bs4 import BeautifulSoup
import os
from colorlog import ColoredFormatter

logger = logging.getLogger()  # 创建一个logger对象
logger.setLevel('INFO')
BASIC_FORMAT = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s'
DATE_FORMAT = '%Y-%m-%d %A %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
color_formatter = ColoredFormatter('%(log_color)s[%(module)-15s][%(funcName)-20s][%(levelname)-8s] %(message)s')
chlr = logging.StreamHandler() # 输出到控制台的handler
chlr.setFormatter(color_formatter)
chlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
fhlr = logging.FileHandler('logger.log') # 输出到文件的handler
fhlr.setFormatter(color_formatter)
logger.addHandler(chlr)
logger.addHandler(fhlr)
import stem
import stem.connection
from stem.control import Controller
from stem import Signal

from threading import Thread
#simulate a browser to be prevented
header = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}

proxies={
    "http" : "127.0.0.1:8118",
    "https" : "127.0.0.1:8118"
}
# #proxy="127.0.0.1:8118"
# # Build ProxyHandler object by given proxy
# proxy_support=urllib.request.ProxyHandler(proxies)
# # Build opener with ProxyHandler object
# opener = urllib.request.build_opener(proxy_support)
# # Install opener to request
# urllib.request.install_opener(opener)



#simulate click or hover via using phantomjs

driver = webdriver.PhantomJS(
    executable_path='./phantomjs',
)

class JSONObject():
    def __init__(self,d):
        self.__dict__=d

#define a class
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

    # get request via urllib
    # def getResponse(self, url):
    #     request = urllib.request.Request(url, headers=header)
    #     # print('ip is :',urllib.request.urlopen(urllib.request.Request("http://icanhazip.com", headers=header)).read())
    #     try:
    #         data = urllib.request.urlopen(request).read()
    #     except Exception as e:
    #         print("exception", e)
    #         return
    #     return data

    async def getResponseAsync(self,url):
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(url) as resp:
                return await resp.text()

    async def GetYoutubeViewCount(self):
        Tag = "YoutubeChannelViewCount"
        YouTubeurl = self.youtube
        if YouTubeurl == '':
            return
        res = False
        resnum = 0
        try:
            id = re.findall("(?<=/)[A-Za-z0-9_-]+$", YouTubeurl)[0];
            key = "AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"
            url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id='
            # id = "UCbzLOZaEegUfTVBJQeSc0sw"
            if "channel" not in YouTubeurl:
                # url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=' + id + "&key=AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"
                data = await self.getResponseAsync(YouTubeurl)
				# get data via xpath
                path = '// meta[ @ property = "og:url"] /@content'
                selector = etree.HTML(data)
                data = selector.xpath(path)
                if (len(data) == 0):
                    logging.error('youtube url is illegal')
                else:
                    YouTubeurl = data[0]

            id = re.findall("(?<=/)[A-Za-z0-9_-]+$", YouTubeurl)[0];
            # url = url + id + "&key=AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"
            data = await self.getResponseAsync(url + id + "&key=" + key)
            data = json.loads(data)
            if len(data['items']) == 0:
                return
            data = data['items'][0]['statistics']['viewCount']

            res = Tag
            resnum = data
        except Exception as e:
            logging.error(e)
            pass
        finally:
            logging.info('{} youtube over {}'.format(self.youtube,resnum))
            self.result[res] = resnum


    # def GetEtherScanAddress(self):
    #     tag = "EtherScanAddress"
    #     if self.etherscan == '':
    #         self.result[tag] = 0
    #         return
    #     data = self.getResponse(self.etherscan, True)
    #     selector = etree.HTML(data)
    #     item = selector.xpath("//table[@class='table']/tr[3]/td[2]/text()")
    #     data = re.sub("[^\d]", "", item[0])
    #     self.result[tag] = data
    #     print('ether over')

    async def getAlexaRank(self):
        tag = "AlexaRank"
        if self.web == '':
            return
        url = ('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % self.web)
        data = await self.getResponseAsync(url)
        soup = BeautifulSoup(data, 'lxml')
        dict_res = {}
        dict_res['global_rank']=0
        dict_res['country_rank']= 0
        try:
            dict_res['global_rank'] = soup.reach['rank']
            dict_res['country_rank'] = soup.country['rank']
        except TypeError as e:
            logging.error(self.web+'has no rank')
        self.result[tag] = dict_res
        logging.info('{} alexa over {}'.format(self.web, dict_res))
        # selector = etree.XML(data)
        # global_rank = selector.xpath('//SD/REACH/@RANK')
        # country_rank = selector.xpath('//SD/COUNTRY/@RANK')

        # if len(global_rank) == 0:
        #     dict_res['GlobalRank'] = 0
        #     self.result[tag] = dict_res
        #     return
        # else:
        #     dict_res['GlobalRank'] = global_rank[0]
        # if len(country_rank) != 0:
        #     dict_res['COUNTRY_RANK'] = country_rank[0]

    async def getGitHubStar(self):
        tag = "GitHubStar"
        res={}
        if self.github.endswith('/'):
            self.github = self.github[:-1]
        if self.github == '' or len(self.github.split('/'))<5:
            logging.error(self.github+' is not a repo url')
            return
        data = await self.getResponseAsync(self.github)

        rule = re.compile('\s+')
        soup = BeautifulSoup(data, 'lxml')
        url = self.github.replace("https://github.com/", "");

        res['stargazers'] = 0
        res['watchers'] = 0
        res['network/members'] = 0

        def getNum(item):
            item=soup.select('[href=/'+url+'/'+str(item)+']')
            if len(item):
                return re.sub(rule,'',item[0].string)
            else:
                return 0

        for k,v in res.items():
            res[k]=getNum(v)

        item=soup.find_all(class_='num text-emphasized')
        res['commits'] = re.sub(rule,'',item[0].string)
        res['branches'] = re.sub(rule,'',item[1].string)
        res['releases'] = re.sub(rule,'',item[2].string)
        try:
            res['contributors'] = re.sub(rule,'',item[3].string)
        except TypeError as e:
            logging.error('{},{}'.format(e,self.github))
        item=soup.find_all(class_='Counter')
        res['issues'] = re.sub(rule, '', item[0].string)
        res['PullRequest'] = re.sub(rule, '', item[1].string)
        res['Projects'] = re.sub(rule, '', item[2].string)


        self.result[tag] = res
        logging.info('{} git over {}'.format(self.github,res))

        # res_json = json.loads(data, object_hook=JSONObject)
        # try:
        #     res['stargazers_count'] = res_json.stargazers_count
        #     res['watchers_count'] = res_json.watchers_count
        #     res['forks'] = res_json.forks
        #     res['open_issues'] = res_json.open_issues
        #     res['subscribers_count'] = res_json.subscribers_count
        #     res['network_count'] = res_json.network_count
        #     res['size'] = res_json.size
        #     res['open_issues'] = res_json.open_issues
        #     res['open_issues'] = res_json.open_issues
        #     rule = re.compile(r'{[[/s/S].*?}')
        #     comments = re.sub(rule, '', res_json.comments_url)
        #     commits = re.sub(rule, '', res_json.commits_url)
        #     contributors = res_json.contributors_url
        #     subscribers = res_json.subscribers_url
        # except AttributeError as e:
        #     logging.error(e)
        # wait={
        #     'comments':comments,
        #     'commits':commits,
        #     'contributors':contributors,
        #     'subscribers':subscribers
        # }
        # for k,v in wait.items():
        #     res[k]=len(json.loads(await (self.getResponseAsync(v)), object_hook=JSONObject))
        # self.result[tag]=res

    async def getTelegramChannelSize(self):
        tag = 'TelegramChannelSize'
        if self.telegram == '':
            return
        data = await self.getResponseAsync(self.telegram)
        soup=BeautifulSoup(data,'lxml')
        result=soup.select('.tgme_page_extra')[0].string
        # result = selector.xpath("//div[@class='tgme_page_extra']/text()")
        result = re.sub("[^\d]", "", result)
        self.result[tag] = result
        logging.info('{} tele over {}'.format(self.telegram,result))

    def getTwitterFollowers(self):
        tag = "TwitterFollowers"
        if self.twitter == '':
            return
        driver.get(self.twitter)

        selector = etree.HTML(driver.page_source)
        followers = selector.xpath('//span[@class="ProfileNav-value" and @data-is-compact="true"]/@data-count')
        if len(followers) == 0:
            return
        count = followers[0]
        self.result[tag] = count
        print('twitter over')
    async def renew_connection(self):
        with Controller.from_port(port = 9051) as controller:
            controller.authenticate(password = 'fyl815')
            controller.signal(Signal.NEWNYM)
            controller.close()

    @asyncio.coroutine
    async def writeResult(self):
        async with AIOFile('ico.json', 'a') as afp:
            writer = Writer(afp)
            await writer(self.result)
            await afp.fsync()
            logging.info('{} json is writed'.format(self.result['id']))
	#threads
    def MulTreGetter(self):
        threads = [
                    # Thread(target=self.renew_connection),
                    # Thread(target=self.GetYoutubeViewCount),
                    Thread(target=self.getAlexaRank),
                    # Thread(target=self.getGitHubStar),
                    # Thread(target=self.getTelegramChannelSize),
                    # Thread(target=self.getTwitterFollowers)
        ]
        # threads.append(Thread(target=self.GetEtherscanAddress))

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.result
    async def tasks(self):
        await self.getAlexaRank()
        await self.getTelegramChannelSize()
        # await self.renew_connection()
        await self.getGitHubStar()
        await self.GetYoutubeViewCount()




if __name__ == "__main__":

    import time,collections
    start = time.time()
    Terms={}
    postData = collections.defaultdict(list)
    file = open('ico_projs.json', "r")
    fileJson = json.load(file)
    for ico_proj in fileJson:
        result = ICOTerm(ico_proj)
        Terms[ico_proj["id"]] = result
    logging.info('Initialize via json')
    tasks=[v.tasks() for k,v in Terms.items()]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    # writeTasks=[v.writeResult() for k,v in Terms.items()]
    # loop.run_until_complete(asyncio.wait(writeTasks))
    for k,v in Terms.items():
        postData['data'].append(v.result)
    postData['date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    filename = 'ico.json'
    fp = open(filename, 'a')
    fp.write(json.dumps(postData))
    fp.close()
    logging.info('cost time ' + str(time.time() - start))
    # t = time.time()
    # p = Pool(10)#todo
    # processes, Terms, res = {}, {}, {}
    # postData=collections.defaultdict(list)
    # #multi-processes
    # for term in Terms.keys():
    #     result = p.apply_async(Terms[term].MulTreGetter)
    #     processes[term] = result
    # p.close()
    # p.join()
    # #wait all processes done
    # driver.quit()
    # for proc in processes.keys():
    #     res[proc] = processes[proc].get()
    #     postData['data'].append(res[proc])
    # postData['date'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #
    # print(res)
    # print(time.time() - t)
	#convert result to a json format and write in a file
    # filename = 'ico.json'
    # fp = open(filename,'a')
    # fp.write(json.dumps(postData))
    # fp.close()




    #TEST
    # 让Tor重建连接，获得新的线路
    # import stem
    # import stem.connection

    # from stem import Signal
    # from stem.control import Controller
    # def renew_connection():
    #     with Controller.from_port(port=9051) as controller:
    #         controller.authenticate(password='fyl815')
    #         controller.signal(Signal.NEWNYM)
    #         controller.close()
    # def get_public_ip(headers):
    #     request = urllib.request.Request("http://icanhazip.com", headers=headers)
    #     data = urllib.request.urlopen(request).read()
    #     print(data)

    # for i in range(10):
    #     # renew_connection()
    #     get_public_ip(header)

