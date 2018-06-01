import urllib.request
import re
from lxml import etree
import json,time
header = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}
js = """{
	"QuarkChain ": {
		"web": "https://www.quarkchain.io/",
		"telegram": "https://t.me/quarkchain",
		"github": "https://github.com/iotexproject/iotex-core",
		"???": "https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0",
		"youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"
	},
	"a":{
	    "web":"http://www.baidu.com",
	    "telegram": "https://t.me/quarkchain",
        "github": "https://github.com/iotexproject/iotex-core",
        "???": "https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0",
        "youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"
	}
}"""
#make a proxy for request
proxies = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
proxy_support = urllib.request.ProxyHandler(proxies)
opener = urllib.request.build_opener(proxy_support)

class ICOTerm:
    def __init__(self, term_dict):
        self.web        =term_dict['web']
        self.youtube    =term_dict['youtube']
        self.github     =term_dict['github']
        self.etherscan  =term_dict['???']
        self.telegram   =term_dict['telegram']
        self.result={}
    def getResponse(self,url,decoding=False,headers=header):
        # start=time.time()
        request = urllib.request.Request(url, headers=header)
        try:
            response = opener.open(request)
            data = response.read()
        except Exception as e:
            print("exception",e)
            return
        # print("url ",url,"read over",(time.time()-start))
        if decoding:
            data.decode('utf-8')
        return data

    def GetYoutubeViewCount(self):
        YouTubeurl = self.youtube
        res = False
        resnum = 0
        try:
            Tag = "YoutubeChannelViewCount"
            id = re.findall("(?<=/)[A-Za-z0-9_-]+$", YouTubeurl)[0];
            key = "AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"
            # id = "UCbzLOZaEegUfTVBJQeSc0sw"
            if ("channel" in YouTubeurl):
                url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id='
                # url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id='+id+"&key=AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"
                "https://www.googleapis.com/youtube/v3/videos"
            else:
                # url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=' + id + "&key=AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"
                url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                Tag = "YoutubeVideoViewCount"

            # url = url + id + "&key=AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"

            data = self.getResponse(url + id + "&key=" + key,True)
            data = json.loads(data)
            data = data['items'][0]['statistics']['viewCount']

            res = Tag
            resnum = data
        except Exception as e:
            print(e)
            pass
        finally:
            self.result[res]= resnum
            print('youtu over')

    def GetEtherscanAddress(self):
        tag = "EtherscanAddress"
        data = self.getResponse(self.etherscan,True)
        selector = etree.HTML(data)
        item = selector.xpath("//table[@class='table']/tr[3]/td[2]/text()")
        data = re.sub("[^\d]", "", item[0])
        self.result[ tag]= data
        print('ether over')
    def getAlexaRank(self):
        tag = "AlexaRank"
        url = ('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (self.web))
        data = self.getResponse((url))

        selector = etree.XML(data)
        global_rank = selector.xpath('//SD/REACH/@RANK')
        country_rank = selector.xpath('//SD/COUNTRY/@RANK')

        dict_res = {'GlobalRank': global_rank[0], 'ChineseRank': country_rank[0]}
        self.result[ tag]= dict_res
        print('alexa over')
    def getGitHubStar(self):
        tag = "GitHubStar";
        data = self.getResponse(self.github)
        selector = etree.HTML(data)
        url = self.github.replace("https://github.com/", "");
        path = '//a[@href="/' + url.replace("https://github.com", "") + '/stargazers"]/text()'
        '//a[@href="/bitcoin/bitcoin/stargazers"]/text()'
        data = selector.xpath(path)
        data = re.sub("[^\d]", "", data[0])
        self.result[ tag]= data.strip()
        print('git over')
    def getTlegramChannelSize(self):
        tag = 'TlegramChannelSize'
        data = self.getResponse(self.telegram)
        selector = etree.HTML(data)
        result = selector.xpath("//div[@class='tgme_page_extra']/text()")
        result = re.sub("[^\d]", "", result[0])
        self.result[ tag]= result
        print('tele over')
    #def callbackEvent(self):
        #print("callback start")
        #self.event.wait()
        #eve.rawlink(lambda : print(ico.result))
        #print("callback over")
if __name__=='__main__':

    # import aiohttp
    # import asyncio
    # async def get(url):
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url) as resp:
    #             print(url, resp.status)
    #             print(url, await resp.text())
    #
    #
    # loop = asyncio.get_event_loop()  # 得到一个事件循环模型
    # tasks = [  # 初始化任务列表
    #     ico.getResponse("http://zhushou.360.cn/detail/index/soft_id/3283370",lambda :print("111")),
    #     ico.getResponse("http://zhushou.360.cn/detail/index/soft_id/3264775",lambda :print("222")),
    #     ico.getResponse("http://zhushou.360.cn/detail/index/soft_id/705490",lambda :print("333"))
    # ]
    # loop.run_until_complete(asyncio.wait(tasks))  # 执行任务
    # loop.close()
    import gevent
    class JSONObject:
        def __init__(self, d):
            self.__dict__ = d
    data=json.loads(js,object_hook=JSONObject)
    ico_list=[item for item in data.__dict__.items()]
    r=[]
    def func(msg):
        print('ico',msg)
        ico=ICOTerm(msg)
        r.append(ico)
        #make a coroutines via gevent
        gevent.joinall(gevent.spawn(ico.getAlexaRank()),
                       gevent.spawn(ico.getGitHubStar()),
                       gevent.spawn(ico.getTlegramChannelSize(),timeout=60),
                       gevent.spawn(ico.GetEtherscanAddress(),timeout=60),
                       gevent.spawn(ico.GetYoutubeViewCount())
                       )
        # print(ico.result)
        # ico.GetYoutubeViewCount()
        # Tag, num = ico.GetYoutubeViewCount()
        # dict[Tag] = num
        # Tag, num = ico.getAlexaRank()
        # dict[Tag] = num
        # Tag, num = ico.GetEtherscanAddress()
        # dict[Tag] = num
        # print('dict is ',dict[Tag])
        # Tag, num = ico.getGitHubStar()
        # dict[Tag] = num;
        # Tag, num = ico.getTlegramChannelSize()
        # dict[Tag] = num
        # print(ico.result)
    # import gevent
    # import time
    # start=time.time()
    # gevent.joinall([gevent.spawn(func,ico[1].__dict__ ) for ico in ico_list])
    # print((time.time()-start)*1000)
    # import time
    # start=time.time()
    # func(ico_list[0][1].__dict__)
    # print((time.time()-start)*1000)
    #make a processPool for evert iten
    from multiprocessing.dummy import Pool
    import multiprocessing
    import time
    start=time.time()
    pool=Pool(2)
    for i in ico_list:
        pool.apply_async(func,(i[1].__dict__,))
    pool.close()
    pool.join()
    print((time.time()-start))
    #for result
    gevent.sleep(10)
    print([i.result for i in r])
    # def inner_func(msg,i):
    #     print("main_msg:",msg,"inner_msg:" ,i)
    #     time.sleep(2)
    #     return
    #
    # def func(msg):
    #     print("msg:", msg)
    #     pool=Pool(10)
    #     for _ in range(100):
    #         pool.apply_async(inner_func,(msg,_))
    #     pool.close()
    #     pool.join()
    #     return ("end"+msg)
    #
    #
    # if __name__ == "__main__":
    #
    #     pool = Pool(4)
    #
    #     res=[]
    #     for i in range(4):
    #         (pool.apply_async(func, (i,)) ) # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    #
    #     pool.close()
    #     pool.join()
    #      # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    #     print("Sub-process(es) done.")