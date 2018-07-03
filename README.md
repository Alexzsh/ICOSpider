# ICOSpider

### 1、数据请求接口


name|parameter|type|result
:---|:----|:-----|:-----
getData()|None|GET|json

**json格式 字段变动直接在单个项目中修改**
```json
[{
	"id": "1",
	"name": "QuarkChain ",
	"web": "https://www.quarkchain.io/",
	"telegram": "https://t.me/quarkchain",
	"github": "https://github.com/iotexproject/iotex-core",
	"etherscan": "https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0",
	"youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"
}, {
	"id": "2",
	"name": "a",
	"web": "http://www.baidu.com",
	"telegram": "https://t.me/quarkchain",
	"github": "https://github.com/iotexproject/iotex-core",
	"etherscan": "https://etherscan.io/token/0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0",
	"youtube": "https://www.youtube.com/c/UCWltsUAyiser4-_eLLGmpdg"
}]
```

### 2、结果发送接口
name|parameter|type|result
:---|:----|:-----|:-----
postData(json)|json|POST|None

```json
{
	"data": [{
		"id": 1,
		"name": "Sparkster",
		"AlexaRank": {
			"GlobalRank": "110883",
			"COUNTRY_RANK": "13435"
		},
		"TelegramChannelSize": "62820",
		"GitHubStar": "1234"
	}, {
		"id": 2,
		"name": "Seele",
		"AlexaRank": {
			"GlobalRank": "198649",
			"COUNTRY_RANK": "21804"
		},
		"TelegramChannelSize": "29875",
		"GitHubStar": "1234"
	}],
	"date": "2018-07-03"
}
```
