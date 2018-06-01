# JSON格式：
#
# 问题1：GITHUB给的很乱，有些是team，有些是项目
# 问题2：YOUTUBE
# 也很乱
# 有些是channel
# 有些是视频
# 有些是c的标签
# https: // www.youtube.com / neonexchange
# https: // www.youtube.com / channel / UCzhJz9g - T5BWjbPeJLKY_jw
# https: // www.youtube.com / c / ProjectShivom
# 目前API中能爬取的只有第二种
# 当前代码给出的案例是可以爬取的
# 代码：
import urllib.request
import re
from lxml import etree
import json

header = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}


def GetYoutubeViewCount(YouTubeurl):
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
        request = urllib.request.Request(url + id + "&key=" + key)

        # 爬取结果

        response = urllib.request.urlopen(request)

        data = response.read().decode('utf-8')

        data = json.loads(data)
        data = data['items'][0]['statistics']['viewCount']

        print(data)
        res = Tag
        resnum = data
    finally:
        return res, resnum


def getGitHubStar(url):
    tag = "GitHubStar";

    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    data = res.read()
    selector = etree.HTML(data)
    url = url.replace("https://github.com/", "");
    path = '//a[@href="/' + url.replace("https://github.com", "") + '/stargazers"]/text()'
    '//a[@href="/bitcoin/bitcoin/stargazers"]/text()'
    print("path", path)
    data = selector.xpath(path)
    data = re.sub("[^\d]", "", data[0])
    print(data.strip())

    return tag, data.strip()


def GetEtherscanAddress(url):
    tag = "EtherscanAddress"
    request = urllib.request.Request(url, headers=header)
    # 爬取结果
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('utf-8')
    # 设置解码方式
    selector = etree.HTML(data)
    item = selector.xpath("//table[@class='table']/tr[3]/td[2]/text()")
    data = re.sub("[^\d]", "", item[0])
    print(data)
    return tag, data


def getAlexaRank(site):
    tag = "AlexaRank"
    url = 'http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % site
    print(type(url))
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()

    selector = etree.XML(data)
    global_rank = selector.xpath('//SD/REACH/@RANK')
    country_rank = selector.xpath('//SD/COUNTRY/@RANK')

    print('WebRank：%s' % site)
    print('GlobalRank = %s' % global_rank[0])
    print('ChineseRank = %s' % country_rank[0])
    dict = {'GlobalRank': global_rank[0], 'ChineseRank': country_rank[0]}

    return tag, dict


def getTlegramChannelSize(url):
    tag = 'TlegramChannelSize'
    request = urllib.request.Request(url)
    data = urllib.request.urlopen(request).read()
    selector = etree.HTML(data)
    result = selector.xpath("//div[@class='tgme_page_extra']/text()")
    result = re.sub("[^\d]", "", result[0])
    return tag, result


js = {
    "QuarkChain ":
        {"web": "https://www.quarkchain.io/",
         "telegram": "https://t.me/quarkchain",
         "github": "https://github.com/iotexproject/iotex-core",
         "???": 'https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0',
         "youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"},

}
if __name__ == '__main__':
    dict = {}
    print(type(js.keys()))
    res = {}
    for name in js.keys():

        js_dict = js[name]
        if "youtube" in js_dict.keys():
            Tag, num = GetYoutubeViewCount(js_dict["youtube"])

            if (Tag != False):
                dict[Tag] = num;
        if "web" in js_dict.keys():
            Tag, num = getAlexaRank(js_dict["web"])
            dict[Tag] = num;
        if "???" in js_dict.keys():
            Tag, num = GetEtherscanAddress(js_dict["???"])
            dict[Tag] = num;
        if "github" in js_dict.keys():
            Tag, num = getGitHubStar(js_dict["github"])
            dict[Tag] = num;
        if "telegram" in js_dict.keys():
            Tag, num = getTlegramChannelSize(js_dict["telegram"])
            dict[Tag] = num;
        print(dict)
        res[name] = dict

# 设置解码方式









