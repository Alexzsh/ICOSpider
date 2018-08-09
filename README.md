# ICOSprider

## Tor+privoxy+stem
> **Change ip via The Onion Route**
- Use privoxy to change http/https request to socks because of tor just for socks
- Use stem to control port restart enforce
- urllib or requests or selenium  use proxies to connect the privoxy's port
- [more setting](#Tor)

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
# Tor 
## **1.Intsall Tor**
```shell
sudo apt-get update
sudo apt-get install tor
sudo /etc/init.d/tor restart
```
默认监听9050端口

## **2.配置 Tor**
- 使其监听9051端口，之后stem中将通过Tor Controller与其通信，当然任何通信都可监听
- 配置一个密码 防止被外部代理随意访问 改密码会被自动哈希

  ```shell
tor --hash-password your_password
> 16:E600ADC1B52Cbalabala6022A0E999A7734571A451EB6AE50FED489B72E3DF
```
- 开启cookie认证模式（和密码登录二选一即可）
可以在配置文件/etc/tor/torrc中进行取消注释修改进行确认
```shell
ControlPort 9051
# hashed password below is obtained via `tor --hash-password your_password`
HashedControlPassword 16:E600ADC1B52Cbalabala6022A0E999A7734571A451EB6AE50FED489B72E3DF
CookieAuthentication 1
```
配置完成后重启tor服务
```shell
sudo /etc/init.d/tor restart
```


> 由于Tor本身并不是一个http代理，所以为了能够脸上tor，还需要使用privoxy进行转化，将http_proxy转到socks5

## **3.Install & config privoxy**

配置其将请求转发到socks5的端口即Tor
```shell
sudo apt-get install privoxy
forward-socks5 / localhost:9050           #127.0.0.1：9050
sudo /etc/init.d/privoxy restart
```
> ATTTTTTTENTION! privoxy配置好了如果出现`拒绝连接`的错误，需将`localhost`换成`127.0.0.1`,或者自行修改`hosts`文件

## **4. 使用stem 在python中进行控制**
```python
# TEST python3.x
# 强制Tor重建连接，获得新的ip
import stem
import stem.connection

from stem import Signal
from stem.control import Controller
header = {

'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Accept-Language': 'zh-CN,zh;q=0.9'

}

proxies={
    "http" : "127.0.0.1:8118",
    "https" : "127.0.0.1:8118"
}
# Build ProxyHandler object by given proxy
proxy_support=urllib.request.ProxyHandler(proxies)
# Build opener with ProxyHandler object
opener = urllib.request.build_opener(proxy_support)
# Install opener to request
urllib.request.install_opener(opener)
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='fyl815')
        controller.signal(Signal.NEWNYM)
        controller.close()
def get_public_ip(headers):
    request = urllib.request.Request("http://icanhazip.com", headers=headers)
    data = urllib.request.urlopen(request).read()
    print(data)

for i in range(10):
    renew_connection()
    get_public_ip(header)
```