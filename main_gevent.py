import json
import re
import time
import urllib.request
from multiprocessing import Pool

import gevent
from lxml import etree
from selenium import webdriver
#simulate a browser to be prevented
header = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}
#simulate click or hover via using phantomjs
driver = webdriver.PhantomJS(
    executable_path='./phantomjs')
class JSONObject():
    def __init__(self,d):
        self.__dict__=d

class ICOTerm():
    def __init__(self, term_dict):
        self.web = term_dict['web']
        self.youtube = term_dict['youtube']
        self.github = term_dict['github']
        # self.etherscan = term_dict['???']
        self.telegram = term_dict['telegram']
        self.twitter = term_dict['twitter']
        self.result = {}			# storage the result

	# get request via urllib
    def getResponse(self, url):
        # start=time.time()
        request = urllib.request.Request(url, headers=header)
        try:
            data = urllib.request.urlopen(request).read()

        except Exception as e:
            print("exception", e)
            return
        # print("url ",url,"read over",(time.time()-start))

        return data

    def GetYoutubeViewCount(self):
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
                request = urllib.request.Request(YouTubeurl)
                response = urllib.request.urlopen(request)

                data = response.read().decode('utf-8')

                path = '// meta[ @ property = "og:url"] /@content'
                selector = etree.HTML(data)
                data = selector.xpath(path)
                if (len(data) == 0):
                    raise Exception("Youtube域名出错")
                else:
                    YouTubeurl = data[0]
            id = re.findall("(?<=/)[A-Za-z0-9_-]+$", YouTubeurl)[0];
            # url = url + id + "&key=AIzaSyAZj7k542xJe9zZSX0Boka858oZ_1RSlC4"

            data = next(self.getResponse(url + id + "&key=" + key))
            data = data.decode('utf-8')
            data = json.loads(data)
            if len(data['items']) == 0:
                return
            data = data['items'][0]['statistics']['viewCount']

            res = Tag
            resnum = data
        except Exception as e:
            print(e)
            pass
        finally:
            self.result[res] = resnum
            print('youtu over')

    # def GetEtherScanAddress(self):
    #     tag = "EtherScanAddress"
    #     if self.etherscan == '':
    #         self.result[tag] = 0
    #         return
    #     data = next(self.getResponse(self.etherscan, True))
    #     selector = etree.HTML(data)
    #     item = selector.xpath("//table[@class='table']/tr[3]/td[2]/text()")
    #     data = re.sub("[^\d]", "", item[0])
    #     self.result[tag] = data
    #     print('ether over')

    def getAlexaRank(self):
        tag = "AlexaRank"
        if self.web == '':
            return
        url = ('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % self.web)
        data = next(self.getResponse(url))
        # data = data.decode('gbk')
        # print(data)
        selector = etree.XML(data)
        global_rank = selector.xpath('//SD/REACH/@RANK')
        country_rank = selector.xpath('//SD/COUNTRY/@RANK')
        dict_res = {}
        if len(global_rank) == 0:
            dict_res['GlobalRank'] = 0
            self.result[tag] = dict_res
            return
        else:
            dict_res['GlobalRank'] = global_rank[0]
        if len(country_rank) != 0:
            dict_res['COUNTRY_RANK'] = country_rank[0]
        self.result[tag] = dict_res
        print('alexa over')

    def getGitHubStar(self):
        tag = "GitHubStar"
        res={}
        if self.github == '':
            return
        data = (self.getResponse(self.github.replace('github','api.github')))
        if data is None:
            return
        res_json = json.loads(data, object_hook=JSONObject)

        res['stargazers_count'] = res_json.stargazers_count
        res['watchers_count'] = res_json.watchers_count
        res['forks'] = res_json.forks
        res['open_issues'] = res_json.open_issues
        res['subscribers_count'] = res_json.subscribers_count
        res['network_count'] = res_json.network_count
        res['size'] = res_json.size
        res['open_issues'] = res_json.open_issues
        res['open_issues'] = res_json.open_issues
        rule = re.compile(r'{[[/s/S].*?}')
        comments = re.sub(rule, '', res_json.comments_url)
        commits = re.sub(rule, '', res_json.commits_url)
        contributors = res_json.contributors_url
        subscribers = res_json.subscribers_url
        wait={
            'comments':comments,
            'commits':commits,
            'contributors':contributors,
            'subscribers':subscribers
        }
        for k,v in wait.items():
            res[k]=len(json.loads((self.getResponse(v)), object_hook=JSONObject))
        self.result[tag]=res

        # selector = etree.HTML(data)
        # url = self.github.replace("https://github.com/", "");
        # path = '//a[@href="/' + url.replace("https://github.com", "") + '/stargazers"]/text()'
        # '//a[@href="/bitcoin/bitcoin/stargazers"]/text()'
        # data = selector.xpath(path)
        # if len(data) == 0:
        #    return
        # data = re.sub("[^\d]", "", data[0])
        # self.result[tag] = data.strip()
        print('git over',res)

    def getTelegramChannelSize(self):
        tag = 'TelegramChannelSize'
        if self.telegram == '':
            return
        data = next(self.getResponse(self.telegram))
        selector = etree.HTML(data)
        result = selector.xpath("//div[@class='tgme_page_extra']/text()")
        result = re.sub("[^\d]", "", result[0])
        self.result[tag] = result
        print('tele over')

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
	#gevents
    def MulTreGetter(self):

        gevent.joinall([
                        # gevent.spawn(self.getAlexaRank()),
                       gevent.spawn(self.getGitHubStar()),
                       # gevent.spawn(self.getTelegramChannelSize()),
                       # gevent.spawn(self.getTwitterFollowers()),
                       # gevent.spawn(self.GetYoutubeViewCount())
                       ])

        return self.result


if __name__ == "__main__":
    t = time.time()
    p = Pool()
    processes = {}
    Terms = {}
    res = {}
    file = open('ico_projs.json', "r")
    fileJson = json.load(file)
    for ico_proj in fileJson:
        result = ICOTerm(ico_proj)
        Terms[ico_proj["name"]] = result
    #multi-processes
    for term in Terms.keys():
        result = p.apply_async(Terms[term].MulTreGetter)
        processes[term] = result

    p.close()
    p.join()
    #wait all processes done
    driver.quit()
    for proc in processes.keys():
        res[proc] = processes[proc].get()
    res['date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(res)
    print(time.time() - t)
    # convert result to a json format and write in a file
    filename = 'ico.json'
    fp = open(filename, 'a+')
    fp.write(json.dumps(res))
    fp.close()
