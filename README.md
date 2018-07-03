# ICOSpider

### 1、数据请求接口


name|parameter|type|result
:---|:----|:-----|:-----
getData()|None|GET|json

**json格式 字段变动直接在单个项目中修改**
```json
[
  {
    "name": "QuarkChain ",
    "web": "https://www.quarkchain.io/",
    "telegram": "https://t.me/quarkchain",
    "github": "https://github.com/iotexproject/iotex-core",
    "???": "https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0",
    "youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"
  },
  {
    "name":"a",
    "web": "http://www.baidu.com",
    "telegram": "https://t.me/quarkchain",
    "github": "https://github.com/iotexproject/iotex-core",
    "???": "https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0",
    "youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"
  }
]
```

### 2、结果发送接口
name|parameter|type|result
:---|:----|:-----|:-----
postData(json)|json|POST|None

```json
{
	"QuarkChain ": {
		"AlexaRank": {
			"GlobalRank": "86186",
			"COUNTRY_RANK": "119965"
		},
		"GitHubStar": "746",
		"TelegramChannelSize": "3587",
        "TwitterFollowers": "1234",
        "YoutubeChannelViewCount":"1234"
	},
	"a": {
		"AlexaRank": {
			"GlobalRank": "4",
			"COUNTRY_RANK": "1"
		},
		"GitHubStar": "746",
		"TelegramChannelSize": "3587",
        "TwitterFollowers": "1234",
        "YoutubeChannelViewCount":"0"
	},
	"date": "2018-07-03"
}
```
